from api import Api
import json


class Zomato(object):
    def __init__(self, lat="0", lon="0", start="0", radius="1000"):
        self.api = Api(lat, lon, start, radius)

    # def search(self, **kwargs):
    #
    #     params = {}
    #     available_params = [
    #         "entity_id", "entity_type", "q", "start",
    #         "count", "lat", "lon", "radius", "cuisines",
    #         "establishment_type", "collection_id",
    #         "category", "sort", "order"]
    #
    #     for key in available_params:
    #         if key in kwargs:
    #             params[key] = kwargs[key]
    #
    #     results = self.api.get("/search", params)
    #     # return results
    #     f = open("restaurants____.json", mode="w")
    #     json.dump(results, f, indent=2)
    #     f.close()
    #     return results

    def write_res(self):
        params = {
            "lat": self.api.lat,
                  "lon": self.api.lon,
                  "start": self.api.start,
                  "radius": self.api.radius
                  }

        results = self.api.get("/search", params)
        # return results
        f = open("restaurants.json", mode="a")
        json.dump(results, f, indent=2)
        f.close()
        print(results)
        return results

#
# def num_of_rest_pages(results):
#     num_of_pages = results["results_found"]/20
#     if isinstance(num_of_pages, float):
#         num_of_pages = int(num_of_pages) + 1
#     return num_of_pages
#
#
# def all_restaurants():
#     info = Zomato(lat="51.569064", lon="-0.2524568", start="0")
#
#     data = info.write_res()
#     num = num_of_rest_pages(data)
#
#     if num > 10: # if num of rest pages more than 10 process only 10 else process all
#         num = 10
#
#     start_shown = 0
#     for i in range(num):
#         start_shown += 20
#         next_page_of_rests = Zomato(lat="51.569064", lon="-0.2524568", start=str(start_shown))
#         next_page_of_rests.write_res()
#         print("done ", start_shown)



if __name__ == "__main__":
    # all_restaurants()

    info = Zomato(lat="38.7077507", lon="-9.1365919", start="0")


    # city = "London"
    print(info.write_res())
