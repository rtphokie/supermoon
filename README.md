# supermoon

[![PyPI](https://img.shields.io/pypi/v/supermoon)](https://pypi.org/project/supermoon/)
[![Python](https://img.shields.io/pypi/pyversions/supermoon)](https://pypi.org/project/supermoon/)
[![License: MIT](https://img.shields.io/pypi/l/supermoon)](https://github.com/rtphokie/supermoon/blob/master/LICENSE)

Finds supermoons, and shows which of the popular (and conflicting) definitions each one meets.
For background, see the [Wikipedia article on supermoons](https://en.wikipedia.org/wiki/Supermoon).

A supermoon, or perigean full moon, is a full Moon that happens near the point in the Moon's orbit
closest to Earth, so the Moon looks slightly larger. The term has no astronomical meaning. An
astrologer coined it, not an astronomer. It describes a timing coincidence in the Moon's synodic
month, and every popular definition of it is essentially arbitrary.

## Installation

Requires Python 3.11 or newer.

```
pip install supermoon
```

To install only the command line tool, in its own isolated environment:

```
pipx install supermoon      # or: uv tool install supermoon
```

The first time you run it, supermoon downloads the JPL DE421 ephemeris (about 17 MB) to
`~/.supermoon`. To keep it somewhere else, or to reuse a copy you already have, set the
`SUPERMOON_DATA` environment variable to that directory. DE421 covers the years 1900 through 2050.

## Command line usage

```
usage: supermoon [-h] [--cnt CNT] [-B] [-P] [-D] [-A] [-C] [year] [endyear]

positional arguments:
  year                  find supermoons for this year (optional, defaults to now onward)
  endyear               last year to find supermoons for (optional)

options:
  -h, --help            show this help message and exit
  --cnt CNT             moons to show (only without a year)
  -B, --brief           brief output
  -P, --perigee         include perigee time
  -D, --distance        include distances
  -A, --angulardiameter
                        include angular diameter
  -C, --csv             also write results to supermoons.csv
```

With no arguments, `supermoon` shows the next supermoon from now. Give a year to list every
supermoon in it, or two years to list every supermoon from the first through the second.
`--cnt` can only be used without a year.

Examples:

```
$ supermoon                    # the next supermoon
$ supermoon --cnt 3 -P -D -A   # the next 3, with perigee, distances and angular diameter
$ supermoon 2029               # every supermoon in 2029
$ supermoon 2020 2035 -B       # how many supermoons there are each year from 2020 to 2035
$ supermoon 2020 2035 -C       # also save them to supermoons.csv
```

Sample output:

```
$ supermoon 2025 -P -D
3 supermoons during 2025:
  Mon 10/06/2025 11:47 PM EDT (03:47 UTC) 361,456.2 km (224,598.4 mi) according to Espenak and Nolle
   perigee: 10/08/2025 08:38 EDT (32.85 hours from full moon) 359,819.0 km (223,581.1 mi)
  ...
```

Times are shown in your computer's local time zone, with UTC in parentheses.
`python -m supermoon` works the same way.

## Python usage

```python
from datetime import UTC, datetime

import supermoon

# the next supermoon on or after a date (defaults to now; naive datetimes are treated as UTC)
result = supermoon.next_supermoon(datetime(2025, 1, 1, tzinfo=UTC))
result["fullmoon"]["date"]      # datetime.datetime(2025, 10, 7, 3, 47, 36, ..., tzinfo=UTC)
result["fullmoon"]["distance"]  # km
result["definitions"]           # {'Sky & Telescope': False, 'Time & Date': False,
                                #  'Espenak': True, 'Nolle': True, 'within 1 day of perigee': False}

supermoon.supermoons(2029)              # list of every supermoon in a year (1900-2050)
supermoon.next_supermoons(count=3)      # the next 3 supermoons from now
supermoon.next_supermoons(count=3, dt=datetime(2030, 1, 1, tzinfo=UTC))

# printable lines, the same as the command line output
for line in supermoon.describe(result, perigee=True, distance=True, angulardiameter=True):
    print(line)

# save results to a CSV file
supermoon.write_csv(supermoon.supermoons(2029), "supermoons.csv")
```

To find which supermoons meet a particular definition:

```python
nolle = [r for r in supermoon.supermoons(2030) if r["definitions"]["Nolle"]]
```

`supermoons()` raises `ValueError` for a year outside 1900 through 2050.

Each result is a dictionary with these keys:

| key | contents |
|---|---|
| `definitions` | each definition's name, mapped to whether this full Moon meets it |
| `fullmoon` | `date` (UTC), `localdate` (local time zone), `distance` (km) |
| `perigee` | `date`, `localdate` and `distance` of the closest perigee |
| `relative distance` | `thisorbit` (Espenak) and `thisyear` (Nolle) ratios |
| `full perigee delta hours` / `full perigee delta seconds` | time between the full Moon and perigee |
| `angular diameter` / `angular diameter raw` | the Moon's apparent size, as a string / in degrees |

The CSV file has the columns `fullmoon_local_date`, `perigee_local_date`, `perigee_distance_km`,
`perigee_distance_mi` and `angular_diameter` (degrees).

## Definitions used

* Richard Nolle, an astrologer, coined the term in 1979 in an article in _Dell Horoscope_ magazine.
  He has refined his definition twice:
    - rule 1 (1979): a full or new Moon at a distance 90% or greater than the perigee in a given orbit
    - rule 2 (2000): a full or new Moon at a distance 90% or greater than mean perigee
      [source](https://www.astropro.com/features/articles/supermoon/)
    - rule 3 (2011): a full or new Moon at a distance 90% or greater than the closest perigee for
      the calendar year. This package calculates this rule.
      [source](https://www.astropro.com/features/tables/cen21ce/suprmoon.html)
* Fred Espenak (retired NASA astrophysicist, best known for lunar and solar eclipse predictions):
  a full Moon at a distance 90% or greater of perigee during the current lunation. EarthSky also
  [uses this definition](https://earthsky.org/astronomy-essentials/why-experts-disagree-on-what-makes-a-supermoon#nolle).
  [source](http://astropixels.com/ephemeris/moon/fullperigee2001.html)
* Sky and Telescope magazine: a full Moon within 223,000 miles (358,884 km)
  [source](https://skyandtelescope.org/observing/what-is-a-supermoon/)
* TimeandDate.com (a Norwegian company offering website and data services on time and astronomy):
  a full Moon within 360,000 kilometers (223,694 mi)
  [source](https://www.timeanddate.com/astronomy/moon/super-full-moon.html)
* Additionally, some sources have labeled full Moons within 24 hours of perigee as supermoons.

Nolle was presumably inspired by the real increase in tidal effects at a perigee
[syzygy](https://en.wikipedia.org/wiki/Syzygy_%28astronomy%29), so his tables include both new and
full Moons. Most mentions of supermoons in the popular media focus on full Moons near perigee,
because a new Moon is hard to see. This package only considers full Moons.

This collection of conflicting definitions is further described in
[this article I wrote on the subject](https://www.wral.com/weather/blogpost/11487264/).

## Supermoons, 2020 through 2035

Times are US Eastern.

```
4 supermoons during 2020:
  Sun 02/09/2020 02:33 AM EST (07:33 UTC) according to Espenak
  Mon 03/09/2020 01:47 PM EDT (17:47 UTC) according to all known definitions
  Tue 04/07/2020 10:35 PM EDT (02:35 UTC) according to all known definitions
  Thu 05/07/2020 06:45 AM EDT (10:45 UTC) according to Espenak and Nolle
4 supermoons during 2021:
  Sun 03/28/2021 02:48 PM EDT (18:48 UTC) according to Espenak
  Mon 04/26/2021 11:31 PM EDT (03:31 UTC) according to all known definitions
  Wed 05/26/2021 07:13 AM EDT (11:13 UTC) according to all known definitions
  Thu 06/24/2021 02:39 PM EDT (18:39 UTC) according to Espenak and Nolle
4 supermoons during 2022:
  Mon 05/16/2022 12:14 AM EDT (04:14 UTC) according to Espenak and Nolle
  Tue 06/14/2022 07:51 AM EDT (11:51 UTC) according to all known definitions
  Wed 07/13/2022 02:37 PM EDT (18:37 UTC) according to all known definitions
  Thu 08/11/2022 09:35 PM EDT (01:35 UTC) according to Espenak and Nolle
4 supermoons during 2023:
  Mon 07/03/2023 07:38 AM EDT (11:38 UTC) according to Espenak
  Tue 08/01/2023 02:31 PM EDT (18:31 UTC) according to all known definitions
  Wed 08/30/2023 09:35 PM EDT (01:35 UTC) according to all known definitions
  Fri 09/29/2023 05:57 AM EDT (09:57 UTC) according to Espenak and Nolle
4 supermoons during 2024:
  Mon 08/19/2024 02:25 PM EDT (18:25 UTC) according to Espenak
  Tue 09/17/2024 10:34 PM EDT (02:34 UTC) according to all known definitions
  Thu 10/17/2024 07:26 AM EDT (11:26 UTC) according to all known definitions
  Fri 11/15/2024 04:28 PM EST (21:28 UTC) according to Espenak
3 supermoons during 2025:
  Mon 10/06/2025 11:47 PM EDT (03:47 UTC) according to Espenak and Nolle
  Wed 11/05/2025 08:19 AM EST (13:19 UTC) according to all known definitions
  Thu 12/04/2025 06:14 PM EST (23:14 UTC) according to all known definitions
3 supermoons during 2026:
  Sat 01/03/2026 05:02 AM EST (10:02 UTC) according to Espenak
  Tue 11/24/2026 09:53 AM EST (14:53 UTC) according to Espenak and Nolle
  Wed 12/23/2026 08:28 PM EST (01:28 UTC) according to all known definitions
3 supermoons during 2027:
  Fri 01/22/2027 07:17 AM EST (12:17 UTC) according to all known definitions
  Sat 02/20/2027 06:23 PM EST (23:23 UTC) according to Espenak
  Mon 12/13/2027 11:08 AM EST (16:08 UTC) according to Espenak
4 supermoons during 2028:
  Tue 01/11/2028 11:03 PM EST (04:03 UTC) according to Espenak and Nolle
  Thu 02/10/2028 10:03 AM EST (15:03 UTC) according to all known definitions
  Fri 03/10/2028 08:06 PM EST (01:06 UTC) according to all known definitions
  Sun 04/09/2028 06:26 AM EDT (10:26 UTC) according to Espenak
5 supermoons during 2029:
  Tue 01/30/2029 01:03 AM EST (06:03 UTC) according to Espenak
  Wed 02/28/2029 12:10 PM EST (17:10 UTC) according to Time & Date, Espenak, and Nolle
  Thu 03/29/2029 10:26 PM EDT (02:26 UTC) according to all known definitions
  Sat 04/28/2029 06:36 AM EDT (10:36 UTC) according to all known definitions
  Sun 05/27/2029 02:37 PM EDT (18:37 UTC) according to Espenak
5 supermoons during 2030:
  Tue 03/19/2030 01:56 PM EDT (17:56 UTC) according to Espenak
  Wed 04/17/2030 11:20 PM EDT (03:20 UTC) according to Time & Date, Espenak, and Nolle
  Fri 05/17/2030 07:19 AM EDT (11:19 UTC) according to all known definitions
  Sat 06/15/2030 02:41 PM EDT (18:41 UTC) according to all known definitions
  Sun 07/14/2030 10:12 PM EDT (02:12 UTC) according to Espenak
5 supermoons during 2031:
  Tue 05/06/2031 11:39 PM EDT (03:39 UTC) according to Espenak
  Thu 06/05/2031 07:58 AM EDT (11:58 UTC) according to Time & Date, Espenak, and Nolle
  Fri 07/04/2031 03:01 PM EDT (19:01 UTC) according to all known definitions
  Sat 08/02/2031 09:45 PM EDT (01:45 UTC) according to all known definitions
  Mon 09/01/2031 05:20 AM EDT (09:20 UTC) according to Espenak
5 supermoons during 2032:
  Wed 06/23/2032 07:32 AM EDT (11:32 UTC) according to Espenak
  Thu 07/22/2032 02:51 PM EDT (18:51 UTC) according to Time & Date, Espenak, Nolle, and within 1 day of perigee
  Fri 08/20/2032 09:46 PM EDT (01:46 UTC) according to all known definitions
  Sun 09/19/2032 05:30 AM EDT (09:30 UTC) according to all known definitions
  Mon 10/18/2032 02:58 PM EDT (18:58 UTC) according to Espenak
5 supermoons during 2033:
  Wed 08/10/2033 02:07 PM EDT (18:07 UTC) according to Espenak
  Thu 09/08/2033 10:20 PM EDT (02:20 UTC) according to Time & Date, Espenak, Nolle, and within 1 day of perigee
  Sat 10/08/2033 06:58 AM EDT (10:58 UTC) according to all known definitions
  Sun 11/06/2033 03:32 PM EST (20:32 UTC) according to all known definitions
  Tue 12/06/2033 02:22 AM EST (07:22 UTC) according to Espenak
4 supermoons during 2034:
  Wed 09/27/2034 10:56 PM EDT (02:56 UTC) according to Espenak
  Fri 10/27/2034 08:42 AM EDT (12:42 UTC) according to all known definitions
  Sat 11/25/2034 05:32 PM EST (22:32 UTC) according to all known definitions
  Mon 12/25/2034 03:54 AM EST (08:54 UTC) according to Time & Date, Espenak, Nolle, and within 1 day of perigee
3 supermoons during 2035:
  Tue 01/23/2035 03:16 PM EST (20:16 UTC) according to Espenak
  Thu 11/15/2035 08:48 AM EST (13:48 UTC) according to Espenak
  Fri 12/14/2035 07:33 PM EST (00:33 UTC) according to all known definitions
```

## Development

The project uses [uv](https://docs.astral.sh/uv/):

```
uv sync --extra test
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run supermoon 2025
```

The tests check results against an independent reference calculation (`tests/oracle.py`) and
against published values from the US Naval Observatory and Fred Espenak's perigee tables. They
need the DE421 ephemeris, which is downloaded on the first run.

## Releasing to PyPI

1. Bump `__version__` in `supermoon/__init__.py`.
2. Run the tests and ruff checks above.
3. Build and check the distributions:

   ```
   rm -rf dist
   uv build
   uvx twine check dist/*
   ```

4. Optionally, try the release on [TestPyPI](https://test.pypi.org/) first:

   ```
   uv publish --publish-url https://test.pypi.org/legacy/
   ```

5. Publish, then tag the release:

   ```
   uv publish
   git tag v$(uv run python -c "import supermoon; print(supermoon.__version__)")
   git push --tags
   ```
