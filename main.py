import csv_manipulation

transactions = csv_manipulation.transactions()

trades = transactions.get_transaction()
print(trades)