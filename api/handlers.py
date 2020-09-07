import json
import config
import urllib.request
from math import sin, cos, sqrt, atan2, radians

# we can additionally improve this by splitting handlers into modules
# i.e. stores module, something_else module
GET_STORES_PATH = "/api/stores"
GET_NEAREST_STORES_PATH = "/api/neareststores"
SEARCH_STORES_PATH = "/api/searchstores"

class APIHandler:
    def register_routes(self):
        pass

class StoresHandler(APIHandler):
    def __init__(self):
        self.stores = []
        self.postcodemap = {}
        self.storesextended = []
        # ideally this should be a true graph. key is code1:code2 (pair of codes), value is the distance
        self.cacheddistances = {}
    def get_stores(self, get_params, query_params):
        return self.storesextended
    def get_nearest_stores(self, get_params, query_params):
        try :
            matching_stores = []
            postcode = get_params[0] # let's assume it's valid. 
            # if it can't be converted to float will propagate exception up
            radius = float(get_params[1])
            postcode_geoloc = (None, None)
            if postcode not in self.postcodemap:
                # get from postcodes.io, it may be something that didn't exist initially
                postcode_geoloc = self.get_geoloc(postcode)
                # cache so that we don't call postcodes.io again
                self.postcodemap[postcode] = {"latitude": postcode_geoloc[0], "longitude": postcode_geoloc[1]}
            else:
                postcode_geoloc = (self.postcodemap[postcode]["latitude"], self.postcodemap[postcode]["longitude"])
            # now iterate through cached distances, if we don't have the distance between two codes already
            # then calculate it and cache it 
            for store in self.storesextended:
                if store["latitude"] is None:
                    continue # can't process anything that does not have lat and lon
                key = postcode + ":" + store["postcode"]
                if key not in self.cacheddistances:
                    distance = self.get_distance(postcode_geoloc, (store["latitude"], store["longitude"]))
                    self.cacheddistances[key] = distance # cache
                distance = self.cacheddistances[key]
                if (distance <= radius):
                    matching_stores.append(store)
            # finally sort north to south (that is, by latitude value DESC)
            # 90 is north pole, -90 is south pole, 0 is equator. 
            matching_stores.sort(key=lambda x: x["latitude"], reverse=True)
            return matching_stores
        except Exception as e:
            raise Exception("Could not get nearest stores, please check if you have supplied valid params. Syntax <url>/api/neareststores/< valid UK postcode>/<radius km>: " + str(e))
    def get_geoloc(self, postcode):
            try:
                resp = urllib.request.urlopen("https://api.postcodes.io/postcodes/" + postcode)
                ret = json.load(resp)
                if (ret["result"] is None):
                    raise Exception("supplied postcode not found/invalid")
                return (ret["result"]["latitude"], ret["result"]["longitude"])
            except Exception as e:
                raise e
    def get_distance(self, loc1, loc2):
        # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude/43211266#43211266
        R = 6373.0
        lat1 = radians(loc1[0])
        lon1 = radians(loc1[1])
        lat2 = radians(loc2[0])
        lon2 = radians(loc2[1])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c
    def search_stores(self, get_params, query_params):
        params = {}
        for p in query_params.split('&'):
            qp = p.split('=')
            if len(qp) == 2:
                params[qp[0]] = qp[1]
        if "query" in params and len(params["query"]) > 0:
            query = params["query"].lower()
            # check how we are going to compare, with indexof/contains or startswith
            contains_matching = True
            if "type" in params and params["type"] == "startswith":
                contains_matching = False
            #postcode_matches = list(filter(lambda x: query in x["postcode"].lower(), self.storesextended))
            #city_matches = list(filter(lambda x: query in x["name"].lower(), self.storesextended))
            # do this with a proper loop. only one loop, the above code does two loops over the same data.
            postcode_matches = []
            city_matches = []
            for store in self.storesextended:
                added = False
                if (contains_matching and query in store["postcode"].lower()) or store["postcode"].lower().startswith(query):
                    postcode_matches.append(store)
                    added = True
                if (not added and contains_matching and query in store["name"].lower()) or store["name"].lower().startswith(query):
                    city_matches.append(store)
            # merge results such that postcodes are always sorted with priority 
            # on top of cities
            return postcode_matches + city_matches
        else:
            # return all because query string not supplied or empty
            return self.storesextended

# JSON specific handler for stores operations.
# if we were to have a Postgres-enabled handler, it would be reading sql tables here
# and returning the same array
class StoresJSONHandler(StoresHandler):
    stores_json_path = "data/stores.json"
    def __init__(self):
        super().__init__()
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
                    self.postcodemap[res["query"].replace(" ", "")] = {
                        "latitude": res["result"]["latitude"],
                        "longitude": res["result"]["longitude"]
                    }
        except Exception as e: 
            print("Error occured while loading postcodes from postcodes.io: ", str(e))
        for store in self.stores:
            pcode = store["postcode"].replace(" ", "")
            self.storesextended.append({
                "name": store["name"], 
                "postcode": store["postcode"], 
                "latitude": self.postcodemap[pcode]["latitude"] if pcode in self.postcodemap else None,
                "longitude": self.postcodemap[pcode]["longitude"] if pcode in self.postcodemap else None,
            })
    # if this class is declared in config.py, will be called by RouteHandler's constructor
    def register_routes(self):
        config.registered_routes[GET_STORES_PATH] = self.get_stores
        config.registered_routes[GET_NEAREST_STORES_PATH] = self.get_nearest_stores
        config.registered_routes[SEARCH_STORES_PATH] = self.search_stores