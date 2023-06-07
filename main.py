import csv_manipulation
import wallet


def main():
    transactions = csv_manipulation.transactions()
    trades_data = transactions.get_transaction()
    money = wallet.wallet(2022)
    for trade in trades_data:
        money.analyze_trade(trade)
    print(money.values, money.total_in)


if __name__ == "__main__":
    main()