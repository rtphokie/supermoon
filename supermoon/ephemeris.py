"""
Shared Skyfield ephemeris and timescale, loaded lazily on first use.

The JPL DE421 ephemeris (~17 MB) is downloaded on first use to ~/.supermoon,
or to the directory named by the SUPERMOON_DATA environment variable.
"""

import os
from functools import cache
from pathlib import Path

from skyfield.api import Loader

DATA_DIR = os.environ.get("SUPERMOON_DATA", str(Path.home() / ".supermoon"))
EPHEMERIS = "de421.bsp"  # covers 1900-2050


@cache
def loader():
    return Loader(DATA_DIR, verbose=False)


@cache
def planets():
    return loader()(EPHEMERIS)


@cache
def timescale():
    return loader().timescale()
