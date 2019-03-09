import json
import folium
from geopy.geocoders import Nominatim


def map_foium_use(file):
    f = open(file)
    data = json.load(f)
    map = folium.Map()
    lay = folium.FeatureGroup(name="Restaurant_map")

    for restaurant in data["restaurants"]:
        name_of_rest = restaurant["restaurant"]["name"]

        lat = restaurant["restaurant"]["location"]["latitude"]
        lon = restaurant["restaurant"]["location"]["longitude"]

        lay.add_child(folium.Marker(location=[float(lat), float(lon)], popup=name_of_rest,
                                    icon=folium.Icon()))

    map.add_child(lay)

    map.save("restaurants_map_example.html")



if __name__ == "__main__":
    file = "restaurants.json"
    map_foium_use(file)

