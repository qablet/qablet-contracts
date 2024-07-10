"""
This module contains examples of forward starting options.
"""

from dataclasses import dataclass
from datetime import datetime

from qablet_contracts.timetable import EventsMixin


@dataclass
class ForwardOption(EventsMixin):
    """In a **Forward Starting Option** the strike price is set on a future date as
    a predetermine percent of the stock price on the strike fixing date.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        strike_rate: the option strike in percent of fixing.
        strike_date: the datetime at which the strike is fixed.
        maturity: the maturity of the option in years.
        is_call: true if the option is a call.
        track: an optional identifier for the contract.

    Examples:
        >>> timetable = ForwardOption( "USD", "SPX", 1.0,
        datetime(2024, 3, 31), datetime(2024, 9, 30), True).print_events()
              time  op  quantity   unit track
        03/31/2024 NaN       0.0 .fix_K   NaN
        09/30/2024   >       0.0    USD
        09/30/2024   +      -1.0     .K
        09/30/2024   +       1.0    SPX
    """

    ccy: str
    asset_name: str
    strike_rate: float
    strike_date: datetime
    maturity: datetime
    is_call: bool
    track: str = ""

    def events(self):
        sign = 1 if self.is_call else -1
        return [
            {
                "track": None,
                "time": self.strike_date,
                "op": None,
                "quantity": 0,
                "unit": f"{self.track}.fix_K",  # set the strike
            },
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
                "quantity": -self.strike_rate * sign,
                "unit": f"{self.track}.K",
            },
            {
                "track": self.track,
                "time": self.maturity,
                "op": "+",
                "quantity": sign,
                "unit": self.asset_name,
            },
        ]

    def expressions(self):
        # Define the strike expression, return the spot itself.
        def strike_fn(inputs):
            return inputs

        return {
            f"{self.track}.fix_K": {
                "type": "snapper",
                "inp": [self.asset_name],
                "fn": strike_fn,
                "out": [f"{self.track}.K"],
            }
        }


if __name__ == "__main__":
    # Create the option timetable
    ForwardOption(
        "USD",
        "SPX",
        1.0,
        datetime(2024, 3, 31),
        datetime(2024, 9, 30),
        True,
    ).print_events()
