#!/usr/bin/env python3
'''
In general, a supermoon is a full moon which occurs near the closest point in its orbit making it appear
bigger and brighter. However, there is no official nor even consistent definition for the concept of 
supermoon leading to disagreements on which full moons should receive the label and which should not.

Known definitions are calculated here
  * Richard Nole 
      rule 1 (1979) - A full or new Moon occurring at a distance 90% or greater than the perigee in a given orbit
                      Dell Horoscope, 1979
      rule 2 (2000) - A full or new Moon occurring at a distance 90% or greater than mean perigee (
                      https://www.astropro.com/features/articles/supermoon/
      rule 3 (2011) - A full or new Moon occurring at a distance 90% or greater than the closest perigee for the calendar year.  This definition is also [preferred by EarthSky.com](https://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle)
                      https://www.astropro.com/features/tables/cen21ce/suprmoon.html
  * EarthSky - A full or new Moon occuring at a distance 90% percent (or greater) of the moon’s closest approach to Earth” by the year’s closest perigee and farthest apogee" this is an interpretation of Nolle's 3rd version, 
    http://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle
  * Fred Espenak - A full or new  Moon occurring at a distance 90% or greater of perigee during the current lunation.
    http://astropixels.com/ephemeris/moon/fullperigee2001.html
  * Sky and Telescope magazine  -  A full Moon within 223,000 miles (358,884 km) of Earth
  * TimeandDate.com  - A full Moon within 360,000 kilometres (223,694 mi) of Earth
    https://www.timeanddate.com/astronomy/moon/super-full-moon.html, https://www.timeanddate.com/moon/phases/
'''
from lunarphases import next_full_moon
from apsis import next_perigee, next_apogee
from datetime import datetime, tzinfo, timedelta
from skyfield.api import utc
from tzlocal import get_localzone
import sys
import simple_cache
import argparse

@simple_cache.cache_it(filename=".supermoon.cache", ttl=12000)
def next_supermoon(dt=None):
    '''
    calculates when the next supermoon will occur based on known criteria
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :return: dictionary
    '''
    if dt is None:
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=utc)
    jan1 = dt.replace(month=1,day=1,hour=0,minute=0)

    # find datetime and distance of next full moon from the date given
    DATEfm, Dfm = next_full_moon(dt)

    # find distance of next perigee and apogee (for Espenak definition)
    DATEp, Dp = next_perigee(dt)
    DATEa, Da = next_apogee(DATEp)
    RelativeDistance_thisorbit = (Da - Dfm) / (Da - Dp)

    # find closest perigee and furthest apogee of the year for (Nolle definition)
    min_perigee_this_year_date, MinDp = next_perigee(jan1, days=366)
    max_apogee_this_year_date, MaxDa = next_apogee(jan1, days=366)
    RelativeDistance_thisyear = (MaxDa - Dfm) / (MaxDa - MinDp)

    #time seperation between perigee and full moon (for within 24 hours definition)
    perigeedelta = abs((DATEp - DATEfm).total_seconds())

    results = {'definitions': {   'EarthSky': Dfm <= 361885,
                           'Sky & Telescope': Dfm <= 358884,
                               'Time & Date': Dfm <= 360000,
                                   'Espenak': RelativeDistance_thisorbit >= 0.9,
                                     'Nolle': RelativeDistance_thisyear >= 0.9,
                   'within 1 day of perigee': perigeedelta <= 86400.0,},
               'relative distance': {'thisorbit': RelativeDistance_thisorbit,
                                     'thisyear': RelativeDistance_thisyear,},
               'fullmoon': {'date': DATEfm, 'localdate': DATEfm.astimezone(get_localzone())},
               'perigee': {'date': DATEp, 'localdate': DATEp.astimezone(get_localzone()), 'distance': Dp},
               'full perigee delta seconds': perigeedelta,
               'full perigee delta hours': perigeedelta/60/60,
              }

    if not any(results['definitions'].values()):
        results = next_supermoon(dt=dt+timedelta(days=29))

    return (results)

