import folium
import json
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
from parsing_site import *
from zomato_example2 import *



def create_map(file):
    """
    (lst) -> None
    This function creates map with markers
    as html-file using list of names and locations
    """
    rest_dct = dict()

    # f = open(file+str(i))
    # data_rests = json.load(f)

    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


    map = folium.Map(zoom_start = 100)
    lay_restaurants = folium.FeatureGroup(name="Restaurants_map")

    # for i in range(0, 101, 20):
    f = open(file)
    data_rests = json.load(f)
    for restaurant in data_rests["restaurants"]:

        name_of_rest = restaurant["restaurant"]["name"]
        price = restaurant["restaurant"]["average_cost_for_two"]

        lat = restaurant["restaurant"]["location"]["latitude"]
        lon = restaurant["restaurant"]["location"]["longitude"]
        rest_dct[name_of_rest] = (lat, lon, price)

        lay_restaurants.add_child(folium.Marker(location=[float(lat), float(lon)], popup=name_of_rest+"\nAverage_cost_for_two: "+str(price),
                                    icon=folium.Icon(color="yellow", icon='cloud')))



    # for key in dct:
    #     try:
    #         location = geolocator.geocode(dct[key][0])
    #         if location != None:
    #             lat, long = location.latitude, location.longitude
    #             ams_of_restaurant = 0
    #             # print(lat, long)
    #             if lat_city-1<lat<lat_city +1 and long_city-1<long<long_city+1:
    #             # print("Finding coordinates of all places. Please wait ...")
    #             #     lay_hotels.add_child(folium.Marker(location=[lat, long], popup=key+ dct[key][1], icon = folium.Icon()))
    #             #     locations_coords.append((lat, long))
    #                 restaurant_dictionary = zomato.get_nearby_restaurants(lat, long)
    #                 # start
    #
    #                 for restaurant in restaurant_dictionary:
    #                     value = restaurant_dictionary[restaurant]
    #                     #
    #                     distance = ((lat - value[0])**2 + (long - value[1])**2)**(1/2)
    #                     if distance < 0.01:
    #                     #
    #
    #                         lay_hotels.add_child(folium.Marker(location=[value[0],value[1]], popup=restaurant + "price:" + str(value[2]), icon = folium.Icon(color='red')))
    #                         ams_of_restaurant += 1
    #                 # end
    #             if ams_of_restaurant != 0 and price > float(dct[key][1][:-1]):
    #                 lay_hotels.add_child(folium.Marker(location=[lat, long], popup=key + dct[key][1] + "\n" + str(ams_of_restaurant), icon=folium.Icon()))
    #                 locations_coords.append((lat, long))
    #
    #
    #         map.add_child(lay_hotels)
    #     except GeocoderTimedOut:
    #         continue
    #
    # map.add_child(lay_hotels)
    #
    # map.save("map_hotels.html")
    # return locations_coords

    map.add_child(lay_restaurants)

    map.save("restaurants_map_example.html")
    print(rest_dct)


if __name__ == "__main__":
    city = str(input("City: "))

    geolocator = Nominatim(user_agent="specify_your_app_name_here")


    city_coords = geolocator.geocode(city)
    lat, long = city_coords.latitude, city_coords.longitude
    print(lat, long)

    # all_restaurants(lat, long)
    info = Zomato(lat=str(lat), lon=str(long))


    info.write_res()

    file = "restaurants.json"
    create_map(file)


# if __name__ == "__main__":
#     name = input("City: ")
#     price = input("Price: ")
#
#     BASE_URL = "http://www.budgetplaces.com/{}/budget-hotels-list/?page=1".format(name.lower())
#     pars = Parsing()
#     text = pars.read_html(pars.get_from_url(BASE_URL))
#
#     create_map(pars.parse_all_sites(text, BASE_URL), name)


