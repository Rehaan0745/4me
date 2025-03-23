from demo import Bank  

bank_db = Bank()

while True:
    print("\n1. Create Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Account Details")
    print("5. Bank Statement")
    print("6. Exit")
    choice = input("Select an option: ")
    
    if choice == '1':
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        mobile_no = input(f"Enter mobile number: ")
        dob = input(f"Enter date of birth (YYYY-MM-DD): ")
        bank_db.create_customer(first_name, last_name, mobile_no, dob)
    
    elif choice == '2':
        account_id = int(input("Enter account ID: "))
        amount = float(input("Enter amount to deposit: "))
        bank_db.deposit_to_account(account_id, amount)
        account = bank_db.get_account(account_id)
        if account:
            print("Transaction Details:")
            for transaction in account.get_transaction_history():
                print(transaction)
    
    elif choice == '3':
        account_id = int(input("Enter account ID: "))
        amount = float(input("Enter amount to withdraw: "))
        bank_db.withdraw_from_account(account_id, amount)
        account = bank_db.get_account(account_id)
        if account:
            print("Transaction Details:")
            for transaction in account.get_transaction_history():
                print(transaction)

    elif choice == '4':  
        account_id = int(input("Enter account ID: "))
        account = bank_db.get_account(account_id)
        if account:
            account.export_details_to_txt()
        else:
            print("Account not found.")
    
    elif choice == '5': 
        account_id = int(input("Enter account ID: "))
        account = bank_db.get_account(account_id)
        if account:
            account.export_transactions_to_csv()
        else:
            print("Account not found.")
    
    elif choice == '6':
        break
    
    else:
        print("Invalid option. Please try again.")