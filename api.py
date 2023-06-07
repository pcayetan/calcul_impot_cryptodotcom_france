import requests

class api:
    
    def get_coin_list():
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        coin_list = response.json()
        return coin_list