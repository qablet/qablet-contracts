"""
This module contains examples of creating timetables for rate contracts such as swaps and swaptions.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from qablet_contracts.ir.swap import simple_swap_period
from qablet_contracts.timetable import EventsMixin


@dataclass
class Swaption(EventsMixin):
    ccy: str
    dates: List[datetime]
    strike_rate: float
    track: str = ""
    """A **Vanilla Swaption**.
    In a Vanilla swaption the holder gets the opportunity to enter into the swap at the beginning of the first period.

    Args:
        ccy: the currency of the swap.
        times: the period times of the underlying swap, including the inception and maturity.
        strike_rate: the strike rate of the swaption (in units, i.e. 0.02 means 200 bps).
        track: an optional identifier for the contract.

    Examples:
        >>> tt = swaption_timetable("USD", [0.5, 1.0, 1.5], 0.05)
        >>> tt["events"].to_pandas()
          track  time op  quantity  unit
        0  .opt   0.5  >     1.000  .swp
        1  .swp   0.5  +     1.000   USD
        2  .swp   1.0  +    -1.025   USD
        3  .swp   1.0  +     1.000   USD
        4  .swp   1.5  +    -1.025   USD
    """

    def events(self):
        # option expiration event at beginning of the swap
        events = [
            {
                "track": self.track + ".opt",
                "time": self.dates[0],
                "op": ">",
                "quantity": 1,
                "unit": self.track + ".swp",
            }
        ]
        # payment events for the underlying swap
        for start, end in zip(self.dates[0:-1], self.dates[1:]):
            events.extend(
                simple_swap_period(
                    self.ccy, start, end, self.strike_rate, self.track + ".swp"
                )
            )

        return events


@dataclass
class BermudaSwaption(EventsMixin):
    ccy: str
    dates: List[float]
    strike_rate: float
    track: str = ""
    """A **Co-terminal Bermuda Swaption**.
    In a Co-terminal Bermuda swaption, the holder can exercise his option at the beginning of each swap period.
    If exercised, the holder pays and receives all remaining payments of the swap. If not exercised, there are
    no payments in the next swap period. Irrespective of the time of exercise, the swap terminates at the same date.


    Args:
        ccy: the currency of the swap.
        times: the period times of the underlying swap, including the inception and maturity.
        strike_rate: the strike rate of the swaption (in units, i.e. 0.02 means 200 bps).
        track: an optional identifier for the contract.

    Examples:
        >>> tt = bermuda_swaption_timetable("USD", [0.5, 1.0, 1.5], 0.05)
        >>> tt["events"].to_pandas()
          track  time op  quantity  unit
        0  .opt   0.5  >     1.000  .swp
        1  .swp   0.5  +     1.000   USD
        2  .swp   1.0  +    -1.025   USD
        3  .opt   1.0  >     1.000  .swp
        4  .swp   1.0  +     1.000   USD
        5  .swp   1.5  +    -1.025   USD
    """

    def events(self):
        events = []
        for start, end in zip(self.dates[0:-1], self.dates[1:]):
            # option expiration event before each period
            events.append(
                {
                    "track": self.track + ".opt",
                    "time": start,
                    "op": ">",
                    "quantity": 1,
                    "unit": self.track + ".swp",
                }
            )
            # payment event for the underlying swap
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

    timetable = Swaption("USD", dates, strike_rate).timetable()
    print(timetable["events"].to_pandas())

    timetable = BermudaSwaption("USD", dates, strike_rate).timetable()
    print(timetable["events"].to_pandas())
