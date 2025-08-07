"""
This file contains different static query URLs for the CTA API software.
"""

KEYFILE = '..//key.env'
with open(KEYFILE) as keyfile:
    keys = keyfile.readlines()
    TRAIN_KEY = keys[0].split('=')[1]
    BUS_KEY = keys[1].split('=')[1]
LINE_CODES = [
    "Brn",
    "Red",
    "Blue",
    "Y",
    "P",
    "Pink",
    "Org",
    "G"
]

def build(root, cmd, params):
    return root.format(cmd = cmd, params = params)


train_query_root = f'https://lapi.transitchicago.com/api/1.0/{{cmd}}?key={TRAIN_KEY}{{params}}&outputType=JSON'
# All trains on specified routes.
train_routes_query = build(train_query_root, 'ttpositions.aspx', f'&rt={','.join(LINE_CODES)}')
# Arrivals at a certain stop.
train_stop_query = build(train_query_root, 'ttarrivals.aspx', '&mapid={mapid}')


bus_query_root = f'https://www.ctabustracker.com/bustime/api/v3/{{cmd}}?key={BUS_KEY}{{params}}&format=json'
# All routes in the system, and display codes.
bus_all_routes_query = build(bus_query_root, 'getroutes', '')
# The directions serviced by a bus route
bus_line_dirs_query = build(bus_query_root, 'getdirections', '&rt={route}')
# All stops in a route, given a direction (standardized as Northbound, Southbound, Eastbound, Westbound literals)
bus_line_stops_query = build(bus_query_root, 'getstops', '&rt={route}&dir={dir}')
# List of stops and waypoints that form the shape of a line, regardless of direction.
# Some routes have more than one shape for either direction of travel. Only two patterns in the query return
# will be the default route, but there is no way to tell which two these are, except that they should be similar length.
bus_line_shape_query = build(bus_query_root, 'getpatterns', '&rt={route}')
# List of stops and waypoints that form the shape of a bus's specific route. pid comes from bus_bus_query below.
bus_bus_shape_query = build(bus_query_root, 'getpatterns', '&pid={pid}')
# Position of all buses on a given line, regardless of direction.
bus_line_bus_query = build(bus_query_root, 'getvehicles', '&rt={route}&tmres=s')
# Position of a given bus.
bus_bus_query = build(bus_query_root, 'getvehicles', '&vid={vid}&tmres=s')
# Estimation of how many minutes until a bus will arrive at a certain stop, by line.
# rt= can precede an empty string legally if no desire for specification.
# Please note: stop IDs seem to be unique by direction. So, at Belmont & Ashland, the 77 stop E (14918) is unique from
# the 9 and X9 stop S, which share an ID (18632), which are unique from the W / N versions. That is to say, each stpid
# is tied to the literal, physical stop shelter or post.
bus_stop_pred_query = build(bus_query_root, 'getpredictions', '&rt={rt}&stpid={stop_id}&tmres=s')
# Estimation of how many minutes until a bus will arrive at its next stop, by vehicle.
bus_bus_pred_query = build(bus_query_root, 'getpredictions', '&vid={vid}&tmres=s')
