from flask import Flask, render_template, request
from MAP_new import *
from PARSE_hotelscan import *
from is_valid import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index_fon.html")


@app.route("/search", methods=["POST"])
def info():
    city = request.form["city"]
    if is_valid_input(city) == False:
        return render_template("index.html")

    try:
        price = int(request.form["price"])
    except:
        price = 10000


    if zomato_valid(city) == "Zomato invalid":
        return render_template("failure_.html")  # must be input


    dct = parsing(city)
    create_map(dct, city, price)

    return render_template("map_hotels.html")

if __name__ == "__main__":
    app.run(debug=True)
