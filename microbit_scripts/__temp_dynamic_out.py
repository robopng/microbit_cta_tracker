"""
THIS IS NOT A FUNCTIONAL SCRIPT FILE!
    This is an unfinished script file that will be automatically completed
and flashed onto the sending micro:bit device during program execution.

    Secondary controller script for the sender micro:bit device. This script
handles communication with the receiving micro:bit device as well as communication
back to the master controller. The primary purpose of this controller, though, is to
store estimated arrival times for the selected stop from the main controller. These
arrival times are automatically inserted into the file during program execution;
this script is designed to not run itself without that insertion.
"""

from microbit import button_a, button_b
from microbit import display, Image
from microbit import sleep
import radio


def scan_input():
    """
    Process different states of input on the micro:bit device.
    For the purposes of this project, only the two front buttons are considered.
    :return: -1 if there was no input
    """
    if button_a.was_pressed():
        on_a()
    elif button_b.was_pressed():
        on_b()
    else:
        return -1


def on_a():
    # send serial code to switch
    print("EXIT")


def on_b():
    global timing, timing_alt
    timing, timing_alt = timing_alt, timing
    radio.send('M' + timing)


def go():
    """
    Initialize communication with the receiving micro:bit device, and listen for
    commands from that device, communicating them back to the master controller
    as necessary.
    """
    radio.on()
    radio.send('M' + timing)
    while True:
        display.show(Image('00300:03630:36963:03630:00300'))
        message = radio.receive()
        if message:
            if 'UPDATE' in message:
                print('UPDATE')
                # loading icon
                display.show(Image('00300:03630:36063:03630:00300'))
                sleep(500)
            if 'SWITCH' in message:
                # b button controls switch functionality
                on_b()
                # loading icon
                display.show(Image('00300:03630:36063:03630:00300'))
                sleep(1500)
        scan_input()


# MAKE SURE this number is identical to the ones defined in
# sender_main.py and sender_main.py
radio.config(group=0)

# AUTO-GENERATED BELOW THIS LINE
# ------------------------------
timing = "Kimball: X"
timing_alt = "Loop: 2"
go()
