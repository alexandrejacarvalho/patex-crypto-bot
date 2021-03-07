from pycoingecko import CoinGeckoAPI


class CoinGeckoHelpers():
    def __init__(self):
        self.cg = CoinGeckoAPI()

    def get_coin_by_symbol(self, symbol):
        coins = self.cg.get_coins_list()
    
        for coin in coins:
            if coin["symbol"] == symbol:
                return coin["id"], coin["name"]
        else:
            return None, None
