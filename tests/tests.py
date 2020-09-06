import unittest
from api.handlers import StoresHandler

class TestStoresHandlerMethods(unittest.TestCase):
    def test_get_nearest_stores(self):
        # first add some stores
        self.storesHandler.storesextended.append({
            "name": "St_Albans",
            "postcode": "AL1 2RJ",
            "latitude": 51.7420243,
            "longitude": -0.3429438
        })
        self.storesHandler.storesextended.append({
            "name": "Worthing",
            "postcode": "BN14 9GB",
            "latitude": 50.8348996,
            "longitude": -0.3687757
        })
        self.storesHandler.storesextended.append({
            "name": "Rustington",
            "postcode": "BN16 3RT",
            "latitude": 50.8180813,
            "longitude": -0.5007961
        })
        self.storesHandler.storesextended.append({
            "name": "Eastbourne",
            "postcode": "BN23 6QD",
            "latitude": 50.786528,
            "longitude": 0.3006973
        })
        self.storesHandler.storesextended.append({
            "name": "Newhaven",
            "postcode": "BN9 0AG",
            "latitude": 50.7979911,
            "longitude": 0.0582773
        })
        stores = self.storesHandler.get_nearest_stores(("CT195SY", 100))
        self.assertEqual(len(stores), 2)
        self.assertEqual(stores[0]["name"], "Newhaven")
        self.assertEqual(stores[1]["name"], "Eastbourne")
    # this is not a "true" unit test, meaning it actually calls postcodes.io. so it's more of a scenario test
    def test_get_geoloc(self):
        geoloc_info = self.storesHandler.get_geoloc("RH159QT")
        self.assertEqual(geoloc_info[0], 50.950564)
        self.assertEqual(geoloc_info[1], -0.149078)
    def test_get_distance(self):
        self.assertEqual(self.storesHandler.get_distance((52.2296756, 21.0122287), (52.406374, 16.9251681)), 278.54558935106695)
    def setUp(self):
        self.storesHandler = StoresHandler()
    def tearDown(self):
        pass