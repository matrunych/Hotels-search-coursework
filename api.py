import requests


class Api(object):
    def __init__(self, lat="0", lon="0",  start="0", radius="1000",
                 content_type='application/json'):
        self.start = start
        self.lon = lon
        self.lat = lat
        self.radius = radius
        self.host="https://developers.zomato.com/api/v2.1/search?&entity_type=city&start={}&count=20&lat={}&lon={}&radius={}&sort=real-distance".format(self.start, self.lat, self.lon, self.radius)
        self.user_key = "91657ee651c5913aae2a61747888e59f"
        self.headers = {
            "User-agent": "curl/7.43.0",
            'Accept': content_type,
            'X-Zomato-API-Key': self.user_key
        }

    def get(self, endpoint, params):
        """
        Get json from zomato with defined params
        """
        url = self.host + endpoint + "?"
        for k, v in params.items():
            url = url + "{}={}&".format(k, v)
        url = url.rstrip("&")
        response = requests.get(url, headers=self.headers)
        return response.json()



