'''
In general, a supermoon is a full moon which occurs near the closest point in its orbit making it appear
bigger and brighter. However, there is no official nor even consistent definition for the concept of
supermoon leading to disagreements on which full moons should receive the label and which should not.

Known definitions are calculated here
  * Richard Nolle
      rule 1 (1979) - A full or new Moon occurring at a distance 90% or greater than the perigee in a given orbit
                      Dell Horoscope, 1979
      rule 2 (2000) - A full or new Moon occurring at a distance 90% or greater than mean perigee (
                      https://www.astropro.com/features/articles/supermoon/
      rule 3 (2011) - A full or new Moon occurring at a distance 90% or greater than the closest perigee for the calendar year.  This definition is also [preferred by EarthSky.com](https://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle)
                      https://www.astropro.com/features/tables/cen21ce/suprmoon.html
  * Fred Espenak - A full or new  Moon occurring at a distance 90% or greater of perigee during the current lunation, also used by Earth Sky
    http://astropixels.com/ephemeris/moon/fullperigee2001.html
  * Sky and Telescope magazine  -  A full Moon within 223,000 miles (358,884 km) of Earth
  * TimeandDate.com  - A full Moon within 360,000 kilometres (223,694 mi) of Earth
    https://www.timeanddate.com/astronomy/moon/super-full-moon.html, https://www.timeanddate.com/moon/phases/
'''
from .lunarphases import next_full_moon
from .apsis import next_perigee, next_apogee
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from tzlocal import get_localzone

# range covered by the JPL DE421 ephemeris
MIN_YEAR = 1900
MAX_YEAR = 2050


def next_supermoon(dt=None):
    '''
    calculates when the next supermoon will occur based on known criteria
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :return: dictionary
    '''
    if dt is None:
        dt = datetime.now(timezone.utc)
    elif dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    result = _full_moon(dt)
    while not any(result['definitions'].values()):
        result = _full_moon(result['fullmoon']['date'] + timedelta(days=1))
    return result


@lru_cache(maxsize=512)
def _full_moon(dt):
    '''
    evaluates the first full moon after dt against each supermoon definition
    '''
    # find datetime and distance of next full moon from the date given
    DATEfm, Dfm, diameter = next_full_moon(dt)
    jan1 = datetime(year=DATEfm.year, month=1, day=1, tzinfo=timezone.utc)

    # find distance of next perigee and apogee (for Espenak definition)
    DATEp, Dp = next_perigee(DATEfm - timedelta(days=14))
    DATEa, Da = next_apogee(DATEp)

    RelativeDistance_thisorbit = (Da - Dfm) / (Da - Dp)

    # find closest perigee and furthest apogee of the year for (Nolle definition)
    min_perigee_this_year_date, MinDp = next_perigee(jan1, days=366)
    max_apogee_this_year_date, MaxDa = next_apogee(jan1, days=366)
    RelativeDistance_thisyear = (MaxDa - Dfm) / (MaxDa - MinDp)

    # time seperation between perigee and full moon (for within 24 hours definition)
    perigeedelta = abs((DATEp - DATEfm).total_seconds())

    return {'definitions': {
                            'Sky & Telescope': bool(Dfm <= 358884),
                            'Time & Date': bool(Dfm <= 360000),
                            'Espenak': bool(RelativeDistance_thisorbit >= 0.9),
                            'Nolle': bool(RelativeDistance_thisyear >= 0.9),
                            'within 1 day of perigee': perigeedelta <= 86400.0, },
            'relative distance': {'thisorbit': float(RelativeDistance_thisorbit),
                                  'thisyear': float(RelativeDistance_thisyear), },
            'fullmoon': {'date': DATEfm, 'localdate': DATEfm.astimezone(get_localzone()), 'distance': float(Dfm)},
            'perigee': {'date': DATEp, 'localdate': DATEp.astimezone(get_localzone()), 'distance': float(Dp)},
            'full perigee delta seconds': perigeedelta,
            'full perigee delta hours': perigeedelta / 3600,
            'angular diameter': str(diameter),
            }


def next_supermoons(count=1, dt=None):
    '''
    the next count supermoons on or after dt
    :param count: number of supermoons to return
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :return: list of dictionaries, as returned by next_supermoon
    '''
    results = []
    for i in range(count):
        result = next_supermoon(dt=dt)
        results.append(result)
        dt = result['fullmoon']['date'] + timedelta(days=1)
    return results


def supermoons(year):
    '''
    all supermoons during a calendar year (UTC)
    :param year: year between 1900 and 2050
    :return: list of dictionaries, as returned by next_supermoon
    '''
    if not MIN_YEAR <= year <= MAX_YEAR:
        raise ValueError(f"year must be between {MIN_YEAR} and {MAX_YEAR} (per JPL DE421), got {year}")
    results = []
    dt = datetime(year=year, month=1, day=1, tzinfo=timezone.utc)
    while True:
        result = next_supermoon(dt=dt)
        if result['fullmoon']['date'].year != year:
            break
        results.append(result)
        dt = result['fullmoon']['date'] + timedelta(days=1)
    return results


def describe(result, perigee=False, distance=False, angulardiameter=False):
    '''
    human readable description of a supermoon
    :param result: dictionary, as returned by next_supermoon
    :return: list of lines
    '''
    lines = []
    msgstr = f"{result['fullmoon']['localdate'].strftime('%a %m/%d/%Y %I:%M %p %Z')} ({result['fullmoon']['date'].strftime('%H:%M %Z')})"
    if distance:
        msgstr += f" {result['fullmoon']['distance']:,} km ({result['fullmoon']['distance'] * 0.621371:,.1f} mi)"
    thelist = []
    for definition, meets in result['definitions'].items():
        if meets:
            thelist.append(definition)
    if len(thelist) == len(result['definitions'].values()):
        thelist = ['all known definitions']
    elif len(thelist) > 1:
        thelist.insert(-1, 'and')
    lines.append(f"  {msgstr} according to {', '.join(thelist)}")
    if angulardiameter:
        lines.append(f"   angular diameter: {result['angular diameter']}")
    if perigee:
        distmsgstr = f"   perigee: {result['perigee']['localdate'].strftime('%m/%d/%Y %H:%M %Z')} ({result['full perigee delta hours']:.2f} hours from full moon)"
        if distance:
            distmsgstr += f" {result['perigee']['distance']:,} km ({result['perigee']['distance'] * 0.621371:,.1f} mi)"
        lines.append(distmsgstr)
    return lines
