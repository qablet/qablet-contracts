"""
This module contains examples of equity vanilla options.
"""

from dataclasses import dataclass
from datetime import datetime

from qablet_contracts.timetable import EventsMixin


@dataclass
class Option(EventsMixin):
    """An **European Call Option** offers the holder the option to buy a stock for
    a fixed strike price, on the option maturity date.
    Similarly, a **Put Option** offers the holder the option to sell a stock for
    a fixed strike price.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        strike: the option strike.
        maturity: the maturity of the option.
        is_call: true if the option is a call.
        track: an optional identifier for the contract.

    Examples:
        Call:
        >>> Option("USD", "SPX", 2900, datetime(2024, 3, 31), True).print_events()
            time   op  quantity unit track
        03/31/2024  >       0.0  USD
        03/31/2024  +   -2900.0  USD
        03/31/2024  +       1.0  SPX

        Put:
        >>> Option("USD", "SPX", 2900, datetime(2024, 3, 31), False).print_events()
              time op  quantity unit track
        03/31/2024  >       0.0  USD
        03/31/2024  +    2900.0  USD
        03/31/2024  +      -1.0  SPX
    """

    ccy: str
    asset_name: str
    strike: float
    maturity: datetime
    is_call: bool
    track: str = ""

    def events(self):
        sign = 1 if self.is_call else -1
        return [
            {
                "track": self.track,
                "time": self.maturity,
                "op": ">",
                "quantity": 0,
                "unit": self.ccy,
            },
            {
                "track": self.track,
                "time": self.maturity,
                "op": "+",
                "quantity": -self.strike * sign,
                "unit": self.ccy,
            },
            {
                "track": self.track,
                "time": self.maturity,
                "op": "+",
                "quantity": sign,
                "unit": self.asset_name,
            },
        ]


if __name__ == "__main__":
    # Create the option timetable
    for iscall in [True, False]:
        Option(
            "USD",
            "SPX",
            2900,
            datetime(2024, 3, 31),
            iscall,
            track="<SPX2900>",
        ).print_events()
