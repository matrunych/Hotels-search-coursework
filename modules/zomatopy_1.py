import requests
import ast

base_url = "https://developers.zomato.com/api/v2.1/"


def initialize_app(config):
    """
    Initialize app Zomato API with user-key
    :param config: dict
    """
    return Zomato(config)


class Zomato:
    """
    Class for representing Zomato
    """
    def __init__(self, config):
        """
        Defines variables
        :param config: dict
        """
        self.user_key = config["user_key"]


    def get_nearby_restaurants(self, latitude, longitude):
        """
        Takes the latitude and longitude as inputs.
        Returns a dictionary of Restaurant IDs and their corresponding Zomato URLs.
        :param latitude: str
        :param longitude: str
        """
        try:
            float(latitude)
            float(longitude)
        except ValueError:
            raise ValueError('InvalidLatitudeOr.decode("utf-8")Longitude')

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "geocode?" + "&lat=" + str(latitude) + "&lon=" + str(longitude),
                          headers=headers).content).decode("utf-8")
        r = r.split('"name"')
        rests = {}
        for i in range(len(r)):
            r[i] = r[i].split('"city_id"')
            try:
                r[i][1] = r[i][1].split(",")
                r[i][0] = r[i][0].split(",")
                name = r[i][0][0][2:-1]
                for el in r[i][1]:
                    if el[:22] == '"average_cost_for_two"':
                        rests[name] = [float(r[i][1][1].split(":")[1].strip('"')), float(r[i][1][2].split(":")[1].strip('"')), float(el.split(":")[1].strip('"'))]
                        break
            except:
                pass

        return rests


    def is_valid_restaurant_id(self, restaurant_ID):
        """
        Checks if the Restaurant ID is valid or invalid.
        If invalid, throws a InvalidRestaurantId Exception.
        """
        restaurant_ID = str(restaurant_ID)
        if restaurant_ID.isnumeric() == False:
            raise ValueError('InvalidRestaurantId')

    def is_valid_city_id(self, city_ID):
        """
        Checks if the City ID is valid or invalid.
        If invalid, throws a InvalidCityId Exception.
        """
        city_ID = str(city_ID)
        if city_ID.isnumeric() == False:
            raise ValueError('InvalidCityId')

    def is_key_invalid(self, a):
        """
        Checks if the API key provided is valid or invalid.
        If invalid, throws a InvalidKey Exception.
        """
        if 'my_modules' in a:
            if a['my_modules'] == 403:
                raise ValueError('InvalidKey')

    def is_rate_exceeded(self, a):
        """
        Checks if the request limit for the API key is exceeded or not.
        If exceeded, throws a ApiLimitExceeded Exception.
        """
        if 'my_modules' in a:
            if a['my_modules'] == 440:
                raise Exception('ApiLimitExceeded')



class DotDict(dict):
    """
    Dot notation access to dictionary attributes
    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# if __name__ == "__main__":
#     config={"user_key": "91657ee651c5913aae2a61747888e59f "}
#     info = Zomato(config)
#     city = "London"
#     # city_id = info.get_nearby_restaurants()
#     # print(city_id)
#     # print(info.restaurant_search(city_id))
#     print(info.get_nearby_restaurants("51.569064", "-0.2524568"))