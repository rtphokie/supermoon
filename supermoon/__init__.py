"""Top-level package for supermoon"""
name = "supermoon"
__author__ = """Tony Rice"""
__email__ = 'tony@rtphokie.org'
__version__ = '0.1.0'

import supermoon.apsis
from supermoon.lunarphases import phases
from datetime import datetime, tzinfo
from skyfield.api import utc
from pprint import pprint
import pytz
import logging

  # * Richard Nole - A full or new Moon occurring at a distance 90% or greater of the closest perigee for the calendar year.  This definition is also [preferred by EarthSky.com](https://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle)
  # * Fred Espenak - A full or new  Moon occurring at a distance 90% or greater of perigee during the current lunation.
  # * Sky and Telescope magazine  -  A full Moon within 223,000 miles (358,884 km) of Earth
  # * TimeandDate.com  - A full Moon within 360,000 kilometres (223,694 mi) of Earth


def blackmoon(years=200, now=datetime.now()):
    g.date = ephem.next_full_moon(now.year-(years/2))
    prevmo = None
    prevbm = None
    results = []

    for i in range(12*years):  #compute for next
        m.compute(g)
        dist = m.earth_distance
        g.date = ephem.next_new_moon(g.date)
        lt = ephem.localtime(g.date)
        if lt.month == prevmo:
            dts = lt.strftime("%c")
            deltamo = ''
            if prevbm is not None:
                delta = lt - prevbm
                deltamo = (round(delta.days/365,1))
                # print (f"{dts} {deltamo}")
                results.append({'dateobj': lt,
                                'date': lt.strftime("%c"),
                                'delta': delta.days,
                                'delta_years': round(delta.days/365,1) } )
            prevbm = lt
        prevmo = lt.month
        # print (lt.month)
    return results

def _supermoonrule(d, maxd):
    return d <= maxd

def _timeanddate(d):
    '''
    TimeandDate.com defines a supermoon as any full moon within  360,000 km (223,694 miles)
    :param d: distance of full moon in kilometers
    :return: boolean
    '''
    return _supermoonrule(d, 360000)

def next_supermoon(dt=None):
    if dt is None:
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=utc)
    jan1 = dt.replace(month=1,day=1,hour=0,minute=0)

    next_full_moon_date, next_full_moon_distance = lunarphases.next_full_moon(dt)
    #find distance of next perigee for Espenak definition
    next_perigee_date, next_perigee_distance = apsis.next_perigee(dt)
    #find closest perigee of the year for Nolle definition
    min_perigee_date, min_perigee_distance = apsis.next_perigee(jan1, days=366)

    results = {'nolle':  _supermoonrule(next_full_moon_distance, min_perigee_distance),
               'skyandtelescope': _supermoonrule(next_full_moon_distance, 358884),
               'timeanddate': _supermoonrule(next_full_moon_distance, 360000),
               'espenek': _supermoonrule(next_full_moon_distance, next_perigee_distance),
               'fullmoon': {'date': next_full_moon_date,
                            'distance': next_full_moon_distance},
               'perigee': {'date': next_perigee_date,
                            'distance': next_perigee_distance},
               }


    return (results)

