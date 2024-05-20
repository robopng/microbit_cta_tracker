from datetime import datetime
from dateutil.parser import parse
import requests
from get_station_codes import lines_with_codes as lines

KEY = """6dd9e6c145b046bf916c32cb83f56949"""


def timing(station_name, station_line):
    """
    Speak to the CTA api to get arrival times for a stop, then gather
    the soonest arrival times in each direction the train is going. If
    a stop is more than 9 minutes away, it will be ignored, and a stop
    less than 1 minute away is considered approaching for the purposes of
    this program.
    """
    times = [None, None]
    grabbed_destinations = [None, None]
    mapid = lines[station_line][station_name]

    # do not error handle this; debugging micro:bits is hard
    url = (
            f'http://lapi.transitchicago.com/api/1.0/'
            + f'ttarrivals.aspx'
            + f'?key={KEY}'
            + f'&mapid={mapid}'
            + f'&outputType=JSON'
    )
    full_request = requests.get(url).json()

    # scrape for the soonest arrival in either direction
    i = 0
    wrapping_field = 'ctatt'
    all_arrivals_field = 'eta'
    dest_name_field = 'destNm'
    arrival_time_field = 'arrT'
    full_request = full_request[wrapping_field]
    for arrival in full_request[all_arrivals_field]:
        if arrival[dest_name_field] not in grabbed_destinations:
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
        times[i] = int(divmod(
            (parse(times[i]) - datetime.now()).total_seconds(),
            60
        )[0])
        # stylistic choices
        if times[i] > 9: times[i] = 'X'
        elif times[i] <= 1: times[i] = 'A'

        times[i] = f'{grabbed_destinations[i]}: {str(times[i])}'

    # sort to keep the presentation of the stops consistent across arrival
    # times
    return sorted(times, key=lambda x: x[1])