def yearly_supermoons(year):
    jan1 = dt.datetime(year=year,month=1,day=1,hour=0,minute=0,tzinfo=utc)
    result = next_supermoon(dt=jan1)
    msgstr = f"{result['fullmoon']['localdate'].strftime('%a %b %d %Y %I:%M %p %Z')} ({result['fullmoon']['date'].strftime('%H:%M %Z')})"
    print (f"The next supermoon will occur on {msgstr}" )
    print("The next 8 supermoons are")
    # dt = result['fullmoon']['date']
    for i in range(0,12):
        result = next_supermoon(dt=result['fullmoon']['date']+timedelta(days=1))
        if result['fullmoon']['localdate'].year > year:
            continue
        msgstr = f"{result['fullmoon']['localdate'].strftime('%a %m %d %Y %I:%M %p %Z')} ({result['fullmoon']['date'].strftime('%H:%M %Z')})"
        thelist = []
        for definition, meets in result['definitions'].items():
            if meets:
               thelist.append(definition)
        if len(thelist) == len(result['definitions'].values()):
            thelist = ['all known definitions']
        elif len(thelist) > 1:
            thelist.insert(-1, 'and')
        print (f"  {msgstr} according to {', '.join(thelist)}")

def main(dt,moons=1, year=None):
    for i in range(1,moons+1):
        result = next_supermoon(dt=dt)
        if year is not None and result['fullmoon']['date'].year != year:
            break
        msgstr = f"{result['fullmoon']['localdate'].strftime('%a %m/%d/%Y %I:%M %p %Z')} ({result['fullmoon']['date'].strftime('%H:%M %Z')})"
        thelist = []
        for definition, meets in result['definitions'].items():
            if meets:
               thelist.append(definition)
        if len(thelist) == len(result['definitions'].values()):
            thelist = ['all known definitions']
        elif len(thelist) > 1:
            thelist.insert(-1, 'and')
        print (f"  {msgstr} according to {', '.join(thelist)}")
        dt = result['fullmoon']['date']+timedelta(days=29)

if __name__ == '__main__':
    helpmsg = '''
Supermoon definitions used:
* Richard Nole (coined the term in 1979): A full or new Moon occurring at a 
  distance 90% or greater than the closest perigee for the calendar year.
  https://www.astropro.com/features/tables/cen21ce/suprmoon.html
* Fred Espenak (retired NASA astrophysicist, best known for lunar and solar 
  eclipse predictions)- A full Moon occurring at a distance 90% or greater 
  of perigee during the current lunation.
  http://astropixels.com/ephemeris/moon/fullperigee2001.html
* EarthSky (astronomy radio series/blog) - A full Moon occurring within 361,885 km
  http://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle
* Sky and Telescope magazine - A full Moon occurring within 223,000 miles (358,884 km)
* TimeandDate.com (Norwegian company offering website and data services on 
  time and astronomy)- A full Moon within 360,000 kilometres (223,694 mi) 
  https://www.timeanddate.com/astronomy/moon/super-full-moon.html
    
    '''
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     epilog=helpmsg)
    parser.add_argument('year', type=int, nargs='?', default=None, help='find supermoons for this year (optional)')
    parser.add_argument('--cnt', type=int, default=1, help='moons to show')
    args = parser.parse_args()

    if args.year is None:
        if args.cnt < 1:
            print (f"expecting count of 1 or more, got {args.cnt}")
            sys.exit(1)
        elif args.cnt > 1:
            print (f"The next {args.cnt} supermoons will be:")
        else:
            print("The next supermoon will be:")
        main(dt=None, moons=args.cnt)
    else:
        if 1900 <= args.year <= 2050:
            print (f"Supermoons during {args.year}:")
            jan1 = datetime(year=args.year, month=1, day=1, hour=0, minute=0, tzinfo=utc)
            main(dt=jan1, moons=13, year=args.year)
        else:
            print (f"Please provide a year between 1900 and 2050, got {args.year} (per JPL DE421) ")
            sys.exit(1)
