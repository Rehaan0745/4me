from banking import Bank  

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
        mobile_no = input("Enter mobile number: ")
        dob = input("Enter date of birth (YYYY-MM-DD): ")
        
        bank_db.create_customer(first_name, last_name, mobile_no, dob)
    
    elif choice == '2':
        try:
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                print("Amount must be positive.")
            else:
                bank_db.deposit_to_account(account_id, amount)
                print(f"Deposited ${amount:.2f} to account ID {account_id}.")
        except ValueError:
            print("Invalid input. Please enter numeric values for account ID and amount.")
    
    elif choice == '3':
        try:
            account_id = int(input("Enter account ID: "))
            amount = float(input("Enter amount to withdraw: "))
            if amount <= 0:
                print("Amount must be positive.")
            else:
                bank_db.withdraw_from_account(account_id, amount)
                print(f"Withdrew ${amount:.2f} from account ID {account_id}.")
        except ValueError:
            print("Invalid input. Please enter numeric values for account ID and amount.")

    elif choice == '4':  
        try:
            account_id = int(input("Enter account ID: "))
            account = bank_db.get_account(account_id)
            if account:
                account.export_details_to_txt()
            else:
                print("Account not found.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for account ID.")
    
    elif choice == '5': 
        try:
            account_id = int(input("Enter account ID: "))
            account = bank_db.get_account(account_id)
            if account:
                account.export_transactions_to_csv()  # Call the method from the BankAccount class
            else:
                print("Account not found.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for account ID.")
    
    elif choice == '6':
        print("Exiting the application. Goodbye!")
        break
    
    else:
        print("Invalid option. Please try again.")