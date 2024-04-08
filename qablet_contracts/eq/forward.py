"""
Utils for creating forward starting options timetable
"""

from dataclasses import dataclass
from datetime import datetime

from qablet_contracts.timetable import EventsMixin


@dataclass
class ForwardOption(EventsMixin):
    ccy: str
    asset_name: str
    strike_rate: float
    strike_date: datetime
    maturity: datetime
    is_call: bool
    track: str = ""

    """A **Forward Starting Option**.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        strike_rate: the option strike in percent of fixing.
        strike_time: the time at which the strike is fixed.
        maturity: the maturity of the option in years.
        is_call: true if the option is a call.
        track: an optional identifier for the contract.

    Examples:
        >>> tt = forward_option_timetable("USD", "EQ", 1.1, 1.0, 2.0, True)
        >>> tt["events"].to_pandas()
          track  time   op  quantity unit
        0   NaN   1.0  NaN       0.0  FIX
        1         2.0    >       0.0  USD
        2         2.0    +      -1.1   .K
        3         2.0    +       1.0   EQ
    """

    def events(self):
        sign = 1 if self.is_call else -1
        return [
            {
                "track": None,
                "time": self.strike_date,
                "op": None,
                "quantity": 0,
                "unit": f"{self.track}.FIX_K",  # set the strike
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
            "FIX": {
                "type": "snapper",
                "inp": [self.asset_name],
                "fn": strike_fn,
                "out": [f"{self.track}.K"],
            }
        }


if __name__ == "__main__":
    # Create the option timetable
    timetable = ForwardOption(
        "USD",
        "SPX",
        1.0,
        datetime(2024, 3, 31),
        datetime(2024, 9, 30),
        True,
    ).timetable()

    print(timetable["events"].to_pandas())
