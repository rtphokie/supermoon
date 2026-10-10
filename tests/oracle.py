"""
Independent reference ("oracle") calculations used to check the supermoon package.

The package finds apsides and full moons with Skyfield's search functions
(find_minima / find_maxima / find_discrete). The oracle shares only the JPL DE421
ephemeris with it: it samples the Earth-Moon distance and the Moon's phase angle on an
hourly grid, refines each event with its own search, and evaluates each supermoon
definition from scratch rather than through the package's code.
"""

from functools import cache

import numpy as np
from skyfield import almanac

from supermoon.ephemeris import planets, timescale


def _distance_km(t):
    e = planets()
    return (e["moon"] - e["earth"]).at(t).distance().km


def _hourly(year):
    """an hourly grid from Nov 1 of the prior year through Mar 1 of the next"""
    ts = timescale()
    start = ts.utc(year - 1, 11, 1)
    hours = np.arange(0, (ts.utc(year + 1, 3, 1) - start) * 24)
    return ts.tt_jd(start.tt + hours / 24)


def _refine_extremum(jd, sign):
    """
    the extremum of distance within an hour of jd: sample each minute, then fit a
    parabola through the best sample and its neighbors
    """
    ts = timescale()
    jds = jd + np.arange(-60, 61) / 1440
    d = _distance_km(ts.tt_jd(jds))
    i = int(np.argmin(sign * d))
    y0, y1, y2 = d[i - 1], d[i], d[i + 1]
    offset = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)  # in minutes, from jds[i]
    t = ts.tt_jd(jds[i] + offset / 1440)
    return t.utc_datetime(), float(_distance_km(t))


@cache
def apsides(year):
    """perigees and apogees from Nov 1 of the prior year through Mar 1 of the next"""
    t = _hourly(year)
    d = _distance_km(t)
    result = []
    for sign in (1, -1):  # minima (perigees), then maxima (apogees)
        s = sign * d
        idx = np.flatnonzero((s[1:-1] < s[:-2]) & (s[1:-1] <= s[2:])) + 1
        result.append([_refine_extremum(t.tt[i], sign) for i in idx])
    return tuple(result)


@cache
def full_moons(year):
    """(datetime, distance km) of every full moon in the calendar year (UTC)"""
    ts = timescale()
    eph = planets()

    def past_full(jd):
        """degrees past full; negative while waxing toward full"""
        return almanac.moon_phase(eph, ts.tt_jd(jd)).degrees % 360 - 180

    t = _hourly(year)
    phase = past_full(t.tt)
    results = []
    for i in np.flatnonzero((phase[:-1] < 0) & (phase[1:] >= 0)):
        lo, hi = t.tt[i], t.tt[i + 1]
        while (hi - lo) * 86400 > 0.01:  # bisect to 10 ms
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if past_full(mid) < 0 else (lo, mid)
        tt = ts.tt_jd((lo + hi) / 2)
        if tt.utc_datetime().year == year:
            results.append((tt.utc_datetime(), float(_distance_km(tt))))
    return results


def evaluate(year):
    """
    every full moon of the year, with its perigee and each definition evaluated
    :return: list of dictionaries, in date order
    """
    perigees, apogees = apsides(year)

    def in_year(events):
        return [d for dt, d in events if dt.year == year]

    min_perigee, max_apogee = min(in_year(perigees)), max(in_year(apogees))

    results = []
    for fm_date, fm_dist in full_moons(year):
        p_date, p_dist = min(perigees, key=lambda p: abs(p[0] - fm_date))
        a_dist = next(d for dt, d in apogees if dt > p_date)
        results.append(
            {
                "fullmoon": (fm_date, fm_dist),
                "perigee": (p_date, p_dist),
                "definitions": {
                    "Sky & Telescope": fm_dist <= 358884,
                    "Time & Date": fm_dist <= 360000,
                    "Espenak": (a_dist - fm_dist) / (a_dist - p_dist) >= 0.9,
                    "Nolle": (max_apogee - fm_dist) / (max_apogee - min_perigee) >= 0.9,
                    "within 1 day of perigee": abs((p_date - fm_date).total_seconds())
                    <= 86400,
                },
            }
        )
    return results


def expected_supermoons(year):
    return [r for r in evaluate(year) if any(r["definitions"].values())]
