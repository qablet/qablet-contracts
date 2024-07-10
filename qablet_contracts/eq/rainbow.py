"""
This module contains examples of equity rainbow options.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

from qablet_contracts.timetable import EventsMixin


@dataclass
class Rainbow(EventsMixin):
    """A **Rainbow Call Option** offers the holder the option to buy the best of
    a list of stocks (or none) for corresponding fixed strike prices, on the option maturity date.
    Similarly, a **Rainbow Put Option** offers the holder the option to sell the worst of
    a list of stocks (or none) for corresponding fixed strike prices.

    Args:
        ccy: the currency of the option.
        asset_names: the name of the underlying assets.
        strikes: the option strikes.
        notional: the notional of the option.
        maturity: the maturity of the option.
        is_call: true if the option is a call.
        track: an optional identifier for the contract.

    Examples:
        >>> assets = ["SPX", "FTSE", "N225"]
        >>> strikes = [5087, 7684, 39100]
        >>> Rainbow("USD", assets, strikes, 100_000, datetime(2024, 3, 31), True).print_events()
              time op       quantity unit track
        03/31/2024  + -100000.000000  USD
        03/31/2024  >      19.657952  SPX
        03/31/2024  >      13.014055 FTSE
        03/31/2024  >       2.557545 N225
        03/31/2024  +  100000.000000  USD
    """

    ccy: str
    asset_names: List[str]
    strikes: List[float]
    notional: float
    maturity: datetime
    is_call: bool
    track: str = ""

    def events(self):
        sign = 1 if self.is_call else -1
        # Pay the initial strike
        events = [
            {
                "track": "",
                "time": self.maturity,
                "op": "+",
                "quantity": -self.notional * sign,
                "unit": self.ccy,
            },
        ]

        # Options to receive any of the assets
        for asset, strike in zip(self.asset_names, self.strikes):
            events.append(
                {
                    "track": "",
                    "time": self.maturity,
                    "op": ">",
                    "quantity": self.notional / strike * sign,
                    "unit": asset,
                }
            )

        # Otherwise receive the notional back
        events.append(
            {
                "track": "",
                "time": self.maturity,
                "op": "+",
                "quantity": self.notional * sign,
                "unit": self.ccy,
            }
        )
        return events


if __name__ == "__main__":
    # Create the rainbow option
    Rainbow(
        "USD",
        ["SPX", "FTSE", "N225"],
        [5087, 7684, 39100],
        100_000,
        datetime(2024, 3, 31),
        True,
    ).print_events()
