"""
Utils for creating barrier options timetable
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from qablet_contracts.eq.vanilla import Option
from qablet_contracts.timetable import EventsMixin


@dataclass
class OptionKO(EventsMixin):
    ccy: str
    asset_name: str
    strike: float
    maturity: datetime
    is_call: bool
    barrier: float
    barrier_type: str
    barrier_dates: List[datetime]
    rebate: float = 0
    track: str = ""

    """Create timetable for a **Knock Out Option**.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        strike: the option strike.
        maturity: the maturity of the option in years.
        is_call: true if the option is a call.
        barrier: the barrier level.
        barrier_type: the type of barrier option, e.g "Dn/Out" or "Up/Out".
        barrier_date: the barrier observation points.
        rebate: the rebate amount.
        track: an optional identifier for the contract.

    Examples:
        >>> tt = ko_option_timetable("USD", "EQ", 100, 0.2, True, 100, "Dn/Out", 5)
        >>> tt["events"].to_pandas()
          track  time  op  quantity unit
        0        0.00  KO       0.0  USD
        1        0.04  KO       0.0  USD
        2        0.08  KO       0.0  USD
        3        0.12  KO       0.0  USD
        4        0.16  KO       0.0  USD
        5        0.20  KO       0.0  USD
        6        0.20   >       0.0  USD
        7        0.20   +    -100.0  USD
        8        0.20   +       1.0   EQ
    """

    def events(self):
        events = []
        for barrier_date in self.barrier_dates:
            events.append(
                {
                    "track": self.track,
                    "time": barrier_date,
                    "op": "KO",
                    "quantity": self.rebate,
                    "unit": self.ccy,
                }
            )

        vanilla_events = Option(
            self.ccy,
            self.asset_name,
            self.strike,
            self.maturity,
            self.is_call,
            self.track,
        ).events()

        events.extend(vanilla_events)
        return events

    def expressions(self):
        """Define the knockout expression (KO)."""
        if self.barrier_type == "Dn/Out":

            def ko_fn(inputs):
                [S] = inputs
                return [S < self.barrier]
        elif self.barrier_type == "Up/Out":

            def ko_fn(inputs):
                [S] = inputs
                return [S > self.barrier]
        else:
            raise ValueError(f"Unknown barrier type: {self.barrier_type}")

        return {
            "KO": {
                "type": "phrase",
                "inp": [self.asset_name],
                "fn": ko_fn,
            }
        }


if __name__ == "__main__":
    # Create the KO option
    start = datetime(2024, 3, 31)
    maturity = datetime(2024, 9, 30)
    barrier_dates = pd.date_range(start, maturity, freq="ME")
    timetable = OptionKO(
        "USD", "EQ", 100, maturity, True, 102, "Up/Out", barrier_dates
    ).timetable()
    print(timetable["events"].to_pandas())
