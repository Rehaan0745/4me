import pandas as pd
import psycopg2
from contextlib import contextmanager
from decimal import Decimal
import random
import datetime
from collections import deque
import queue
import threading
import time

DB_NAME = "Banking"
DB_USER = "postgres"
DB_PASSWORD = "REHAAN4786"  
DB_HOST = "localhost"
DB_PORT = "5432"

def connect():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@contextmanager
def transaction(conn):
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
    finally:
        conn.close()

class BankAccount:
    def __init__(self, customer_id, name, account_id, balance=0.0):
        self.customer_id = customer_id
        self.name = name
        self.account_id = account_id
        self.balance = Decimal(balance)
        self.transactions = []
        self.transaction_queue = queue.Queue()
        self.processing_thread = threading.Thread(target=self.process_transactions)
        self.processing_thread.start()

    def deposit(self, amount):
        amount = Decimal(amount)
        if amount > 0:
            self.transaction_queue.put(('deposit', amount))
            print(f"Deposit of ${amount:.2f} queued.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        amount = Decimal(amount)
        if amount > 0:
            self.transaction_queue.put(('withdraw', amount))
            print(f"Withdrawal of ${amount:.2f} queued.")
        else:
            print("Withdrawal amount must be positive.")

    def process_transactions(self):
        while True:
            if not self.transaction_queue.empty():
                trans_type, amount = self.transaction_queue.get()
                self.process_transaction(trans_type, amount)
                self.transaction_queue.task_done()
            time.sleep(1)  # Sleep to prevent busy waiting

    def process_transaction(self, trans_type, amount):
        with connect() as conn:
            current_balance = self.get_current_balance(conn)

            if trans_type == 'deposit':
                self.balance += amount
                self.record_transaction(conn, 'Deposit', amount)
                self.update_balance_in_db(conn)
                print(f"Deposited: ${amount:.2f}. New balance: ${self.balance:.2f}")

            elif trans_type == 'withdraw':
                if amount <= current_balance:
                    self.balance -= amount
                    self.record_transaction(conn, 'Withdraw', amount)
                    self.update_balance_in_db(conn)
                    print(f"Withdrew: ${amount:.2f}. New balance: ${self.balance:.2f}")
                else:
                    print("Insufficient funds for withdrawal.")

    def get_current_balance(self, conn):
        with conn.cursor() as curs:
            curs.execute("SELECT balance FROM accounts WHERE account_id = %s;", (self.account_id,))
            result = curs.fetchone()
            return result[0] if result else 0

    def update_balance_in_db(self, conn):
        with conn.cursor() as curs:
            curs.execute(
                "UPDATE accounts SET balance = %s WHERE account_id = %s;",
                (self.balance, self.account_id)
            )

    def record_transaction(self, conn, trans_type, amount):
        with conn.cursor() as curs:
            curs.execute(
                "INSERT INTO transactions (account_id, amount, transaction_type) VALUES (%s, %s, %s)",
                (self.account_id, amount, trans_type)
            )
        self.transactions.append({
            "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Particulars": trans_type,
            "Withdrawals": amount if trans_type == 'Withdraw' else 0,
            "Deposits": amount if trans_type == 'Deposit' else 0,
            "Balance": self.balance
        })

    def export_details_to_txt(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"account_details_{self.account_id}_{timestamp}.txt"
        with open(filename, 'w') as file:
            file.write(f"Account ID: {self.account_id}\n")
            file.write(f"Customer ID: {self.customer_id}\n")
            file.write(f"Name: {self.name}\n")
            file.write(f"Balance: ${self.balance:.2f}\n")
            file.write("Transactions:\n")
            for transaction in self.transactions:
                file.write(f"{transaction}\n")
        print(f"Account details exported to {filename}.")

    def export_transactions_to_csv(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"transactions_{self.account_id}_{timestamp}.csv"
        df = pd.DataFrame(self.transactions)
        df.to_csv(filename, index=False)
        print(f"Transactions exported to {filename}.")

class Bank:
    def __init__(self):
        self.accounts = {}
        self.transactions = deque()

    def create_customer(self, first_name, last_name, mobile_no, dob):
        full_name = f"{first_name} {last_name}"
        account_id = random.randint(100000, 999999)
        new_account = BankAccount(customer_id=None, name=full_name, account_id=account_id)
        self.accounts[account_id] = new_account

        with connect() as conn:
            with conn.cursor() as curs:
                curs.execute(
                    "INSERT INTO customers (first_name, last_name, mobile_no, dob) VALUES (%s, %s, %s, %s) RETURNING customer_id;",
                    (first_name, last_name, mobile_no, dob)
                )
                customer_id = curs.fetchone()[0]
                new_account.customer_id = customer_id
                curs.execute(
                    "INSERT INTO accounts (account_id, customer_id, name, balance) VALUES (%s, %s, %s, %s);",
                    (account_id, customer_id, new_account.name, new_account.balance)
                )
                print(f"Account created for {full_name} with Account ID: {new_account.account_id}")

    def get_account(self, account_id):
        return self.accounts.get(account_id, None)

    def deposit_to_account(self, account_id, amount):
        account = self.get_account(account_id)
        if account:
            account.deposit(amount)
            self.transactions.append((account_id, 'Deposit', amount))

    def withdraw_from_account(self, account_id, amount):
        account = self.get_account(account_id)
        if account:
            account.withdraw(amount)
            self.transactions.append((account_id, 'Withdraw', amount))

    def display_account_details(self, account_id):
        account = self.get_account(account_id)
        if account:
            account.export_details_to_txt()
            account.export_transactions_to_csv()

    def export_all_transactions_to_csv(self):
        transactions_list = list(self.transactions)
        transactions_data = []
        for transaction in transactions_list:
            account_id, trans_type, amount = transaction
            transactions_data.append({
                "Account ID": account_id,
                "Transaction Type": trans_type,
                "Amount": amount,
                "Date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        df = pd.DataFrame(transactions_data)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"all_transactions_{timestamp}.csv"
        df.to_csv(filename, index=False)
        print(f"All transactions exported to {filename}.")