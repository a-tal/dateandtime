#!/usr/bin/env python2.7
#coding: utf-8


"""A little clock to tell the date & time."""


import sys
import time
import datetime
import calendar


class ANSISettings(object):
    """ANSI terminal colour settings."""

    TODAY = "\033[94m"
    PAST = "\033[31m"
    OTHERMONTH = "\033[36m"
    END = "\033[0m"


ANSI = ANSISettings()


def print_calendar():
    """Prints the calendar, highlights the day."""

    now = datetime.datetime.now()
    # the TextCalendar(6) is to start the week on Sunday
    this_month = calendar.TextCalendar(6).formatmonth(now.year, now.month)
    today = str(int(now.strftime("%d")))
    first_day = True
    for line in this_month.splitlines():
        if now.strftime("%b") in line or "Mo" in line:
            print(line)
            continue
        formatted_days = []
        for day in line.split():
            if day == today:
                formatted_days.append("{end}{start}{day}{end}".format(
                    start=ANSI.TODAY,
                    day=_format_day(day),
                    end=ANSI.END,
                ))
                first_day = False
            else:
                if first_day:
                    first_day = False
                    formatted_days.append("{start}{day}".format(
                        start=ANSI.PAST,
                        day=_format_day(day),
                    ))
                else:
                    formatted_days.append(_format_day(day))
        print("{line}".format(line=_format_line(formatted_days)))


def _format_line(line):
    """For a line of a calendar, replace any whitespace with the next or
    previous month's dates.

    Args:
        line: the list of formatted days

    Returns:
        line, joined by spaces, including the other month's formatted dates
    """

    if len(line) < 7:
        first_week = True
        ending_days = ["28", "29", "30", "31"]
        for day in line:
            for ending_day in ending_days:
                # import pdb; pdb.set_trace()
                if ending_day == day:
                    first_week = False
                elif day.endswith("{}{}".format(ending_day, ANSI.END)):
                    first_week = False

        if first_week:
            return "{line}".format(
                line=" ".join(_get_last_days_of_last_month(line)),
            )
        else:
            return "{line}".format(
                line=" ".join(_get_next_days_of_next_month(line)),
            )
    else:
        return " ".join(line)


def _format_day(day):
    """Dates < 10 should have a leading space."""

    if int(day) < 10:
        return " {day}".format(day=day)
    else:
        return str(day)


def _get_last_days_of_last_month(line):
    """Fill in leading whitespace with ansi-formatted dates from last month."""

    now = datetime.datetime.now()
    day = 31
    while len(line) < 7:
        try:
            datetime.datetime(year=now.year, month=(now.month - 1), day=day)
        except ValueError:
            pass
        else:
            line.insert(0, "{start}{date}{end}".format(
                start=ANSI.OTHERMONTH,
                date=_format_day(day),
                end=ANSI.END,
            ))
        finally:
            day -= 1
    return line


def _get_next_days_of_next_month(line):
    """Fill in trailing whitespace with ansi-formatted dates for next month."""

    day = 0
    while len(line) < 7:
        day += 1
        line.append("{start}{date}{end}".format(
            start=ANSI.OTHERMONTH,
            date=_format_day(day),
            end=ANSI.END,
        ))
    return line


def print_spaces():
    """Prints a bunch of spaces..."""

    for _ in xrange(420):
        print("{newlines}".format(newlines="\n" * 10))


def print_time(now):
    """Prints the time line.

    Args:
        now: a datetime.now() object
    """

    sys.stdout.write("\r{tab}{hour}:{minute} {ampm}{tail}".format(
        tab=" " * (6 + (1 * (int(now.strftime("%I")) < 10))),
        hour=int(now.strftime("%I")),
        minute=now.strftime("%M"),
        ampm=now.strftime("%p").lower(),
        tail=" " * 5,
    ))
    sys.stdout.flush()


def be_a_clock():
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
        print_calendar()
        sys.stdout.write("\n")
        while starting_time.day == running_time.day:
            print_time(running_time)
            printed_time = running_time
            while printed_time.minute == running_time.minute:
                running_time = datetime.datetime.now()
                time.sleep(1)


if __name__ == "__main__":
    try:
        be_a_clock()
    except KeyboardInterrupt:
        raise SystemExit("\n")
