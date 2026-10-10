"""
supermoons() and friends checked against the independent reference in oracle.py
"""

from datetime import UTC, datetime, timedelta

import pytest
from oracle import evaluate, expected_supermoons

from supermoon import next_supermoon, next_supermoons, supermoons
from supermoon.core import MAX_YEAR, MIN_YEAR

YEARS = list(range(2010, 2036))


def utc(*args):
    return datetime(*args, tzinfo=UTC)


def same_instant(a, b):
    """event searches started from different dates agree to well under a second"""
    return abs((a - b).total_seconds()) < 1


@pytest.mark.parametrize("year", YEARS)
def test_matches_reference(year):
    expected = expected_supermoons(year)
    actual = supermoons(year)

    assert [r["fullmoon"][0].date() for r in expected] == [
        r["fullmoon"]["date"].date() for r in actual
    ]
    for exp, act in zip(expected, actual, strict=True):
        fm_date, fm_dist = exp["fullmoon"]
        p_date, p_dist = exp["perigee"]
        label = fm_date.date().isoformat()
        assert abs((act["fullmoon"]["date"] - fm_date).total_seconds()) <= 60, label
        assert act["fullmoon"]["distance"] == pytest.approx(fm_dist, abs=1), label
        assert abs((act["perigee"]["date"] - p_date).total_seconds()) <= 60, label
        assert act["perigee"]["distance"] == pytest.approx(p_dist, abs=1), label
        assert act["definitions"] == exp["definitions"], label


@pytest.mark.parametrize("year", [2020, 2025])
def test_every_full_moon_is_classified(year):
    """full moons left out of supermoons() are exactly those meeting no definition"""
    found = {r["fullmoon"]["date"].date() for r in supermoons(year)}
    for r in evaluate(year):
        assert (r["fullmoon"][0].date() in found) == any(r["definitions"].values())


@pytest.mark.parametrize("year", [2020, 2025])
def test_definitions_agree_with_reported_values(year):
    for r in supermoons(year):
        d = r["fullmoon"]["distance"]
        assert any(r["definitions"].values())
        assert r["definitions"]["Sky & Telescope"] == (d <= 358884)
        assert r["definitions"]["Time & Date"] == (d <= 360000)
        assert r["definitions"]["Espenak"] == (
            r["relative distance"]["thisorbit"] >= 0.9
        )
        assert r["definitions"]["Nolle"] == (r["relative distance"]["thisyear"] >= 0.9)
        assert r["definitions"]["within 1 day of perigee"] == (
            r["full perigee delta hours"] <= 24
        )
        # Sky & Telescope's threshold is stricter than Time & Date's
        if r["definitions"]["Sky & Telescope"]:
            assert r["definitions"]["Time & Date"]


@pytest.mark.parametrize("year", [MIN_YEAR, MAX_YEAR])
def test_ephemeris_limits(year):
    results = supermoons(year)
    assert 2 <= len(results) <= 8
    assert all(r["fullmoon"]["date"].year == year for r in results)


@pytest.mark.parametrize("year", [MIN_YEAR - 1, MAX_YEAR + 1])
def test_out_of_range(year):
    with pytest.raises(ValueError, match="year must be between"):
        supermoons(year)


def test_next_supermoon_is_first_on_or_after_date():
    start = utc(2025, 1, 1)
    first = next_supermoon(dt=start)
    assert same_instant(
        first["fullmoon"]["date"], supermoons(2025)[0]["fullmoon"]["date"]
    )
    # starting just after a supermoon moves on to the next one
    following = next_supermoon(dt=first["fullmoon"]["date"] + timedelta(minutes=1))
    assert same_instant(
        following["fullmoon"]["date"], supermoons(2025)[1]["fullmoon"]["date"]
    )


def test_next_supermoon_naive_datetime_is_utc():
    naive = next_supermoon(dt=datetime(2025, 1, 1))
    aware = next_supermoon(dt=utc(2025, 1, 1))
    assert same_instant(naive["fullmoon"]["date"], aware["fullmoon"]["date"])


def test_next_supermoon_defaults_to_now():
    result = next_supermoon()
    now = datetime.now(UTC)
    assert (
        now - timedelta(days=1) < result["fullmoon"]["date"] < now + timedelta(days=800)
    )


def test_next_supermoons_spans_years():
    expected = supermoons(2024) + supermoons(2025)
    results = next_supermoons(count=len(expected), dt=utc(2024, 1, 1))
    assert len(results) == len(expected)
    for r, e in zip(results, expected, strict=True):
        assert same_instant(r["fullmoon"]["date"], e["fullmoon"]["date"])


def test_localdate_is_same_instant():
    for r in supermoons(2025):
        assert r["fullmoon"]["localdate"] == r["fullmoon"]["date"]
        assert r["perigee"]["localdate"] == r["perigee"]["date"]
        assert r["fullmoon"]["localdate"].tzinfo is not None
