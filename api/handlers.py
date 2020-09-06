import json
import config
import urllib.request

# we can additionally improve this by splitting handlers into modules
# i.e. stores module, something_else module
GET_STORES_PATH = "/data/stores"

class APIHandler:
    def register_routes(self):
        pass

class StoresHandler(APIHandler):
    stores = []
    postcodemap = {}
    storesextended = []
    def get_stores(self):
        return self.storesextended

# JSON specific handler for stores operations.
# if we were to have a Postgres-enabled handler, it would be reading sql tables here
# and returning the same array
class StoresJSONHandler(StoresHandler):
    stores_json_path = "data/stores.json"
    def __init__(self):
        # open stores.json for reading and load it into the stores variable
        with open(self.stores_json_path, "r") as stores_data:
            self.stores = json.load(stores_data)
        # merge stores with lat , lon from postcodes.io
        postcodearr = []
        for store in self.stores:
            postcodearr.append(store["postcode"])
        params = json.dumps({"postcodes": postcodearr}).encode("utf8")
        # if this service isn't available, need to handle the error but can't do much 
        try:
            req = urllib.request.Request("https://api.postcodes.io/postcodes", data=params,
                headers={"content-type": "application/json"})
            resp = urllib.request.urlopen(req)
            respjson = json.load(resp)
            for res in respjson["result"]:
                if (res["result"]):
                    self.postcodemap[res["query"]] = {
                        "latitude": res["result"]["latitude"],
                        "longitude": res["result"]["longitude"]
                    }
        except Exception as e: 
            print("Error occured while loading postcodes from postcodes.io: ", str(e))
        for store in self.stores:
            self.storesextended.append({
                "name": store["name"], 
                "postcode": store["postcode"], 
                "latitude": self.postcodemap[store["postcode"]]["latitude"] if store["postcode"] in self.postcodemap else None,
                "longitude": self.postcodemap[store["postcode"]]["longitude"] if store["postcode"] in self.postcodemap else None,
            })
    # if this class is declared in config.py, will be called by RouteHandler's constructor
    def register_routes(self):
        config.registered_routes[GET_STORES_PATH] = self.get_stores