from datetime import datetime
from dateutil.parser import parse
import requests
from get_station_codes import lines_with_codes as lines
from general.query_form import train_stop_query as query

LINE_CODES = {
    "BROWN": "Brn",
    "RED": "Red",
    "BLUE": "Blue",
    "YELLOW": "Y",
    "PURPLE": "P",
    "PINK": "Pnk",
    "ORANGE": "O",
    "GREEN": "Green"
}


def timing(station_name, station_line):
    """
    Speak to the CTA api to get arrival times for a stop, then gather
    the soonest arrival times in each direction the train is going. If
    a stop is more than 9 minutes away, it will be ignored, and a stop
    less than 1 minute away is considered approaching for the purposes of
    this program.
    """
    times = ['X', 'X']
    grabbed_destinations = ['None', 'None']
    mapid = lines[station_line][station_name]

    # do not error handle this; debugging micro:bits is hard
    url = query.replace('{mapid}', mapid)
    full_request = requests.get(url).json()

    # scrape for the soonest arrival in either direction
    i = 0
    wrapping_field = 'ctatt'
    all_arrivals_field = 'eta'
    dest_name_field = 'destNm'
    arrival_time_field = 'arrT'
    line_field = 'rt'

    full_request = full_request[wrapping_field]
    for arrival in full_request[all_arrivals_field]:
        if arrival[dest_name_field] not in grabbed_destinations\
                and arrival[line_field] == LINE_CODES[station_line]:
            grabbed_destinations[i] = arrival[dest_name_field]
            times[i] = arrival[arrival_time_field]
            i += 1
        if i >= 2: break

    # reduce the larger timezone string down to just the minute difference
    # between the estimated time and current time
    for i in range(len(times)):
        # divmod gives desirable results with rounding
        # convert time to datetime object, find out how far away it is from
        # the current time, and then divide for the difference in minutes
        try:
            times[i] = int(divmod(
                (
                    parse(times[i]) - datetime.now()).total_seconds(),
                    60
                )[0]
            )
            # stylistic choices
            if times[i] > 9: times[i] = 'X'
            elif times[i] <= 1: times[i] = 'A'
        # if times[i] is an X for no times found
        except:
            pass

        times[i] = f'{grabbed_destinations[i]}: {str(times[i])}'

    # sort to keep the presentation of the stops consistent across arrival
    # times
    return sorted(times, key=lambda x: x[1])
