import zomatopy

config={
  "user_key":"91657ee651c5913aae2a61747888e59f "
}

zomato = zomatopy.initialize_app(config)
# city_name must be a string without numbers or special characters.
city_ID = zomato.get_city_ID("London")

# city_ID must be an integer.
establishment_types_dictionary = zomato.get_establishment_types(61)


restaurants = zomato.restaurant_search(61)

#print(establishment_types_dictionary)
#print(city_ID)
print(restaurants)
