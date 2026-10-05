"""
Shared Skyfield ephemeris and timescale, loaded lazily on first use.

The JPL DE421 ephemeris (~17 MB) is downloaded on first use to ~/.supermoon,
or to the directory named by the SUPERMOON_DATA environment variable.
"""

import os
from functools import lru_cache

from skyfield.api import Loader

DATA_DIR = os.environ.get(
    "SUPERMOON_DATA", os.path.join(os.path.expanduser("~"), ".supermoon")
)
EPHEMERIS = "de421.bsp"  # covers 1900-2050


@lru_cache(maxsize=None)
def loader():
    return Loader(DATA_DIR, verbose=False)


@lru_cache(maxsize=None)
def planets():
    return loader()(EPHEMERIS)


@lru_cache(maxsize=None)
def timescale():
    return loader().timescale()
