"""
Process CTA stop data for relevant fields, and maintain dictionaries
of every line: the stops within those lines, and the map ids associated
with those stops.
"""

import csv

data_file_name = "stops.csv"
red_line = {}
blue_line = {}
green_line = {}
brown_line = {}
purple_line = {}
yellow_line = {}
pink_line = {}
orange_line = {}
lines_with_codes = {
    "RED": red_line,
    "BLUE": blue_line,
    "GREEN": green_line,
    "BROWN": brown_line,
    "PURPLE": purple_line,
    "YELLOW": yellow_line,
    "PINK": pink_line,
    "ORANGE": orange_line
}

with open(data_file_name) as stops:
    reader = csv.reader(stops)
    header = next(reader, None)
    name_col = header.index("STATION_NAME")
    full_name_col = header.index("STATION_DESCRIPTIVE_NAME")
    map_id_col = header.index("MAP_ID")
    # stop_id_col = header.index("STOP_ID")
    for stop in reader:
        for line in lines_with_codes.keys():
            if line in stop[full_name_col]:
                # if this overwrites an old stop, it doesn't matter; map_id is the id
                # for the entire station, and the direction of the stop is irrelevant
                # for our purposes. it's just redundant, but that's ok
                # lines[BROWN][PAULINA] = 41310
                lines_with_codes[line][stop[name_col]] = stop[map_id_col]
