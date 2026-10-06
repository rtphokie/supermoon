"""
apsis and lunarphases checked against the independent reference in oracle.py
"""

from datetime import datetime, timedelta, timezone

import pytest
from oracle import apsides, full_moons

from supermoon import apsis, lunarphases


def utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


def _sweep(year, step_days=3):
    start = utc(year, 1, 1)
    while start.year == year:
        yield start
        start += timedelta(days=step_days)


@pytest.mark.parametrize(
    "func, which",
    [(apsis.next_perigee, 0), (apsis.next_apogee, 1)],
    ids=["perigee", "apogee"],
)
@pytest.mark.parametrize("year", [2020, 2025])
def test_next_apsis_is_the_next_one(func, which, year):
    events = apsides(year)[which]
    wrong = []
    for start in _sweep(year):
        expected, expected_d = next((dt, d) for dt, d in events if dt >= start)
        actual, actual_d = func(start)
        if (
            abs((actual - expected).total_seconds()) > 60
            or abs(actual_d - expected_d) > 1
        ):
            wrong.append(
                f"from {start:%Y-%m-%d}: got {actual:%Y-%m-%d %H:%M}, expected {expected:%Y-%m-%d %H:%M}"
            )
    assert not wrong, "\n".join(wrong)


def test_perigee_closer_than_apogee():
    p_dt, p_d = apsis.next_perigee(utc(2025, 1, 1))
    a_dt, a_d = apsis.next_apogee(p_dt)
    assert 356000 < p_d < 370500
    assert 404000 < a_d < 406800
    assert timedelta(days=12) < a_dt - p_dt < timedelta(days=17)


def test_invalid_extrema():
    with pytest.raises(ValueError):
        apsis.next_apsis(dt=utc(2025, 1, 1), extrema="mid")


@pytest.mark.parametrize("year", [2020, 2025])
def test_full_moons_match_reference(year):
    expected = full_moons(year)
    actual = lunarphases.phases(utc(year, 1, 1), days=365 + (year % 4 == 0), phases=[2])
    assert len(actual) == len(expected)
    for (exp_dt, exp_d), act in zip(expected, actual):
        assert abs((act["dt"] - exp_dt).total_seconds()) <= 1
        assert act["d"] == pytest.approx(exp_d, abs=0.1)
        assert act["phase_name"] == "Full Moon"


def test_phases_in_order():
    data = lunarphases.phases(utc(2019, 1, 1), days=30)
    # Jan 2019: last quarter (Dec 29) was before the start; new Jan 6, first quarter Jan 14,
    # full Jan 21, last quarter Jan 27
    assert [p["phase_code"] for p in data] == [0, 1, 2, 3]
    assert [p["dt"].day for p in data] == [6, 14, 21, 27]


def test_new_and_full_moons_in_a_year():
    data = lunarphases.phases(utc(2019, 1, 1), days=365, phases=[0, 2])
    assert {p["phase_code"] for p in data} == {0, 2}
    assert len(data) == 25  # 13 new moons and 12 full moons in 2019


def test_angular_diameter():
    _, d, diameter = lunarphases.next_full_moon(utc(2025, 11, 1))
    # the Moon's apparent diameter ranges from about 29.4' at apogee to 34.1' at perigee
    assert 29.3 < diameter.arcminutes() < 34.2
    assert d < 360000 and diameter.arcminutes() > 33
