import zomatopy_1
from geopy.geocoders import Nominatim
from hidden import config


zomato = zomatopy_1.initialize_app(config)

def is_valid_input(city):
    """
    Check if city with defined name exists
    :param city: str
    :return: bool or tuple
    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    try:
        location_city = geolocator.geocode(city)
        lat_city, long_city = location_city.latitude, location_city.longitude
        return lat_city, long_city
    except:
        return False


def zomato_valid(city):
    """
    Checks if zomato has info about defined city
    :param city: str
    :return: str or bool
    """
    if is_valid_input(city) != False:
        lat, long = is_valid_input(city)
        restaurant_dictionary = zomato.get_nearby_restaurants(lat, long)
        if restaurant_dictionary == {}:
            return "Zomato invalid"
        else:
            return True
    return "Invalid city"

