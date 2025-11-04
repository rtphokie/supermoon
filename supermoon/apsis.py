from datetime import datetime, timedelta, date
from skyfield.api import Loader, Topos
import numpy as np
from scipy.signal import argrelextrema

load = Loader("/var/data")
planets = load("de421.bsp")


def next_apogee(dt=datetime.now(), days=30):
    return next_apsis(dt=dt, days=days, extrema="max")


def next_perigee(dt=datetime.now(), days=30):
    return next_apsis(dt=dt, days=days, extrema="min")


def next_apsis(dt=datetime.now(), days=30, extrema="min"):
    earth = planets["earth"]
    moon = planets["moon"]
    ts = load.timescale()

    # synodic month 29d 12h 44m 03s
    # day granulartiy
    t = ts.utc(dt.year, dt.month, range(dt.day, dt.day + days))
    dt, _ = _find_apsis(earth, moon, t, extrema)
    # hour granulartiy
    t = ts.utc(dt.year, dt.month, dt.day, range(dt.hour - 24, dt.hour + 24))
    dt, _ = _find_apsis(earth, moon, t, extrema)
    # minute granulartiy
    t = ts.utc(dt.year, dt.month, dt.day, dt.hour, range(dt.minute - 60, dt.hour + 60))
    dt, _ = _find_apsis(earth, moon, t, extrema)
    # second granulartiy
    t = ts.utc(
        dt.year,
        dt.month,
        dt.day,
        dt.hour,
        dt.minute,
        range(dt.second - 60, dt.second + 60),
    )
    dt, d = _find_apsis(earth, moon, t, extrema)

    return dt, round(d, 0)


def _find_apsis(earth, moon, t, extrema):
    dt = None
    value = None
    position = (moon - earth).at(t)
    d = position.distance().km
    if extrema == "min":
        dt = t[d.argmin()].utc_datetime()
        value = d.min()
    elif extrema == "max":
        dt = t[d.argmax()].utc_datetime()
        value = d.max()
    else:
        raise ValueError("please use extremas of min or max")

    return dt, value
