"""
This module contains examples of creating timetables for rate contracts such as swaps and swaptions.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from qablet_contracts.ir.dcf import dcf_30_360 as dcf
from qablet_contracts.timetable import EventsMixin


def simple_swap_period(
    ccy: str,
    start: datetime,
    end: datetime,
    fixed_rate: float,
    track: str = "",
) -> list:
    """Simple representation of a swap period, paying fixed, receiving floating rate.

    Args:
        ccy: the currency of the swap.
        start: the start of the period in years.
        end: the end of the period in years.
        fixed_rate: the fixed annual rate of the swap.
        track: an optional identifier for the contract.
    """
    return [
        {
            "track": track,
            "time": start,
            "op": "+",
            "quantity": 1,
            "unit": ccy,
        },
        {
            "track": track,
            "time": end,
            "op": "+",
            "quantity": -1 - fixed_rate * dcf(end, start),
            "unit": ccy,
        },
    ]


@dataclass
class Swap(EventsMixin):
    ccy: str
    dates: List[datetime]
    strike_rate: float
    track: str = ""
    """A **Vanilla Swap**.

    Args:
        ccy: the currency of the swap.
        times: the period times of the swap, including the inception and maturity.
        strike_rate: the strike rate of the swaption (in units, i.e. 0.02 means 200 bps).
        track: an optional identifier for the contract.

    Examples:
        >>> tt = swap_timetable("USD", [0.5, 1.0, 1.5], 0.05)
        >>> tt["events"].to_pandas()
          track  time op  quantity  unit
        1  .swp   0.5  +     1.000   USD
        2  .swp   1.0  +    -1.025   USD
        3  .swp   1.0  +     1.000   USD
        4  .swp   1.5  +    -1.025   USD
    """

    def events(self):
        events = []
        # payment events
        for start, end in zip(self.dates[0:-1], self.dates[1:]):
            events.extend(
                simple_swap_period(
                    self.ccy, start, end, self.strike_rate, self.track + ".swp"
                )
            )

        return events


if __name__ == "__main__":
    dates = pd.bdate_range(
        datetime(2023, 12, 31),
        datetime(2025, 12, 31),
        freq="2QE",
        inclusive="both",
    )
    strike_rate = 0.03

    timetable = Swap("USD", dates, strike_rate).timetable()
    print(timetable["events"].to_pandas())
