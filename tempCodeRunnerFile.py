# Example transactions for Alice
# account = bank.retrieve_account(1)  # Assuming account ID 1 belongs to Alice
# if account:
#     account.deposit(connect(), 500)  # Deposit $500
#     account.withdraw(connect(), 200)   # Withdraw $200

# # Example transactions for Bob
# account = bank.retrieve_account(2)  # Assuming account ID 2 belongs to Bob
# if account:
#     account.deposit(connect(), 300)  # Deposit $300
#     account.withdraw(connect(), 100)   # Withdraw $100

# # Export transactions to CSV
# bank.export_transactions_to_csv(1, "alice_transactions.csv")
# bank.export_transactions_to_csv(2, "bob_transactions.csv")
# # Convert CSV to Excel
# bank.convert_csv_to_excel("alice_transactions.csv", "alice_transactions.xlsx")
# bank.convert_csv_to_excel("bob_transactions.csv", "bob_transactions.xlsx")