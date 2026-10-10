"""
In general, a supermoon is a full moon which occurs near the closest point in its
orbit making it appear bigger and brighter. However, there is no official nor even
consistent definition for the concept of supermoon leading to disagreements on which
full moons should receive the label and which should not.

Known definitions are calculated here
  * Richard Nolle
      rule 1 (1979) - A full or new Moon occurring at a distance 90% or greater than
                      the perigee in a given orbit
                      Dell Horoscope, 1979
      rule 2 (2000) - A full or new Moon occurring at a distance 90% or greater than
                      mean perigee
                      https://www.astropro.com/features/articles/supermoon/
      rule 3 (2011) - A full or new Moon occurring at a distance 90% or greater than
                      the closest perigee for the calendar year. This definition is
                      also preferred by EarthSky.com
                      https://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle
                      https://www.astropro.com/features/tables/cen21ce/suprmoon.html
  * Fred Espenak - A full or new Moon occurring at a distance 90% or greater of
    perigee during the current lunation, also used by EarthSky
    http://astropixels.com/ephemeris/moon/fullperigee2001.html
  * Sky and Telescope magazine - A full Moon within 223,000 miles (358,884 km) of Earth
  * TimeandDate.com - A full Moon within 360,000 kilometres (223,694 mi) of Earth
    https://www.timeanddate.com/astronomy/moon/super-full-moon.html
    https://www.timeanddate.com/moon/phases/
"""

import csv
from datetime import UTC, datetime, timedelta
from functools import cache, lru_cache
from pathlib import Path

from tzlocal import get_localzone

from .apsis import apsides, next_apogee
from .lunarphases import next_full_moon

KM_TO_MI = 0.621371

# range covered by the JPL DE421 ephemeris
MIN_YEAR = 1900
MAX_YEAR = 2050
CSV_FIELDS = (
    "fullmoon_local_date",
    "perigee_local_date",
    "perigee_distance_km",
    "perigee_distance_mi",
    "angular_diameter",
)


def next_supermoon(dt=None):
    """
    calculates when the next supermoon will occur based on known criteria
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :return: dictionary
    """
    if dt is None:
        dt = datetime.now(UTC)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    result = _full_moon(dt)
    while not any(result["definitions"].values()):
        result = _full_moon(result["fullmoon"]["date"] + timedelta(days=1))
    return result


@lru_cache(maxsize=512)
def _full_moon(dt):
    """
    evaluates the first full moon after dt against each supermoon definition
    """
    # find datetime and distance of next full moon from the date given
    fm_date, fm_dist, diameter = next_full_moon(dt)

    # perigee nearest the full moon and the apogee after it (for Espenak definition)
    window = timedelta(days=16)
    perigees = apsides(fm_date - window, fm_date + window, "min")
    p_date, p_dist = min(perigees, key=lambda p: abs(p[0] - fm_date))
    p_dist = round(p_dist, 0)
    _, a_dist = next_apogee(p_date)

    rel_dist_orbit = (a_dist - fm_dist) / (a_dist - p_dist)

    # find closest perigee and furthest apogee of the year for (Nolle definition)
    min_perigee, max_apogee = _year_extremes(fm_date.year)
    rel_dist_year = (max_apogee - fm_dist) / (max_apogee - min_perigee)

    # time separation between perigee and full moon (for within 24 hours definition)
    perigeedelta = abs((p_date - fm_date).total_seconds())

    return {
        "definitions": {
            "Sky & Telescope": bool(fm_dist <= 358884),
            "Time & Date": bool(fm_dist <= 360000),
            "Espenak": bool(rel_dist_orbit >= 0.9),
            "Nolle": bool(rel_dist_year >= 0.9),
            "within 1 day of perigee": perigeedelta <= 86400.0,
        },
        "relative distance": {
            "thisorbit": float(rel_dist_orbit),
            "thisyear": float(rel_dist_year),
        },
        "fullmoon": {
            "date": fm_date,
            "localdate": fm_date.astimezone(get_localzone()),
            "distance": float(fm_dist),
        },
        "perigee": {
            "date": p_date,
            "localdate": p_date.astimezone(get_localzone()),
            "distance": float(p_dist),
        },
        "full perigee delta seconds": perigeedelta,
        "full perigee delta hours": perigeedelta / 3600,
        "angular diameter": str(diameter),
        "angular diameter raw": diameter.degrees,
    }


