import pickle
import api
import numpy as np

class wallet:
    coins = {}
    values = {}
    total_in = 0
    total_out = 0
    nb_out = 0
    coins_api = []
    year = "2022"
    array_out = np.array(["Date", "Prix total d'acquisition", "Valeur cession", "Valeur portefeuille"])

    def __init__(self) -> None:
        self.get_coins()

    def analyze_trade(self, trade):
        self.check_currency(trade[2])
        self.check_currency(trade[4])
        self.update_wallet(trade, 2)
        self.update_wallet(trade, 4)
        self.update_total_in(trade)
        self.update_out(trade)

    
    def check_currency(self, currency):
        if(currency in self.coins.keys() or currency is np.nan or currency == 'EUR'):
            return
        if not self.coins_api:
            self.get_coins_api()
        encountered_values = []
        for coin in self.coins_api:
            if(coin['symbol'] == currency.lower()):
                encountered_values.append(coin['id'])

        index = 0
        if(len(encountered_values) == 0):
            print("Coin not found in API:", currency)
            id = input("\nGive id:")
            self.coins.update({currency: id})
            self.save_coins()
            return
        if(len(encountered_values) > 1):
            print("Multiple IDs found for ", currency, "\n")
            i = 0
            for value in encountered_values:
                print(value, " : ", i)
                i += 1
            try:
                index = int(input("\nType the number for the correct ID:"))
            except ValueError:
                print("Please enter a valid integer")
        self.coins.update({currency: encountered_values[index]})
        self.save_coins()
        
        
    
    def print_coins_dictionnary(self):
        print(self.coins)

    def get_coins_api(self):
        try:
            with open('data/coins_api.pickle', 'rb') as file:
                self.coins_api = pickle.load(file)
        except EOFError:
            endpoint = api.api
            self.coins_api = endpoint.get_coin_list()
            self.save_coins_api()

    def save_coins_api(self):
        with open('data/coins_api.pickle', 'wb') as file:
            pickle.dump(self.coins_api, file)

    
    def get_coins(self):
        try:
            with open('data/coins.pickle', 'rb') as file:
                self.coins = pickle.load(file)
        except EOFError:
            self.coins = {}

    def save_coins(self):
        with open('data/coins.pickle', 'wb') as file:
            pickle.dump(self.coins, file)

    def update_total_in(self, trade):
        if (("EUR ->" in trade[1]) or ("Buy " in trade[1]) or ("From " in trade[1])):
            self.total_in += trade[7]

    def update_wallet(self, trade, emplacement):
        if(trade[emplacement] is np.nan or trade[emplacement] == 'EUR'):
            return
        value = self.values.get(trade[emplacement])
        if(value):
            self.values.update({trade[emplacement]: value+trade[emplacement+1]})
        else:
            self.values.update({trade[emplacement]: trade[emplacement+1]})
        if self.values[trade[emplacement]] < 0.1:
            del self.values[trade[emplacement]]

    def update_out(self, trade):
        # Calculer la cession
        if ("-> EUR" in trade[1]):
            self.nb_out += 1
            self.total_out += trade[7]
            #if trade[0][:4] == self.year:
            date = self.setup_date(trade[0][:10])
            valeur_portefeuille = self.global_value(date)
            #else:
                #valeur_portefeuille = np.nan
            row = np.array([trade[0], self.total_in, trade[7], valeur_portefeuille])
            self.array_out = np.vstack((self.array_out, row))

    def setup_date(self, date):
        date = date.replace("/", "-")
        flipped_date = "-".join(date.split("-")[::-1])
        return flipped_date
    
    def global_value(self, date):
        wallet_value = 0
        for coin_id in self.values:
            if(self.values[coin_id] != 0):
                endpoint = api.api
                coin_value = endpoint.fetch_coin_value(endpoint,self.coins[coin_id], date)
                wallet_value += coin_value * self.values[coin_id]
        return wallet_value