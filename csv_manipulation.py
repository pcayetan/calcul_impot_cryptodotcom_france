import os
import pandas as pd
import csv
import numpy as np

# Goals: 
# - merge all files together
# - parse right transactions
# - parse all coins  


class transactions:

    def __init__(self) -> None:
        self.merger()
        self.parser()

    def get_transaction(self):
        df_trade = pd.read_csv('transactions_nettoyées/final.csv', index_col=0)
        df_trade.dropna(how="all", inplace=True)
        np_trade = df_trade.to_records(index=True)
        np_trade = np.flipud(np_trade)
        return np_trade
    
    def merger(self):
        directory = 'transactions_originales'
        data_frames = []
        for filename in os.listdir(directory):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory, filename)
                df = pd.read_csv(file_path)
                data_frames.append(df)
        merged_df = pd.concat(data_frames, ignore_index=True)
        merged_df.to_csv('transactions_nettoyées/merged.csv', index=False)

    def parser(self):
        csv_file  = "transactions_nettoyées/merged.csv"
        temp_file = "transactions_nettoyées/final.csv"
        column_index = 1
        field_value = ["MCO Lockup","MCO/CRO Wallet Swap","MCO Unlock","CRO Lockup","Crypto Earn Deposit", "CRO Lockup Rebate","Crypto Earn Withdrawal"]

        with open(csv_file, "r") as input_file, open(temp_file, "w", newline="") as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            for row in reader:
                if row[column_index] not in field_value:
                    writer.writerow(row)

