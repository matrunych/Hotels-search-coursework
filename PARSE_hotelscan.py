import requests
import datetime
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from is_valid import is_valid_input

def parsing(name):
    """
    Parse site with hotels of defined city
    Return dict with hotels' names, coordinates and price per night for two
    :param name: str
    :return: dict
    """
    currentDT = datetime.datetime.now()
    year = str(currentDT.year)
    month = str(currentDT.month)
    day = str(currentDT.day)
    tommorow = currentDT + datetime.timedelta(days=1)
    tommorow_year = str(tommorow.year)
    tommorow_month = str(tommorow.month)
    tommorow_day = str(tommorow.day)

    if is_valid_input(name) == False:
        return "Enter city name correctly"


    id = requests.get('https://hotelscan.com/autocomplete?q=%7B%22locale%22%3A%22en%22%2'
                      'C%22term%22%3A%22{}%22%2C%22pos%22%3A%22ua%22%7D'.format(name)).json()['suggest'][0]['hs_id']


    hotel_dct = dict()
    for page in range(5):
        BASE_URL = "https://hotelscan.com/ru/search?geoid={}&checkin={}-{}-{}&" \
                   "checkout={}-{}-{}&rooms=2&page={}".format(id, year,
                                    month, day, tommorow_year,
                                    tommorow_month, tommorow_day, page)

        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        driver.get(BASE_URL)

        url = driver.execute_script("return document.documentElement.outerHTML")

        soup = BeautifulSoup(url, features="html.parser")

        hotels_lst = soup.find("section", id="property-list")

        names_lst = []
        coords_lst = []
        prices_lst = []


        for property in hotels_lst.find_all(class_ = "property"):
            names = property.find_all('h3', {'class': 'name'})
            coords = property.find_all(class_="hidden")
            prices = property.find_all(class_="currency-value")
            for i in range(len(names)):
                try:
                    names_lst.append(names[i].text)
                    lat_long = re.findall('-?\d+\.\d+', str(coords[i]))
                    coords_lst.append(lat_long)
                    prices_lst.append(round(int(prices[i].text)/27))

                    hotel_dct[names[i].text] = (lat_long, round(int(prices[i].text)/27))
                except IndexError:
                    continue


    if hotel_dct == {}:
        while hotel_dct == {}:
            hotel_dct = parsing(name)


    return hotel_dct


# if __name__ == "__main__":
#     name = "lokooon"
#     print(parsing(name))

