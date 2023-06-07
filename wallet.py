import pickle
import api
import numpy as np

class wallet:
    coins = {}
    values = {}
    total_in = 0
    total_out = 0
    coin_api = []

    def __init__(self) -> None:
        self.get_coins()

    def analyze_trade(self, trade):
        self.check_currency(trade[2])
        self.check_currency(trade[4])
        
    
    def check_currency(self, currency):
        if(currency in self.coins.keys() or currency is np.nan or currency == 'EUR'):
            return
        if not self.coin_api:
            self.get_coins_api()
        for coin in self.coin_api:
            if(coin['symbol'] == currency.lower()):
                self.coins.update({currency: coin['id']})
                self.save_coins()
                return
        print("Coin not found in API:", currency)
        id = input("\nGive id:")
        self.coins.update({currency: id})
        self.save_coins()
    
    def print_coins_dictionnary(self):
        print(self.coins)

    def get_coins_api(self):
        try:
            with open('data/coins_api.pickle', 'rb') as file:
                self.coin_api = pickle.load(file)
        except EOFError:
            endpoint = api.api
            self.coin_api = endpoint.get_coin_list()
            self.save_coins_api()

    def save_coins_api(self):
        with open('data/coins_api.pickle', 'wb') as file:
            pickle.dump(self.coin_api, file)

    
    def get_coins(self):
        try:
            with open('data/coins.pickle', 'rb') as file:
                self.coins = pickle.load(file)
        except EOFError:
            self.coins = {}

    def save_coins(self):
        with open('data/coins.pickle', 'wb') as file:
            pickle.dump(self.coins, file)
