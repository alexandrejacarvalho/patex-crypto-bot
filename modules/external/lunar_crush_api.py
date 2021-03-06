import requests

from system import config


class LunarCrushAPI:
    def __init__(self, endpoint=""):
        self.url = f"https://api.lunarcrush.com/v2{endpoint}"

    def _request(self, **kwargs):
        if kwargs:
            parameters = []
            for kwarg in kwargs:
                parameters.append("{key}={value}".format(
                    key=kwarg,
                    value=kwargs[kwarg]
                ))

            self.url += "?{query_params}".format(
                query_params="&".join(parameters)
            )

        r = requests.get(self.url)
        print(self.url)
        print(r.text)
        return r.json()

    def _get_data_for_symbol(self, symbol):
        return self._request(data="assets", key=config.LUNAR_CRUSH_API_KEY, symbol=symbol)

    def get_price_for_symbol(self, symbol, timestamp=None):
        if timestamp == None:
            data = self._get_data_for_symbol(symbol)

            return data["data"]["price"]
        else:
            raise Exception("Feature not developed yet.")