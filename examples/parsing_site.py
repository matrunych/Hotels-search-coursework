import requests

from bs4 import BeautifulSoup


class Parsing:
    def get_from_url(self, url):
        r = requests.get(url)
        with open('site.html', 'w') as output_file:
            output_file.write(r.text)
        return "site.html"

    def read_html(self, file):
        with open(file) as f:
            text = f.read()
        return text

    def parse(self, text):
        hotel_dct = dict()

        soup = BeautifulSoup(text)

        names_list = soup.findAll('a', {'class': 'accom-name bdd-est-name app-clickable-cta'})
        coords_list = soup.findAll('span', {'class': 'bdd-est-address'})
        price_list = soup.findAll('span', {'class': 'price-from-value bdd-est-price'})

        for i in range(len(names_list)):
            names_list[i] = names_list[i].text
            coords_list[i] = coords_list[i].text
            price_list[i] = price_list[i].text
            hotel_dct[names_list[i]] = (coords_list[i], price_list[i])

        return hotel_dct

    def parse_all_sites(self, text, url):
        all_hotels_dct = dict()
        for i in range(1, int(self.get_count_page(text))+1):
            url = url[:-1] + str(i)
            all_hotels_dct.update(self.parse(self.read_html(self.get_from_url(url))))

        return all_hotels_dct

    def get_count_page(self, text):
        soup = BeautifulSoup(text)
        page_list = soup.findAll('li', {'class': 'other'})
        count = page_list[-1].text
        return count


if __name__ == "__main__":
    pars = Parsing()
    name = input()
    BASE_URL = "http://www.budgetplaces.com/{}/budget-hotels-list/?page=1".format(name.lower())

    #london paris barcelona rome, new york, amsterdam, madrid, berlin, dublin, venice, brussels, lisbon

    #zomato london dublin rome milan lisbon vienna? prague

    text = pars.read_html(pars.get_from_url(BASE_URL))
    # print(text)
    # print(get_count_page(text))
    # print(parse(text))
    all_hotels = pars.parse_all_sites(text, BASE_URL)
    print(all_hotels)


