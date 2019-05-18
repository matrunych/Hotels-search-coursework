import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager




class Parsing:
    def get_from_url(self, url):

        r = requests.get(url)
        with open('hotelscan.html', 'w') as output_file:
            output_file.write(r.text)
        return "hotelscan.html"

    def read_html(self, file):
        with open(file) as f:
            text = f.read()
        # print(text)
        return text

    def parse(self, text):
        hotel_dct = dict()

        soup = BeautifulSoup(text)
        coords = []

        names_list = soup.findAll('h3', {'class': 'name'})
        coords_list = soup.findAll('p', {'class': 'location'})

        price_list = soup.findAll('span', {'class': 'currency-value '})
        print(price_list)

        for i in range(len(names_list)):
            names_list[i] = names_list[i].text
             # price_list[i] = price_list[i].text
            # price = price_list[i].find("span", {'span': 'currency-value'}).text

            lat_lon_coords = re.findall('-?\d+\.\d+', str(coords_list[i]))
            hotel_dct[names_list[i]] = (lat_lon_coords)




        return hotel_dct

    def parse_all_sites(self, text, url):
        all_hotels_dct = dict()
        for i in range(1, int(self.get_count_page(text))+1):
            url = url[:-1] + str(i)
            all_hotels_dct.update(self.parse(self.read_html(self.get_from_url(url))))

        return all_hotels_dct

    def get_count_page(self, text):
        soup = BeautifulSoup(text)
        page_list = soup.findAll('a', {'class': 'change-page'})
        print(page_list)
        count = page_list[-1].text
        print(count)
        return count


if __name__ == "__main__":


    pars = Parsing()
    BASE_URL = "https://hotelscan.com/ru/search?geoid=xmmdk0vfx09k&checkin=2019-05-30&checkout=2019-05-31&rooms=2"
    text = pars.parse(pars.read_html(pars.get_from_url(BASE_URL)))

    print(text)
    print(pars.get_count_page(text))
    # print(parse(text))
    all_hotels = pars.parse_all_sites(text, BASE_URL)
    for hot in all_hotels:
        print(all_hotels[hot])


