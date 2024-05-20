"""
Handle all serial communication with the sending micro:bit device.
Version: 1.2
"""

from script_to_hex import convert, push
from get_station_codes import lines_with_codes as lines
from get_station_timings import timing
import serial


def write_dynamic(times):
    """
    Finish the remaining portion of sender_dynamic.py, filling in
    relevant timing information and inserting an initial function call.
    :param times: the times to be given to the sending micro:bit device
    :return: the path to the complete sender_dynamic script
    """
    dyn_script_path = './microbit_scripts/sender_dynamic.py'
    out_path = f'./microbit_scripts/__temp_dynamic_out.py'

    with open(dyn_script_path, mode='r') as file:
        file_contents = file.read()

    with open(out_path, mode='w') as file:
        file.write(file_contents)
        file.write(
            f'timing = "{times[0]}|{times[1]}"\n'
            f'go()\n'
        )

    return out_path


def update_timing():
    """
    Get new time information for the stop.
    When new time information is retrieved, hand it off to
    the sending micro:bit device through the secondary dynamic controller.
    """
    global station, line
    times = timing(station, line)
    convert(write_dynamic(times))


def check_input(station_name):
    """
    Process serial input from the sending micro:bit device.
    :param station_name: the full provided input
    """
    global station, line
    station_name = station_name.split(',')
    station, line = station_name
    #
    if line in lines and station in lines[line]:
        update_timing()


station = None
line = None
# baud rate defined by micro:bit, COM port determined locally
ser = serial.Serial('COM3', 115200, timeout=0.1)
# initialize the sending micro:bit device
push(r'microbit_scripts/sender_outside_compile.hex')
# this dump seems to help things work, though I'm not entirely sure why.
ser.readall()
start_time = 0
while True:
    # if time.time() - start_time <= listen_interval_length: continue
    # else: start_time = time.time()

    code = ser.readall().decode('utf-8').strip()
    if ',' in code:
        check_input(code.strip())
    elif 'EXIT' in code:
        print(code)
        push(r'microbit_scripts/sender_outside_compile.hex')
    elif 'UPDATE' in code:
        print(code)
        update_timing()
    elif code:
        print(code)

