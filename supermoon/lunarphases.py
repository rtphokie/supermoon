from datetime import timedelta

import numpy as np
from skyfield import almanac
from skyfield.api import Angle

from .ephemeris import planets, timescale


def phases(dt, days=30, phases=range(4)):
    """
    lunar phases in the days following dt
    :param dt: datetime to begin search
    :param days: days to search, defaults to 30 to encompass a full lunation
    :param phases: 0=new, 1=first quarter, 2=full, 3=last quarter
    :return: list of dictionaries in date order, where dt is the datetime (UTC),
             d is distance in km, phase_name is the title of the phase and
             phase_code is the integer representing the phase
    """
    e = planets()
    earth, moon = e["earth"], e["moon"]
    ts = timescale()
    t0 = ts.utc(dt)
    t1 = ts.utc(t0.utc_datetime() + timedelta(days=days))
    t, y = almanac.find_discrete(t0, t1, almanac.moon_phases(e))
    positions = (moon - earth).at(t)

    results = []
    for dd, phase_code, pos in zip(t, y, positions, strict=True):
        if phase_code in phases:
            results.append(
                {
                    "dt": dd.utc_datetime(),
                    "d": round(pos.distance().km, 1),
                    "dd": dd,
                    "phase_code": phase_code,
                    "phase_name": almanac.MOON_PHASES[phase_code],
                }
            )
    return results


def next_full_moon(dt):
    """
    the first full moon after dt
    :param dt: datetime to begin search
    :return: datetime (UTC), distance in km (geometric, Earth center to Moon center)
             and apparent angular diameter as a Skyfield Angle
    """
    r_moon = 1737.1  # in km

    result = phases(dt, days=30, phases=[2])[0]
    diameter = Angle(radians=np.arcsin(r_moon / result["d"]) * 2.0)
    return result["dt"], result["d"], diameter
