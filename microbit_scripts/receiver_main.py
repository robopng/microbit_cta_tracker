"""
THIS IS NOT A FUNCTIONAL SCRIPT FILE!
    This is an imported micropython script created on python.microbit.org.
It may be compiled locally, but it would not be possible to transmit it remotely
to the receiving micro:bit device (and there is no builtin COM port functionality
for that device). The existence of this file in the project is purely for
referential purposes.
    If you want to update the code wrtitten in this file, do so on
python.microbit.org, download a copy of the compiled .hex code, and upload it
directly to the receiving micro:bit device.

    Controller script for the receiver micro:bit device. This script handles
functionality for receiving messages, and for communicating commands back to the
sending micro:bit device.
"""
from microbit import button_a, button_b
from microbit import display, Image
from microbit import sleep
from micropython import const
import radio

TEXT_DELAY = const(135)
TEXT_DELAY_FAST = const(110)
TEXT_WAIT = True
TEXT_LOOP = False
TEXT_CLEAR = True


def show_text(text, speed=TEXT_DELAY, wait=TEXT_WAIT, loop=TEXT_LOOP):
    """
    Cosmetic wrapper for the builtin display.scroll() function that allows for
    simply unified display of any text across many functions.
    :param text: the text to be scrolled
    :param speed: the speed at which that text will be scrolled, in ms
    :param wait: whether the program should hang until the text is done scrolling
    :param loop: whether the text should scroll continuously
    """
    display.scroll(text + ' ', speed, wait=wait, loop=loop)


def scan_input():
    """
    Process different states of input on the micro:bit device.
    For the purposes of this project, only the two front buttons are considered.
    :return: -1 if there was no input
    """
    if button_a.was_pressed():
        display.show(Image.SQUARE_SMALL, wait=False)
        on_a()
    elif button_b.was_pressed():
        display.show(Image.SQUARE_SMALL, wait=False)
        on_b()
    else:
        return -1


def on_a():
    global direction
    direction = (direction + 1) % 2
    show_text(times[direction][:-2], speed=TEXT_DELAY_FAST)


def on_b():
    radio.send("UPDATE")


def process_command(command):
    """
    Process a command code for its respective consequence.
    :param command: command code to be processed
    """
    # add more in an elif chain
    if command == 'SWITCH': on_a()


def go():
    """
    Begin receiving input from the sending micro:bit device.
    Process input as either an intial ('B'), continuous ('M'), or
    service ('S') message.
    """
    global times
    radio.on()
    while True:
        message = radio.receive()
        if message:
            # B messages are of the format X on the Y line
            if message[0] == 'B':
                try:
                    space = message.index(' on ')
                except ValueError:
                    # some kind of mangling occurred in transmission
                    space = message.index(' ')
                show_text(message[1:space])
                display.show(message[space + 1:], delay=TEXT_DELAY_FAST, clear=True)
            # M messages are of the format X Y
            elif message[0] == 'M':
                message = message[1:]
                times = message.split('|')
                show_text(times[direction][:-2], speed=TEXT_DELAY_FAST)
            elif message[0] == 'S':
                message = message[1:]
                process_command(message)
        display.show(times[direction][-1])
        scan_input()


# MAKE SURE this number is identical to the ones defined in
# sender_dynamic.py and sender_main.py
radio.config(group=0)

direction = 0
times = ('None: X', 'None: X')
# await initial input
while scan_input() == -1: display.show(Image.ARROW_E)
display.clear()
go()
