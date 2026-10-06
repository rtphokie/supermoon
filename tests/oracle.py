"""
Independent reference ("oracle") calculations used to check the supermoon package.

The package finds apsides with its own coarse-to-fine grid search. The oracle instead
uses Skyfield's root-finding search (find_minima / find_maxima / find_discrete) directly
on the Earth-Moon distance, sharing only the JPL DE421 ephemeris with the code under test.
"""

from functools import lru_cache

from skyfield import almanac
from skyfield.searchlib import find_maxima, find_minima

from supermoon.ephemeris import planets, timescale


def _distance_km(t):
    e = planets()
    return (e["moon"] - e["earth"]).at(t).distance().km


_distance_km.step_days = 1.0


@lru_cache(maxsize=None)
def apsides(year):
    """perigees and apogees from Nov 1 of the prior year through Mar 1 of the next"""
    ts = timescale()
    t0, t1 = ts.utc(year - 1, 11, 1), ts.utc(year + 1, 3, 1)
    tp, dp = find_minima(t0, t1, _distance_km)
    ta, da = find_maxima(t0, t1, _distance_km)
    perigees = [(t.utc_datetime(), float(d)) for t, d in zip(tp, dp)]
    apogees = [(t.utc_datetime(), float(d)) for t, d in zip(ta, da)]
    return perigees, apogees


@lru_cache(maxsize=None)
def full_moons(year):
    """(datetime, distance km) of every full moon in the calendar year (UTC)"""
    ts = timescale()
    t, phase = almanac.find_discrete(
        ts.utc(year, 1, 1), ts.utc(year + 1, 1, 1), almanac.moon_phases(planets())
    )
    return [
        (tt.utc_datetime(), float(_distance_km(tt)))
        for tt, p in zip(t, phase)
        if p == 2
    ]


def evaluate(year):
    """
    every full moon of the year, with its perigee and each supermoon definition evaluated
    :return: list of dictionaries, in date order
    """
    perigees, apogees = apsides(year)
    in_year = lambda events: [d for dt, d in events if dt.year == year]
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
