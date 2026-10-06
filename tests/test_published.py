"""
Checks against published values, independent of Skyfield.

Full moon times: US Naval Observatory phases of the Moon.
Perigees: Fred Espenak, astropixels.com "Moon at Perigee and Apogee" tables (1 minute / 1 km precision).
"""

from datetime import datetime, timedelta, timezone

import pytest

from supermoon import next_supermoon
from supermoon.lunarphases import next_full_moon


def utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


FULL_MOONS = [
    utc(2016, 11, 14, 13, 52),
    utc(2018, 1, 31, 13, 27),
    utc(2019, 2, 19, 15, 54),
    utc(2020, 4, 8, 2, 35),
    utc(2025, 11, 5, 13, 19),
]

# (full moon, perigee time, perigee distance km)
PERIGEES = [
    (utc(2016, 11, 14, 13, 52), utc(2016, 11, 14, 11, 23), 356509),
    (utc(2018, 1, 31, 13, 27), utc(2018, 1, 30, 9, 54), 358995),
    (utc(2019, 2, 19, 15, 54), utc(2019, 2, 19, 9, 6), 356761),
    (utc(2020, 4, 8, 2, 35), utc(2020, 4, 7, 18, 8), 356907),
]


@pytest.mark.parametrize("expected", FULL_MOONS, ids=lambda d: d.date().isoformat())
def test_full_moon_time(expected):
    dt, _, _ = next_full_moon(expected - timedelta(days=2))
    assert abs((dt - expected).total_seconds()) <= 60


@pytest.mark.parametrize(
    "fullmoon, perigee, distance",
    PERIGEES,
    ids=[p[0].date().isoformat() for p in PERIGEES],
)
def test_perigee_of_supermoon(fullmoon, perigee, distance):
    result = next_supermoon(dt=fullmoon - timedelta(days=2))
    assert abs((result["fullmoon"]["date"] - fullmoon).total_seconds()) <= 60
    # Espenak's times come from Meeus' series, which differ from DE421 by a few minutes
    assert abs((result["perigee"]["date"] - perigee).total_seconds()) <= 5 * 60
    assert abs(result["perigee"]["distance"] - distance) <= 2


def test_2016_11_14_meets_all_definitions():
    """the closest full moon since 1948, 2.5 hours from perigee"""
    result = next_supermoon(dt=utc(2016, 11, 1))
    assert result["fullmoon"]["date"].date() == utc(2016, 11, 14).date()
    assert all(result["definitions"].values())
