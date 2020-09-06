import config
import json
from http.server import SimpleHTTPRequestHandler

# basic generic REST API router implementation
class RouteHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.canroute():
            self.execute_route()
        else:
            # delegate to parent (this will serve static content such as index.html,css, etc.)
            super().do_GET()
    def do_HEAD(self):
        super().do_HEAD()
    def do_POST(self):
        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/501
        self.send_response(501)
    def do_PUT(self):
        self.send_response(501)
    def do_DELETE(self):
        self.send_response(501)
    def canroute(self):
        if self.path in config.registered_routes.keys():
            return True
        return False
    def execute_route(self):
        # execute registered route as function and get response data
        # this is possible due to the fact that Python's functions are first class objects
        # example: GET /data/stores => calls StoresJSONHandler.get_stores()
        try:
            response_data = config.registered_routes[self.path]()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response_data, ensure_ascii=False), "utf-8"))
        except Exception as e:
            self.send_error(500, str(e))