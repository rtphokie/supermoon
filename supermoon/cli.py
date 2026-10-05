import argparse
import sys

from .core import MAX_YEAR, MIN_YEAR, describe, next_supermoons, supermoons, write_csv

helpmsg = """
Supermoon definitions used:
* Richard Nolle (coined the term in 1979): A full or new Moon occurring at a
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


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="supermoon", formatter_class=argparse.RawTextHelpFormatter, epilog=helpmsg
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
    parser.add_argument("-B", "--brief", action="store_true", help="brief output")
    parser.add_argument(
        "-P", "--perigee", action="store_true", help="include perigee time"
    )
    parser.add_argument(
        "-D", "--distance", action="store_true", help="include distances"
    )
    parser.add_argument(
        "-A", "--angulardiameter", action="store_true", help="include angular diameter"
    )
    parser.add_argument(
        "-C", "--csv", action="store_true", help="also write results to supermoons.csv"
    )
    args = parser.parse_args(argv)
    options = {
        "perigee": args.perigee,
        "distance": args.distance,
        "angulardiameter": args.angulardiameter,
    }

    if args.year is None:
        if args.cnt < 1:
            parser.error(f"expecting count of 1 or more, got {args.cnt}")
        if args.cnt > 1:
            print(f"The next {args.cnt} supermoons will be:")
        else:
            print("The next supermoon will be:")
        results = next_supermoons(count=args.cnt)
        for result in results:
            print("\n".join(describe(result, **options)))
        if args.csv:
            _write_csv(results)
        return 0

    if args.endyear is None:
        args.endyear = args.year
    for year in (args.year, args.endyear):
        if not MIN_YEAR <= year <= MAX_YEAR:
            parser.error(
                f"Please provide a year between {MIN_YEAR} and {MAX_YEAR}, got {year} (per JPL DE421)"
            )
    all_results = []
    for year in range(args.year, args.endyear + 1):
        results = supermoons(year)
        all_results.extend(results)
        print(f"{len(results)} supermoons during {year}:")
        if not args.brief:
            for result in results:
                print("\n".join(describe(result, **options)))
    if args.csv:
        _write_csv(all_results)
    return 0


def _write_csv(results, filename="supermoons.csv"):
    write_csv(results, filename)
    print(f"Wrote {len(results)} rows to {filename}")


if __name__ == "__main__":
    sys.exit(main())
