"""
The main file to run.
"""
import sys
import os
from typing import List

from config import WatcherConfig
from cache import WatcherCache
import util


def main(args: List[str]):
    """The main function."""
    wconfig = WatcherConfig(os.environ)
    wcache = WatcherCache(wconfig)
    entries = util.csv_to_entries(args[1])


if __name__ == '__main__':
    main(sys.argv)
