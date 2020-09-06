import config
from http.server import HTTPServer
from api.router import RouteHandler
from pydoc import locate

# register all concrete (*fully qualified*) route handler implementations defined in config
# e.g. ROUTE_HANDLERS = ".api.handlers.StoresJSONHandler" in config.py
for classstr in config.ROUTE_HANDLERS.split(","):
    RouteClass = locate(classstr) # must be fully qualified class name including packages etc
    RouteClass().register_routes() # calls the concrete register_routes

server = HTTPServer((config.HOST, config.PORT), RouteHandler)
server.serve_forever()