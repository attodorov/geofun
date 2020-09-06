import config
import json
from http.server import SimpleHTTPRequestHandler

# basic generic REST API router implementation
class RouteHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        route_info = self.resolveroute()
        if route_info is not None:
            self.execute_route(route_info["route"], route_info["route_params"], route_info["query_params"])
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
    def resolveroute(self):
        resolved_path = self.path
        path_parts = list(filter(None, self.path.split("/", )))
        query_params = ""
        if len(path_parts) >= 2: # e.g. if we have sth like /api/stores/<postcode>/<radius>
            resolved_path = "/" + path_parts[0] + "/" + path_parts[1]
            # url has query params, for example for filtering/sorting/search: ?query=<sth>
            if "?" in resolved_path:
                query_params = resolved_path[resolved_path.index("?")+1:len(resolved_path)]
                resolved_path = resolved_path[0:resolved_path.index("?")]
        if resolved_path in config.registered_routes.keys():
            url_params = []
            if len(path_parts) > 2:
                url_params = path_parts[2:]
            return {"route":resolved_path, "route_params":url_params, "query_params": query_params}
        return None
    def execute_route(self, route, route_params, query_params):
        # execute registered route as function and get response data
        # this is possible due to the fact that Python's functions are first class objects
        # example: GET /data/stores => calls StoresJSONHandler.get_stores()
        try:
            response_data = config.registered_routes[route](route_params, query_params)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response_data, ensure_ascii=False), "utf-8"))
        except Exception as e:
            self.send_error(500, str(e))