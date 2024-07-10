"""
This module contains examples of barrier options.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd

from qablet_contracts.eq.vanilla import Option
from qablet_contracts.timetable import EventsMixin


@dataclass
class OptionKO(EventsMixin):
    """In a **Dn/Out Option** the contract is cancelled if the underlying asset price
    falls below the barrier level on any of the barrier observation dates.
    In an **Up/Out Option** the contract is cancelled if the underlying asset price
    rises above the barrier level on any of the observation dates.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        strike: the option strike.
        maturity: the maturity of the option in years.
        is_call: true if the option is a call.
        barrier: the barrier level.
        barrier_type: the type of barrier option, e.g "Dn/Out" or "Up/Out".
        barrier_dates: the barrier observation points.
        rebate: the rebate amount paid at cancellation.
        track: an optional identifier for the contract.

    Examples:
        >>> start = datetime(2024, 3, 31)
        >>> maturity = datetime(2024, 9, 30)
        >>> barrier_dates = pd.date_range(start, maturity, freq="2ME")
        >>> OptionKO("USD", "EQ", 100, maturity, True, 102, "Up/Out", barrier_dates).print_events()
              time op  quantity unit track
        03/31/2024 ko       0.0  USD
        05/31/2024 ko       0.0  USD
        07/31/2024 ko       0.0  USD
        09/30/2024 ko       0.0  USD
        09/30/2024  >       0.0  USD
        09/30/2024  +    -100.0  USD
        09/30/2024  +       1.0   EQ
    """

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

    def events(self):
        events = []
        for barrier_date in self.barrier_dates:
            events.append(
                {
                    "track": self.track,
                    "time": barrier_date,
                    "op": "ko",
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
        """Define the knockout expression (ko)."""
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
            "ko": {
                "type": "phrase",
                "inp": [self.asset_name],
                "fn": ko_fn,
            }
        }


if __name__ == "__main__":
    # Create the ko option
    start = datetime(2024, 3, 31)
    maturity = datetime(2024, 9, 30)
    barrier_dates = pd.date_range(start, maturity, freq="2ME")
    OptionKO(
        "USD", "EQ", 100, maturity, True, 102, "Up/Out", barrier_dates
    ).print_events()
