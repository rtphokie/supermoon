#!/usr/bin/env python3
"""
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
  * Fred Espenak - A full or new  Moon occurring at a distance 90% or greater of perigee during the current lunation, also used by Earth Sky
    http://astropixels.com/ephemeris/moon/fullperigee2001.html
  * Sky and Telescope magazine  -  A full Moon within 223,000 miles (358,884 km) of Earth
  * TimeandDate.com  - A full Moon within 360,000 kilometres (223,694 mi) of Earth
    https://www.timeanddate.com/astronomy/moon/super-full-moon.html, https://www.timeanddate.com/moon/phases/
"""

from lunarphases import next_full_moon
from apsis import next_perigee, next_apogee
from datetime import datetime, timedelta
from skyfield.api import utc
from tzlocal import get_localzone
import sys
import simple_cache
import argparse

import csv
from typing import List, Dict, Any


def write_dicts_to_csv(
        rows: List[Dict[str, Any]], filename: str = "supermoons.csv"
) -> None:
    """
    Write an array of dictionaries to `ofo.csv`.
    Header fields are the union of all keys in input, preserving first-seen order.
    """
    if not rows:
        # create an empty file
        open(filename, "w", newline="", encoding="utf-8").close()
        return

    # Collect fieldnames in order of first appearance
    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # ensure None becomes empty string (optional)
            safe_row = {k: ("" if v is None else v) for k, v in row.items()}
            writer.writerow(safe_row)

    print(f"Wrote {len(rows)} rows to {filename}")


@simple_cache.cache_it(filename=".supermoon.cache", ttl=12000)
def next_supermoon(dt=None):
    """
    calculates when the next supermoon will occur based on known criteria
    :param dt: timezone aware datetime, defaults to current time (UTC)
    :return: dictionary
    """
    if dt is None:
        dt = datetime.utcnow()
        dt = dt.replace(tzinfo=utc)
    jan1 = dt.replace(month=1, day=1, hour=0, minute=0)

    # find datetime and distance of next full moon from the date given
    DATEfm, Dfm, diameter = next_full_moon(dt)

    # find distance of next perigee and apogee (for Espenak definition)
    DATEp, Dp = next_perigee(DATEfm - timedelta(days=14))
    DATEa, Da = next_apogee(DATEp)

    RelativeDistance_thisorbit = (Da - Dfm) / (Da - Dp)

    # find closest perigee and furthest apogee of the year for (Nolle definition)
    min_perigee_this_year_date, MinDp = next_perigee(jan1, days=366)
    max_apogee_this_year_date, MaxDa = next_apogee(jan1, days=366)
    RelativeDistance_thisyear = (MaxDa - Dfm) / (MaxDa - MinDp)

    # time seperation between perigee and full moon (for within 24 hours definition)
    perigeedelta = abs((DATEp - DATEfm).total_seconds())

    results = {
        "definitions": {
            "Sky & Telescope": Dfm <= 358884,
            "Time & Date": Dfm <= 360000,
            "Espenak": RelativeDistance_thisorbit >= 0.9,
            "Nolle": RelativeDistance_thisyear >= 0.9,
            "within 1 day of perigee": perigeedelta <= 86400.0,
        },
        "relative distance": {
            "thisorbit": RelativeDistance_thisorbit,
            "thisyear": RelativeDistance_thisyear,
        },
        "fullmoon": {
            "date": DATEfm,
            "localdate": DATEfm.astimezone(get_localzone()),
            "distance": Dfm,
        },
        "perigee": {
            "date": DATEp,
            "localdate": DATEp.astimezone(get_localzone()),
            "distance": Dp,
        },
        "full perigee delta seconds": perigeedelta,
        "full perigee delta hours": perigeedelta / 3600,
        "angular diameter": str(diameter),
        "angular diameter raw": diameter.degrees,
    }
    if not any(results["definitions"].values()):
        results = next_supermoon(dt=dt + timedelta(days=29))
    return results


def main(
        dt,
        moons=1,
        year=None,
        perigee=False,
        distance=False,
        angulardiameter=True,
        csv=False,
):
    lines = []
    csv_rows = []
    for i in range(1, moons + 1):
        result = next_supermoon(dt=dt)
        if year is not None and result["fullmoon"]["date"].year != year:
            break
        full_datetime_local = result["fullmoon"]["localdate"].strftime(
            "%a %m/%d/%Y %I:%M %p %Z"
        )
        msgstr = (
            f"{full_datetime_local} ({result['fullmoon']['date'].strftime('%H:%M %Z')})"
        )
        if distance:
            msgstr += f" {result['fullmoon']['distance']:,} km ({result['fullmoon']['distance'] * 0.621371:,.1f} mi)"
        thelist = []
        for definition, meets in result["definitions"].items():
            if meets:
                thelist.append(definition)
        if len(thelist) == len(result["definitions"].values()):
            thelist = ["all known definitions"]
        elif len(thelist) > 1:
            thelist.insert(-1, "and")
        lines.append(f"  {msgstr} according to {', '.join(thelist)}")
        dt = result["fullmoon"]["date"] + timedelta(days=29)
        if angulardiameter:
            lines.append(f"   angular diameter: {result['angular diameter']}")
        if perigee:
            distmsgstr = f"   perigee: {result['perigee']['localdate'].strftime('%m/%d/%Y %H:%M %Z')} ({result['full perigee delta hours']:.2f} hours from full moon)"
            if distance:
                distmsgstr += f" {result['perigee']['distance']:,} km ({result['perigee']['distance'] * 0.621371:,.1f} mi)"
            lines.append(distmsgstr)
        if csv:
            csv_rows.append(
                {
                    "fullmoon_local_date": result["fullmoon"]["localdate"].strftime(
                        "%Y-%m-%d %H:%M %Z"
                    ),
                    "perigee_local_date": result["perigee"]["localdate"].strftime(
                        "%Y-%m-%d %H:%M %Z"
                    ),
                    "perigee_distance_km": int(result["perigee"]["distance"]),
                    "perigee_distance_mi": round(
                        result["perigee"]["distance"] * 0.621371
                    ),
                    "angular_diameter": result["angular diameter raw"],
                }
            )

    return lines, csv_rows


