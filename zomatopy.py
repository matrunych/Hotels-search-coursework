import requests
import ast

base_url = "https://developers.zomato.com/api/v2.1/"


def initialize_app(config):
    return Zomato(config)


class Zomato:
    def __init__(self, config):
        self.user_key = config["user_key"]

    def get_city_ID(self, city_name):
        """
        Takes City Name as input.
        Returns the ID for the city given as input.
        """
        if city_name.isalpha() == False:
            raise ValueError('InvalidCityName')
        city_name = city_name.split(' ')
        city_name = '%20'.join(city_name)
        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "cities?q=" + city_name, headers=headers).content).decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        if len(a['location_suggestions']) == 0:
            raise Exception('invalid_city_name')
        elif 'name' in a['location_suggestions'][0]:
            city_name = city_name.replace('%20', ' ')
            if str(a['location_suggestions'][0]['name']).lower() == str(city_name).lower():
                return a['location_suggestions'][0]['id']
            else:
                raise ValueError('InvalidCityId')


    def get_establishment_types(self, city_ID):
        """
        Takes City ID as input.
        Returns a sorted dictionary of all establishment type IDs and their respective establishment type names.
        """
        self.is_valid_city_id(city_ID)

        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "establishments?city_id=" + str(city_ID), headers=headers).content).decode("utf-8")
        a = ast.literal_eval(r)

        self.is_key_invalid(a)
        self.is_rate_exceeded(a)

        temp_establishment_types = {}
        establishment_types = {}
        if 'establishments' in a:
            for establishment_type in a['establishments']:
                temp_establishment_types.update({establishment_type['establishment']['id'] : establishment_type['establishment']['name']})

            for establishment_type in sorted(temp_establishment_types):
                establishment_types.update({establishment_type : temp_establishment_types[establishment_type]})

            return establishment_types
        else:
            raise ValueError('InvalidCityId')


    def restaurant_search(self, query="", latitude="", longitude="", cuisines="", limit=5):
        """
        Takes either query, latitude and longitude or cuisine as input.
        Returns a list of Restaurant IDs.
        """
        cuisines = "%2C".join(cuisines.split(","))
        if str(limit).isalpha() == True:
            raise ValueError('LimitNotInteger')
        headers = {'Accept': 'application/json', 'user-key': self.user_key}
        r = (requests.get(base_url + "search?q=" + str(query) + "&count=" + str(limit) + "&lat=" + str(latitude) + "&lon=" + str(longitude) + "&cuisines=" + str(cuisines), headers=headers).content).decode("utf-8")
        a = ast.literal_eval(r)

        restaurants = []

        if a['results_found'] == 0:
            return []
        else:
            for restaurant in a['restaurants']:
                restaurants.append(restaurant['restaurant']['id'])

        return restaurants
