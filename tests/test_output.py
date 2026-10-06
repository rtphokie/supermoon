"""
describe(), CSV output and the command line interface
"""

import csv
import subprocess
import sys
from datetime import datetime, timezone

import pytest

from supermoon import describe, next_supermoon, supermoons, write_csv
from supermoon.cli import main
from supermoon.core import CSV_FIELDS


def utc(*args):
    return datetime(*args, tzinfo=timezone.utc)


@pytest.fixture
def nov2016():
    return next_supermoon(dt=utc(2016, 11, 1))


def with_definitions(result, *names):
    result = dict(result)
    result["definitions"] = {k: k in names for k in result["definitions"]}
    return result


def test_describe_all_definitions(nov2016):
    lines = describe(nov2016)
    assert len(lines) == 1
    assert lines[0].endswith("according to all known definitions")
    assert "(13:52 UTC)" in lines[0]


@pytest.mark.parametrize(
    "names, expected",
    [
        (["Nolle"], "according to Nolle"),
        (["Espenak", "Nolle"], "according to Espenak and Nolle"),
        (
            ["Time & Date", "Espenak", "Nolle"],
            "according to Time & Date, Espenak, and Nolle",
        ),
    ],
)
def test_describe_lists_definitions(nov2016, names, expected):
    line = describe(with_definitions(nov2016, *names))[0]
    assert line.endswith(expected)


def test_describe_options(nov2016):
    lines = describe(nov2016, perigee=True, distance=True, angulardiameter=True)
    assert len(lines) == 3
    assert "356,520.2 km (221,531.3 mi)" in lines[0]
    assert lines[1].startswith("   angular diameter:")
    assert "perigee:" in lines[2]
    assert "(2.51 hours from full moon)" in lines[2]
    assert "356,509.0 km" in lines[2]


def test_write_csv(tmp_path):
    results = supermoons(2025)
    path = tmp_path / "out.csv"
    write_csv(results, str(path))
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(results)
    assert tuple(rows[0].keys()) == CSV_FIELDS
    for row, r in zip(rows, results):
        assert int(row["perigee_distance_km"]) == int(r["perigee"]["distance"])
        assert int(row["perigee_distance_mi"]) == round(
            r["perigee"]["distance"] * 0.621371
        )
        assert row["fullmoon_local_date"].startswith(
            r["fullmoon"]["localdate"].strftime("%Y-%m-%d %H:%M")
        )
        assert float(row["angular_diameter"]) == pytest.approx(
            r["angular diameter raw"]
        )


def test_cli_year(capsys):
    assert main(["2025"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == f"{len(supermoons(2025))} supermoons during 2025:"
    assert len(out) == 1 + len(supermoons(2025))


def test_cli_year_range_brief(capsys):
    assert main(["2024", "2025", "-B"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out == [
        f"{len(supermoons(2024))} supermoons during 2024:",
        f"{len(supermoons(2025))} supermoons during 2025:",
    ]


def test_cli_csv(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["2025", "-B", "--csv"]) == 0
    assert (
        f"Wrote {len(supermoons(2025))} rows to supermoons.csv"
        in capsys.readouterr().out
    )
    assert (tmp_path / "supermoons.csv").exists()


def test_cli_next(capsys):
    assert main(["--cnt", "2"]) == 0
    out = capsys.readouterr().out.splitlines()
    assert out[0] == "The next 2 supermoons will be:"
    assert len(out) == 3


@pytest.mark.parametrize(
    "argv", [["1899"], ["2025", "2051"], ["--cnt", "0"], ["notayear"]]
)
def test_cli_rejects_bad_input(argv):
    with pytest.raises(SystemExit) as exc:
        main(argv)
    assert exc.value.code == 2


def test_python_dash_m():
    proc = subprocess.run(
        [sys.executable, "-m", "supermoon", "2025", "-B"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert proc.stdout.startswith(f"{len(supermoons(2025))} supermoons during 2025:")
