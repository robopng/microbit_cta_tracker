"""
THIS IS NOT A FUNCTIONAL SCRIPT FILE!
    This is an imported micropython script created on python.microbit.org.
It will not work if it is compiled into hex code locally; micro:bit devices
cannot accept the user-defined import "from sender_lines import LINES" and
if that file is inlined, the version 1 devices lack sufficient memory to load
the entire file. The existence of this file in the project is purely for
referential purposes.
    If you want to update the code wrtitten in this file, do so on
python.microbit.org, download a copy of the compiled .hex code, and replace
sender_outside_compile.hex with it.

    Main controller script for the sender micro:bit device. This script
encapsulates functionality for selecting a CTA stop on any of the CTA 'L' lines,
or loading in a default configuration (Paulina stop on the Brown line).
    Additionally, this script is responsible for initial serial communication
with the master controller device that will overwrite scripts dynamically to update
train arrival timing estimates.
"""

# from microbit import *
from microbit import button_a
from microbit import button_b
from microbit import display
from microbit import sleep
from microbit import Image
from micropython import const
from sender_lines import LINES
import radio

# DELAY, DELAY_FAST, and LOOP are purely cosmetic variables, but WAIT and
# CLEAR should not be changed unless you know what you are doing - they can
# softlock the device!
TEXT_DELAY = const(135)
TEXT_DELAY_FAST = const(100)
TEXT_WAIT = False
TEXT_LOOP = True
TEXT_CLEAR = True


def refresh():
    # initialize default configuration
    global station, line
    line = "BROWN"
    station = "PAULINA"


def main_menu():
    # display main menu options on startup
    # the main menu largely exists to allow quick boot-up with default
    global awaiting, answer, mode
    options = {
        "SETTINGS": settings,
        "DEFAULT": go,
    }
    options[_scan_options(options.keys())]()


def settings():
    global station, line, answer, mode
    mode = "MENU"
    # recursion depth error if a method call to set_station is made in set_line
    old_line = line
    # settings is the default return menu for all states the device can reach
    while True:
        options = {
            "SET LINE": set_line,
            "SET STATION": set_station,
            "CONFIRM": go,
            "RESET": refresh,
        }
        options[_scan_options(options.keys())]()
        # force station change if we changed lines
        if line != old_line:
            set_station()
            old_line = line
        display.show(Image.TARGET)
        sleep(500)


def set_line():
    global line
    line = _scan_options(LINES.keys())
    display.show(Image.SQUARE)
    sleep(500)


def set_station():
    global station, line
    station = _scan_options(LINES[line])
    display.show(Image.SQUARE)
    sleep(500)


def _scan_options(options):
    """
    Given an iterable, yield results on user input until a specific result
    is selected
    :param options: iterable choices will be given from
    :return: the user selected element from the given iterable
    """
    global answer
    # repeat scroll when end is passed
    while True:
        for option in options:
            show_text(option, speed=TEXT_DELAY_FAST)
            while scan_input() == -1: pass
            if answer == "SELECTED":
                return option


def go():
    """
    Initialize communication with the receiving micro:bit device, and send
    serial communication to the master controller to change states.
    """
    global station, line, awaiting, answer, mode
    radio.on()
    mode = "ON"
    radio.send('B' + station + ' ON THE ' + line + ' LINE ')
    # serial communication to master controller
    print(station + ',' + line)
    # loading icon
    display.show(Image('00300:03630:36063:03630:00300'))
    # either the script will be flash overwritten during execution of this loop
    # or mode will be changed by a button press to return to the settings menu
    while mode == "ON":
        scan_input()
    radio.off()


def scan_input():
    """
    Process different states of input on the micro:bit device.
    For the purposes of this project, only the two front buttons are considered.
    :return: -1 if there was no input
    """
    if button_a.is_pressed(): on_a()
    elif button_b.is_pressed(): on_b()
    else: return -1


def on_a():
    global answer, score, mode
    if mode == "MENU" or mode == "MAIN_MENU":
        answer = "SELECTED"
    sleep(150)


def on_b():
    global answer, score, mode
    if mode == "MENU" or mode == "MAIN_MENU":
        answer = "NEXT"
    elif mode == "ON":
        mode = "MENU"
    sleep(100)


def show_text(text, speed=TEXT_DELAY, wait=TEXT_WAIT, loop=TEXT_LOOP):
    """
    Cosmetic wrapper for the builtin display.scroll() function that allows for
    simply unified display of any text across many functions.
    :param text: the text to be scrolled
    :param speed: the speed at which that text will be scrolled, in ms
    :param wait: whether the program should hang until the text is done scrolling
    :param loop: whether the text should scroll continuously
    """
    display.clear()
    sleep(75)
    display.scroll(text + ' ', speed, wait=wait, loop=loop)


# MAKE SURE this number is identical to the ones defined in
# sender_dynamic.py and receiver_main.py
radio.config(group=0)
mode = "MAIN_MENU"

refresh()
sleep(2)
# await initial input
while scan_input() == -1: display.show(Image.ARROW_E)
display.clear()
main_menu()
