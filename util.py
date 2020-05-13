"""
Utility functions that don't belong most anywhere else.
"""
from typing import Dict


def csv_to_entries(filename: str) -> Dict[str, str]:
    """Convert a CSV file into a dictionary of item/value pairs."""
    try:
        with open(filename, 'r') as csvfile:
            ret = {}
            for line in csvfile.readlines():
                line = line.strip().split(',')
                ret[line[0]] = line[1]
            return ret
    except FileNotFoundError:
        return {}
