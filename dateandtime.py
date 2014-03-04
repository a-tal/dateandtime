#!/usr/bin/env python2.7
#coding: utf-8


"""A little clock to tell the date & time."""


import os
import sys
import time
import datetime
import calendar

try:
    import ddate
except ImportError:
    pass  # optional, Discordianism support. see https://github.com/a-tal/ddate


class ANSISettings(object):
    """ANSI terminal colour settings."""

    TODAY = "\033[94m"
    PAST = "\033[31m"
    OTHERMONTH = "\033[36m"
    END = "\033[0m"


ANSI = ANSISettings()


def _calendar_header(date):
    """"Get the month/year and weekday abbreviates for the date object."""

    if hasattr(date, "SEASONS"):
        weekday_abbrs = [day[:2].title() for day in date.WEEKDAYS]
        return date.SEASONS[date.season], date.day_of_season, weekday_abbrs
    else:
        weekday_abbrs = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
        return date.strftime("%B"), date.strftime("%d"), weekday_abbrs


def make_disco_calendar(date):
    """Simulate calendar.TextCalendar for discordian dates."""

    first_day_of_season = ddate.DDate(
        datetime.date(
            year=date.date.year,
            month=date.date.month,
            day=date.date.day,
        ) - datetime.timedelta(days=date.day_of_season - 1),
    )

    weeks = []
    first_week = True

    for week in range(1, 73, 5):
        if first_week:
            weeks.append("{}{}{}".format(
                "  " * first_day_of_season.day_of_week,
                str(first_day_of_season.day_of_week + 1).rjust(2, " "),
                " ".join([str(x).rjust(2, " ") for x in range(
                    2, first_day_of_season.day_of_week + 6)]
                ),
            ))
            first_week = False
        else:
            weeks.append(" ".join(
                [str(x) for x in range(week, min(week + 5, 74))]))

    return weeks


def print_calendar(discordian=False, eve_is_real=False, eve_game=False):
    """Prints the calendar, highlights the day."""

    if discordian:
        date = ddate.DDate()
        this_month = make_disco_calendar(date)
    else:
        date = datetime.datetime.now()
        # the TextCalendar(6) is to start the week on Sunday
        this_month = calendar.TextCalendar(6).formatmonth(
            date.year,
            date.month,
        ).splitlines()[2:]

    if eve_is_real:
        year = 23236 + (date.year - 1900)
    elif eve_game:
        year = "YC {}".format(date.year - 1900)
    else:
        year = date.year

    month, day_of_month, weekday_abbrs = _calendar_header(date)

    tag_line = "{} {}".format(month, year)
    if discordian:
        max_width = 14
    else:
        max_width = 20

    if len(tag_line) > max_width:
        tag_line = "{} {}".format(month[:3], date.year)

    print("{}{}\n{}".format(
        " " * ((max_width - len(tag_line)) / 2),
        tag_line,
        " ".join(weekday_abbrs),
    ))

    first_day = True
    for line in this_month:
        formatted_days = []
        for day in line.split():
            if int(day) == int(day_of_month):
                formatted_days.append("{end}{start}{day}{end}".format(
                    start=ANSI.TODAY,
                    day=str(day).rjust(2),
                    end=ANSI.END,
                ))
                first_day = False
            else:
                if first_day:
                    first_day = False
                    formatted_days.append("{start}{day}".format(
                        start=ANSI.PAST,
                        day=str(day).rjust(2),
                    ))
                else:
                    formatted_days.append(str(day).rjust(2))
        print("{line}".format(line=_format_line(formatted_days, discordian)))


def _format_line(line, discordian=False):
    """For a line of a calendar, replace any whitespace with the next or
    previous month's dates.

    Args:
        line: the list of formatted days

    Returns:
        line, joined by spaces, including the other month's formatted dates
    """

    if len(line) < 7:
        first_week = True
        if discordian:
            ending_days = ["70", "71", "72", "73"]
        else:
            ending_days = ["28", "29", "30", "31"]
        for day in line:
            for ending_day in ending_days:
                if ending_day == day:
                    first_week = False
                elif day.endswith("{}{}".format(ending_day, ANSI.END)):
                    first_week = False

        if first_week:
            return "{line}".format(
                line=" ".join(_get_last_days_of_last_month(line, discordian)),
            )
        else:
            return "{line}".format(
                line=" ".join(_get_next_days_of_next_month(line, discordian)),
            )
    else:
        return " ".join(line)


def _get_last_days_of_last_month(line, discordian=False):
    """Fill in leading whitespace with ansi-formatted dates from last month."""

    if discordian:
        day = 73
        max_len = 5
    else:
        day = 31
        now = datetime.datetime.now()
        lastmonth = now.month - 1 or 12
        lastmonthyear = now.year - (now.month - 1 == 0)
        max_len = 7

    while len(line) < max_len:
        try:
            if not discordian:
                datetime.datetime(year=lastmonthyear, month=lastmonth, day=day)
        except ValueError:
            pass
        else:
            line.insert(0, "{start}{date}{end}".format(
                start=ANSI.OTHERMONTH,
                date=str(day).rjust(2),
                end=ANSI.END,
            ))
        finally:
            day -= 1
    return line


def _get_next_days_of_next_month(line, discordian=False):
    """Fill in trailing whitespace with ansi-formatted dates for next month."""

    day = 0
    while len(line) < (5 if discordian else 7):
        day += 1
        line.append("{start}{date}{end}".format(
            start=ANSI.OTHERMONTH,
            date=str(day).rjust(2),
            end=ANSI.END,
        ))
    return line


def print_spaces():
    """Prints a bunch of spaces..."""

    for _ in xrange(420):
        print("{newlines}".format(newlines="\n" * 10))


def print_time(now, discordian=False):
    """Prints the time line.

    Args:
        now: a datetime.now() object
    """

    if discordian:
        tab = 3
        tail = 2
    else:
        tab = 6
        tail = 5

    sys.stdout.write("\r{tab}{hour}:{minute} {ampm}{tail}".format(
        tab=" " * (tab + (1 * (int(now.strftime("%I")) < 10))),
        hour=int(now.strftime("%I")),
        minute=now.strftime("%M"),
        ampm=now.strftime("%p").lower(),
        tail=" " * tail,
    ))
    sys.stdout.flush()


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


def main():
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
    main()
