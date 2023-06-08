import requests
import time

class api:

    def get_coin_list():
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        coin_list = response.json()
        return coin_list
    
    def fetch_coin_value(self, coin_id, date):
        query = "https://api.coingecko.com/api/v3/coins/" + coin_id + "/history?date=" + date + "&localization=fr"
        print(query)
        response = requests.get(query)
        
        if(response.status_code == 200):
            response_json = response.json()
            try:
                value = response_json['market_data']['current_price']['eur']
                print(value)
            except:
                print("No value found for " + coin_id + " at " + date)
                value = 0
        else:
            print("Waiting for server...")
            time.sleep(16)
            value = self.fetch_coin_value(self, coin_id, date)
        return value