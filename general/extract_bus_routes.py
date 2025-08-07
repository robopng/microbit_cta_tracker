"""
Extract a static dictionary of route numbers and names for CTA bus routes, using various query calls.
"""
import json
import requests
from query_form import bus_all_routes_query, bus_line_shape_query, bus_line_stops_query, bus_line_dirs_query

OUT_FILE = 'routes.json'
ROUTES = {}

grab = requests.get(bus_all_routes_query).json()
shell = 'bustime-response'
grab_shell = 'routes'
route_num = 'rtdd'
route_color = 'rtclr'
route_name = 'rtnm'

for route in grab[shell][grab_shell]:
    num = route[route_num]
    name = route[route_name]
    color = route[route_color]

    # nab shapes (of routes) for given route number.
    # shapes will be given as a dictionary of points, in order; some are stops, some are waypoints.
    # information is entirely preserved for further processing.
    shapes_shell = 'ptr'
    shapes = requests.get(
        bus_line_shape_query.format(route = num)
    ).json()[shell][shapes_shell]

    # nab directions that given route number runs in, for use in nabbing stops below.
    dirs_shell = 'directions'
    dirs_field = 'id'
    dirs = [
        dir[dirs_field]
        for dir in requests.get(
            bus_line_dirs_query.format(route = num)
        ).json()[shell][dirs_shell]
    ]

    # nab all stops in given route in either direction.
    # stops are given as a dictionary of stops, and collated here together with their directional heading.
    # information is entirely preserved for further processing.
    stops_shell = 'stops'
    stops = [
        {
            'dir': dir,
            'stops': requests.get
                (
                    bus_line_stops_query.format(route = num, dir = dir)
                ).json()[shell][stops_shell]
        }
        for dir in dirs
    ]

    ROUTES[num] = {
        'name': name,
        'color': color,
        'shapes': shapes,
        'stops': stops
    }
    print(f'Finished route number: {num}')

with open(OUT_FILE, 'w') as file:
    json.dump(ROUTES, file)
