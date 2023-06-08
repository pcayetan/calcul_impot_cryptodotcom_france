import csv_manipulation
import wallet
import pandas as pd


def main():
    transactions = csv_manipulation.transactions()
    trades_data = transactions.get_transaction()
    money = wallet.wallet()
    for trade in trades_data:
        money.analyze_trade(trade)
    print(money.array_out,money.total_in,money.total_out,money.nb_out)
    print(money.global_value("07-06-2023"))
    df_out = pd.DataFrame(money.array_out)
    df_out.to_csv('./cessions.csv')

if __name__ == "__main__":
    main()