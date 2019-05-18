import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut
from parsing_site import *
import zomatopy_1


config={
  "user_key": "91657ee651c5913aae2a61747888e59f "
}

zomato = zomatopy_1.initialize_app(config)


def create_map(dct, name, price=10000):
    """
    (lst) -> None
    This function creates map with markers
    as html-file using list of names and locations
    """
    locations_coords = []
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    location_city = geolocator.geocode(name)
    lat_city, long_city = location_city.latitude, location_city.longitude

    map = folium.Map(location=[lat_city, long_city],
                     zoom_start=12,
                     tiles='Stamen Terrain')

    lay_hotels = folium.FeatureGroup(name="Hotel_map")


    result = dict()

    # html = """
    #     <h1> This is a big popup</h1><br>
    #     With a few lines of code...
    #     <p>
    #     <code>
    #         from numpy import *<br>
    #         exp(-2*pi)
    #     </code>
    #     </p>
    #     """

    for key in dct:
        try:
            location = geolocator.geocode(dct[key][0])
            if location != None and price > float(dct[key][1][:-1]):
                rests_lst =[]
                lat, long = location.latitude, location.longitude
                ams_of_restaurant = 0
                # print(lat, long)

                if lat_city-1<lat<lat_city +1 and long_city-1<long<long_city+1:
                # print("Finding coordinates of all places. Please wait ...")

                    restaurant_dictionary = zomato.get_nearby_restaurants(lat, long)
                    # start

                    for restaurant in restaurant_dictionary:
                        value = restaurant_dictionary[restaurant]
                        #
                        distance = ((lat - value[0])**2 + (long - value[1])**2)**(1/2)
                        if distance < 0.0099:
                        #

                            lay_hotels.add_child(folium.Marker(location=[value[0], value[1]], popup=restaurant + "\nPrice:" + str(value[2]), icon = folium.Icon(color='green', icon="utensils")))
                            ams_of_restaurant += 1
                            rests_lst.append((restaurant, value[2]))
                    # end

                if ams_of_restaurant != 0:
                    # iframe = folium.IFrame(html=html, width=500, height=300)
                    # popup = folium.Popup(iframe, max_width=2650)

                    # key + dct[key][1] + "\n"
                    lay_hotels.add_child(folium.Marker(location=[lat, long], popup=key + dct[key][1] + "\n" + str(ams_of_restaurant), icon=folium.Icon(color="red", icon="home")))
                    locations_coords.append((lat, long))
                    result.setdefault(key, [])
                    result[key].append((dct[key][1], ams_of_restaurant, rests_lst))



            map.add_child(lay_hotels)
        except GeocoderTimedOut:
            continue

    map.add_child(lay_hotels)


    # folium.Marker([30, -100], popup=popup).add_to(map)

    map.save("templates/map_hotels.html")
    return result


if __name__ == "__main__":
    name = str(input("City: "))
    price = int(input("Price per night: "))
    BASE_URL = "http://www.budgetplaces.com/{}/budget-hotels-list/?page=1".format(name.lower())
    pars = Parsing()
    text = pars.read_html(pars.get_from_url(BASE_URL))

    print(create_map(pars.parse_all_sites(text, BASE_URL), name))

#if price == None pricedefault = 10000,