@cache
def _year_extremes(year):
    """
    distance of the closest perigee and furthest apogee during a calendar year (UTC)
    """
    start = datetime(year=year, month=1, day=1, tzinfo=UTC)
    end = datetime(year=year + 1, month=1, day=1, tzinfo=UTC)
    min_perigee = min(d for _, d in apsides(start, end, "min"))
    max_apogee = max(d for _, d in apsides(start, end, "max"))
    return round(min_perigee, 0), round(max_apogee, 0)


def next_supermoons(count=1, dt=None):
    """
    the next count supermoons on or after dt
    :param count: number of supermoons to return
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :return: list of dictionaries, as returned by next_supermoon
    """
    results = []
    for _ in range(count):
        result = next_supermoon(dt=dt)
        results.append(result)
        dt = result["fullmoon"]["date"] + timedelta(days=1)
    return results


def supermoons(year):
    """
    all supermoons during a calendar year (UTC)
    :param year: year between 1900 and 2050
    :return: list of dictionaries, as returned by next_supermoon
    """
    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ValueError(
            f"year must be between {MIN_YEAR} and {MAX_YEAR} (per JPL DE421), "
            f"got {year}"
        )
    results = []
    dt = datetime(year=year, month=1, day=1, tzinfo=UTC)
    while True:
        result = next_supermoon(dt=dt)
        if result["fullmoon"]["date"].year != year:
            break
        results.append(result)
        dt = result["fullmoon"]["date"] + timedelta(days=1)
    return results


def describe(result, perigee=False, distance=False, angulardiameter=False):
    """
    human readable description of a supermoon
    :param result: dictionary, as returned by next_supermoon
    :return: list of lines
    """
    lines = []
    fullmoon, perigee_info = result["fullmoon"], result["perigee"]
    msgstr = (
        f"{fullmoon['localdate']:%a %m/%d/%Y %I:%M %p %Z} ({fullmoon['date']:%H:%M %Z})"
    )
    if distance:
        msgstr += f" {_km_mi(fullmoon['distance'])}"
    thelist = []
    for definition, meets in result["definitions"].items():
        if meets:
            thelist.append(definition)
    if len(thelist) == len(result["definitions"].values()):
        definitions = "all known definitions"
    elif len(thelist) == 2:
        definitions = " and ".join(thelist)
    elif len(thelist) > 2:
        definitions = f"{', '.join(thelist[:-1])}, and {thelist[-1]}"
    else:
        definitions = thelist[0]
    lines.append(f"  {msgstr} according to {definitions}")
    if angulardiameter:
        lines.append(f"   angular diameter: {result['angular diameter']}")
    if perigee:
        distmsgstr = (
            f"   perigee: {perigee_info['localdate']:%m/%d/%Y %H:%M %Z}"
            f" ({result['full perigee delta hours']:.2f} hours from full moon)"
        )
        if distance:
            distmsgstr += f" {_km_mi(perigee_info['distance'])}"
        lines.append(distmsgstr)
    return lines


def _km_mi(km):
    return f"{km:,} km ({km * KM_TO_MI:,.1f} mi)"


def csv_row(result):
    """
    flattened summary of a supermoon, suitable for CSV output
    :param result: dictionary, as returned by next_supermoon
    :return: dictionary
    """
    return {
        "fullmoon_local_date": result["fullmoon"]["localdate"].strftime(
            "%Y-%m-%d %H:%M %Z"
        ),
        "perigee_local_date": result["perigee"]["localdate"].strftime(
            "%Y-%m-%d %H:%M %Z"
        ),
        "perigee_distance_km": int(result["perigee"]["distance"]),
        "perigee_distance_mi": round(result["perigee"]["distance"] * KM_TO_MI),
        "angular_diameter": result["angular diameter raw"],
    }


def write_csv(results, filename="supermoons.csv"):
    """
    write supermoons to a CSV file
    :param results: list of dictionaries, as returned by next_supermoon
    :param filename: file to write
    """
    with Path(filename).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(csv_row(result) for result in results)
