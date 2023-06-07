import csv_manipulation
import wallet


def main():
    transactions = csv_manipulation.transactions()
    trades_data = transactions.get_transaction()
    money = wallet.wallet()
    for trade in trades_data:
        money.analyze_trade(trade)
    money.print_coins_dictionnary()


if __name__ == "__main__":
    main()