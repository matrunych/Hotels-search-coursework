# import urllib.request
# from bs4 import BeautifulSoup
#
# BASE_URL = "https://www.booking.com/searchresults.en-gb.html?" \
#            "label=gen173nr-1FCAEoggI46AdIM1gEaOkBiAEBmAEJuAEHyAEN2AEB6AEB-AELiAIBqAIDuAKL7OXjBQ&" \
#            "lang=en-gb&sid=ec186a2d439b46eec4ed9b285de4130d&sb=1&src=index&src_" \
#            "elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.en-gb." \
#            "html%3Flabel%3Dgen173nr-1FCAEoggI46AdIM1gEaOkBiAEBmAEJuAEHyAEN2AE" \
#            "B6AEB-AELiAIBqAIDuAKL7OXjBQ%3Bsid%3Dec186a2d439b46eec4ed9b285de4130d%3Bsb_" \
#            "price_type%3Dtotal%26%3B&ss=london&is_ski_area=0&checkin_year=&checkin_month=" \
#            "&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4" \
#            "u_keep_filters=&from_sf=1"
#
#
# def get_html(url):
#     response = urllib.request.urlopen(url)
#     return response.read()
#
#
# def parse(html):
#     soup = BeautifulSoup(html, features="lxml")
#     table = soup.find('div', class_='hotellist_wrap tracked shorten _property_block')
#     print(table)

# def main():
#     parse(get_html(BASE_URL))
#
#
# if __name__ == "__main__":
#     main()

import requests
import re

from bs4 import BeautifulSoup

url = "http://www.booking.com/searchresults.ua.html"
payload = {
'ss':'Warszawa',
'si':'ai,co,ci,re,di',
'dest_type':'city',
'dest_id':'-534433',
'checkin_monthday':'25',
'checkin_year_month':'2015-10',
'checkout_monthday':'26',
'checkout_year_month':'2015-10',
'sb_travel_purpose':'leisure',
'src':'index',
'nflt':'',
'ss_raw':'',
'dcid':'4'
}

r = requests.post(url, payload)
html = r.content
parsed_html = BeautifulSoup(html, "lxml")

print (parsed_html.head.find('title').text)

tables = parsed_html.find_all("table", {"class" : "sr_item_legacy"})

print ("Found %s records." % len(tables))

with open("requests_results.html", "w") as f:
    f.write(str(r.content))

for table in tables:
    name = table.find("a", {"class" : "hotel_name_link url"})
    average = table.find("span", {"class" : "average"})
    price = table.find("strong", {"class" : re.compile(r".*\bprice scarcity_color\b.*")})
    print (name.text + " " + average.text + " " + price.text)