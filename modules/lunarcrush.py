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
