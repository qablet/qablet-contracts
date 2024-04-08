"""
This module contains examples of day count fraction calculations.
"""

from datetime import timedelta


def is_eom(dt):
    return (dt + timedelta(days=1)).month != dt.month


def dcf_30_360(end, start):
    """Calculate a simple 30/360 daycount fraction."""
    if is_eom(start):
        d1 = 30
    else:
        d1 = start.day

    if d1 == 30 and end.day == 31:
        d2 = 30
    else:
        d2 = end.day

    return (
        (end.year - start.year)
        + (end.month - start.month) / 12
        + (d2 - d1) / 360
    )
