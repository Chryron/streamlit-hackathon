import pandas as pd
from openrouteservice import convert


class Route:
    route_df = pd.DataFrame()
    instructions = ""
    route_bbox = [(0, 0), (1, 1)]

    def __init__(self, route_result, instructions) -> None:
        self.instructions = instructions

        if isinstance(route_result, dict):
            geometry = route_result['routes'][0]['geometry']
            decoded = convert.decode_polyline(geometry)
            path = [{"name": "route",
                    "path": decoded['coordinates'],
                     "color": (0, 255, 255)}]
            self.route_df = pd.DataFrame(path)
            self.route_bbox = ((route_result["bbox"][0], route_result["bbox"][1]), (
                route_result["bbox"][2], route_result["bbox"][3]))
            # self.route_df = pd.DataFrame(
            #     decoded['coordinates'],
            #     columns=['lon', 'lat'])
