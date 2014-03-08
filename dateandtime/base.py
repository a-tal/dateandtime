#coding: utf-8

"""A little clock to tell the date & time."""


import os
import sys
import time
import datetime

try:
    import ddate
except ImportError:
    pass  # optional, Discordianism support. see https://github.com/a-tal/ddate

from dateandtime.formatting import print_spaces, print_calendar, print_time


def be_a_clock(discordian=False, eve_is_real=False, eve_game=False):
    """Displays a calendar with the day highlighted, a blank line and the time
    of day. Will loop forever. Sends many blank lines during a day change to
    badly update the highlighted day.

    ░░░░░░░░░░░░▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄░░░░░░░░░░░░░
    ░░░░░▄▄▄▄█▀▀▀░░░░░░░░░░░░▀▀██░░░░░░░░░░░
    ░░▄███▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█▄▄▄░░░░░░░
    ▄▀▀░█░░░░▀█▄▀▄▀██████░▀█▄▀▄▀████▀░░░░░░░
    █░░░█░░░░░░▀█▄█▄███▀░░░░▀▀▀▀▀▀▀░▀▀▄░░░░░
    █░░░█░▄▄▄░░░░░░░░░░░░░░░░░░░░░▀▀░░░█░░░░
    █░░░▀█░░█░░░░▄░░░░▄░░░░░▀███▀░░░░░░░█░░░
    █░░░░█░░▀▄░░░░░░▄░░░░░░░░░█░░░░░░░░█▀▄░░
    ░▀▄▄▀░░░░░▀▀▄▄▄░░░░░░░▄▄▄▀░▀▄▄▄▄▄▀▀░░█░░
    ░█▄░░░░░░░░░░░░▀▀▀▀▀▀▀░░░░░░░░░░░░░░█░░░
    ░░█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▄██░░░░
    ░░▀█▄░░░░░░░░░░░░░░░░░░░░░░░░░▄▀▀░░░▀█░░
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    █▀▄░█▀▀░█▀█░█░░░░█░▄░█░█░▀█▀░█░█░░█░▀█▀░
    █░█░█▀▀░█▀█░█░░░░▀▄▀▄▀░█░░█░░█▀█░░█░░█░░
    ▀▀░░▀▀▀░▀░▀░▀▀▀░░░▀░▀░░▀░░▀░░▀░▀░░▀░░▀░░
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    """

    while True:
        starting_time = datetime.datetime.now()
        running_time = starting_time
        print_spaces()
        print_calendar(discordian, eve_is_real, eve_game)
        sys.stdout.write("\n")
        while starting_time.day == running_time.day:
            print_time(running_time, discordian)
            printed_time = running_time
            while printed_time.minute == running_time.minute:
                running_time = datetime.datetime.now()
                time.sleep(1)


def cmdline_entry():
    """Super lazy arg parsing and main routine."""

    os.system("setterm -cursor off")
    discordian = False
    eve_game = False
    eve_is_real = False
    if "ddate" in globals() and len(sys.argv) == 2 and "-d" in sys.argv[1]:
        discordian = True
    elif len(sys.argv) == 2 and "-e" in sys.argv[1]:
        eve_game = True
    elif len(sys.argv) == 2 and "-r" in sys.argv[1]:
        eve_is_real = True
    try:
        be_a_clock(discordian, eve_is_real, eve_game)
    except KeyboardInterrupt:
        raise SystemExit("\n")
    finally:
        os.system("setterm -cursor on")


if __name__ == "__main__":
    cmdline_entry()
