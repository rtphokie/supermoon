from skyfield import almanac
from skyfield.api import Loader
from datetime import datetime, timedelta, date
from skyfield.api import Loader, Topos
from supermoon import apsis
import pytz
from pprint import pprint

load = Loader('~/Documents/data')
e = load('de421.bsp')
ts = load.timescale()
earth = e['earth']
moon = e['moon']


def phases(dt, days=30, phases=range(0,5)):
    '''

    :param dt: datetime to begin search
    :param days: days to search, defaults to 30 to encompass a full lunation
    :param phases: 0=new, 1=first quarter, 2=full, 3=last quarter
    :return: dictionary (key is the datetime of the event), of dictionaries where
             d is distance in km, phase_name is the title of the phase, phase_code is the integer representing the phase
    '''
    t0 = ts.utc(dt)
    t1 = ts.utc(t0.utc_datetime() + timedelta(days=days))
    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(e))
    positions = (moon - earth).at(t)

    results = []
    for dd, phase_code, pos in zip(t, y, positions):
        if phase_code in phases:
            results.append({'dt': dd.utc_datetime(),
                             'd': round(pos.distance().km,1),
                    'phase_code': phase_code,
                    'phase_name': almanac.MOON_PHASES[phase_code]})
    return results

def next_full_moon(dt):
    '''

    :param dt: datetime to begin search
    :return:
    '''
    result = phases(dt, days=30, phases=[2])[0]
    return result['dt'], result['d']

