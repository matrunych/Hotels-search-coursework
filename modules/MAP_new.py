import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
from PARSE_hotelscan import *
import zomatopy_1
from hidden import config

zomato = zomatopy_1.initialize_app(config)


def create_map(dct, name, price):
    """
    This function creates map with markers
    as html-file using dct of hotels and find hotel with zomato API
    Return dict with info about hotels'names, prices, restaurants nearby
    :param dct: dict
    :param name: str
    :param price: int
    :return: dict
    """
    locations_coords = []
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


    try:
        location_city = geolocator.geocode(name)
        lat_city, long_city = location_city.latitude, location_city.longitude
    except:
        raise ValueError("Invalid city")

    map = folium.Map(location=[lat_city, long_city],
                     zoom_start=12,
                     tiles='Stamen Terrain')

    lay_hotels = folium.FeatureGroup(name="Hotel_map")

    result = dict()

    for key in dct:
        try:

            if price > dct[key][1]:
                rests_lst =[]
                ams_of_restaurant = 0

                lat, long = dct[key][0][0], dct[key][0][1]
                restaurant_dictionary = zomato.get_nearby_restaurants(lat, long)


                if restaurant_dictionary == {}:
                    return "Zomato has not this city"



                for restaurant in restaurant_dictionary:
                    value = restaurant_dictionary[restaurant]

                    distance = ((float(lat) - value[0])**2 + (float(long) - value[1])**2)**(1/2)
                    if distance < 0.0099:

                        lay_hotels.add_child(folium.Marker(location=[value[0], value[1]],
                                              popup=restaurant + "\nAverage price for two:" + str(value[2]),
                                              icon=folium.Icon(color='green', icon="utensils")))
                        ams_of_restaurant += 1
                        rests_lst.append((restaurant, value[2]))

                if ams_of_restaurant != 0:

                    lay_hotels.add_child(folium.Marker(location=[float(lat), float(long)],
                       popup=key + "\nPrice per night for two: " + str(dct[key][1]) +
                                    "\nAmount of restaurants nearby: " + str(ams_of_restaurant),
                                    icon=folium.Icon(color="red", icon="home")))
                    locations_coords.append((lat, long))
                    result.setdefault(key, [])
                    result[key].append((dct[key][1], ams_of_restaurant, rests_lst))


            map.add_child(lay_hotels)
        except GeocoderTimedOut:
            continue

    map.add_child(lay_hotels)

    map.save("templates/map_hotels.html")
    return result


def main_creator():
    """
    Main function of program that call previous function
    """
    name = str(input("City: "))
    try:
        price = int(input("Price per night: "))
    except ValueError:
        price = 100000

    dct = parsing(name)

    create_map(dct, name, price)


# if __name__ == "__main__":
#     main_creator()
