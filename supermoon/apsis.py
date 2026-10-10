from datetime import timedelta

from skyfield.searchlib import find_maxima, find_minima

from ._util import as_utc
from .ephemeris import planets, timescale


def next_apogee(dt=None, days=30):
    return next_apsis(dt=dt, days=days, extrema="max")


def next_perigee(dt=None, days=30):
    return next_apsis(dt=dt, days=days, extrema="min")


def next_apsis(dt=None, days=30, extrema="min"):
    """
    the first perigee (extrema="min") or apogee (extrema="max") on or after dt
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :param days: days to search; perigees and apogees are 24.6 to 28.6 days apart
    :return: datetime (UTC) and distance in km
    """
    dt = as_utc(dt)
    found = apsides(dt, dt + timedelta(days=days), extrema)
    if not found:
        raise ValueError(f"no {extrema} distance found within {days} days of {dt}")
    dt, d = found[0]
    return dt, round(d, 0)


def apsides(start, end, extrema="min"):
    """
    every perigee (extrema="min") or apogee (extrema="max") between start and end
    :return: list of (datetime (UTC), distance in km), in date order
    """
    if extrema == "min":
        find = find_minima
    elif extrema == "max":
        find = find_maxima
    else:
        raise ValueError("please use extremas of min or max")
    ts = timescale()
    t, d = find(ts.from_datetime(start), ts.from_datetime(end), _distance_km)
    return [(tt.utc_datetime(), float(dd)) for tt, dd in zip(t, d, strict=True)]


def _distance_km(t):
    e = planets()
    return (e["moon"] - e["earth"]).at(t).distance().km


_distance_km.step_days = 1.0