if __name__ == "__main__":
    helpmsg = """
Supermoon definitions used:
* Richard Nole (coined the term in 1979): A full or new Moon occurring at a 
  distance 90% or greater than the closest perigee for the calendar year.
  https://www.astropro.com/features/tables/cen21ce/suprmoon.html
* Fred Espenak (retired NASA astrophysicist, best known for lunar and solar 
  eclipse predictions)- A full Moon occurring at a distance 90% or greater 
  of perigee during the current lunation.
  http://astropixels.com/ephemeris/moon/fullperigee2001.html
* Sky and Telescope magazine - A full Moon occurring within 223,000 miles (358,884 km)
* TimeandDate.com (Norwegian company offering website and data services on 
  time and astronomy)- A full Moon within 360,000 kilometres (223,694 mi) 
  https://www.timeanddate.com/astronomy/moon/super-full-moon.html
    
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter, epilog=helpmsg
    )
    parser.add_argument(
        "year",
        type=int,
        nargs="?",
        default=None,
        help="find supermoons for this year (optional, defaults to current date forward)",
    )
    parser.add_argument(
        "endyear",
        type=int,
        nargs="?",
        default=None,
        help="stop finding supermoons (optional)",
    )
    parser.add_argument("--cnt", type=int, default=1, help="moons to show")
    parser.add_argument(
        "-B",
        "--brief",
        action="store_const",
        default=False,
        const=True,
        help="brief output",
    )
    parser.add_argument(
        "-P",
        "--perigee",
        action="store_const",
        default=False,
        const=True,
        help="include perigee time",
    )
    parser.add_argument(
        "-D",
        "--distance",
        action="store_const",
        default=False,
        const=True,
        help="include distances",
    )
    parser.add_argument(
        "-C",
        "--csv",
        action="store_const",
        default=False,
        const=True,
        help="output CSV format",
    )
    parser.add_argument(
        "-A",
        "--angulardiameter",
        action="store_const",
        default=True,
        const=True,
        help="include angular diameter",
    )
    args = parser.parse_args()
    if args.endyear is None and args.year is not None:
        args.endyear = args.year

    csv_rows_all_years = []

    if args.year is None:
        lines, csv_rows = main(
            dt=None,
            moons=args.cnt,
            perigee=args.perigee,
            distance=args.distance,
            angulardiameter=args.angulardiameter,
        )
        csv_rows_all_years.extend(csv_rows)
        if args.cnt < 1:
            print(f"expecting count of 1 or more, got {args.cnt}")
            print("\n".join(lines))
            sys.exit(1)
        elif args.cnt > 1:
            print(f"The next {args.cnt} supermoons will be:")
            print("\n".join(lines))
        else:
            print("The next supermoon will be:")
            print("\n".join(lines))
    elif args.year is not None:
        for year in range(args.year, args.endyear + 1):
            jan1 = datetime(year=year, month=1, day=1, hour=0, minute=0, tzinfo=utc)
            lines, csv_rows = main(
                dt=jan1,
                moons=13,
                year=year,
                perigee=args.perigee,
                distance=args.distance,
                csv=args.csv,
            )
            csv_rows_all_years.extend(csv_rows)
            if args.distance:
                cnt = len(lines) / 2
            else:
                cnt = len(lines)
            print(f"{int(cnt)} supermoons during {year}:")
            if not args.brief:
                print("\n".join(lines))

    else:
        if 1900 <= args.year <= 2050:
            print(f"Supermoons during {args.year}:")
            jan1 = datetime(
                year=args.year, month=1, day=1, hour=0, minute=0, tzinfo=utc
            )
            main(
                dt=jan1,
                moons=13,
                year=args.year,
                perigee=args.perigee,
                distance=args.distance,
                csv=args.csv,
            )
        else:
            print(
                f"Please provide a year between 1900 and 2050, got {args.year} (per JPL DE421) "
            )
            sys.exit(1)
    if args.csv:
        write_dicts_to_csv(csv_rows_all_years, filename="supermoons.csv")
    else:
        print("skipping csv output")
