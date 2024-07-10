"""
This module contains examples of zero coupon bond and related contracts.
"""

from dataclasses import dataclass
from datetime import datetime

from qablet_contracts.timetable import EventsMixin


@dataclass
class Bond(EventsMixin):
    """A **zero coupon bond** pays a single fixed payment at a future time.

    Args:
        ccy: the currency of the bond.
        maturity: the maturity of the bond.
        track: an optional identifier for the contract.

    Examples:
        >>> Bond("USD", datetime(2025, 3, 31)).print_events()
              time op  quantity unit track
        03/31/2025  +       1.0  USD
    """

    ccy: str
    maturity: datetime
    track: str = ""

    def events(self):
        return [
            {
                "track": self.track,
                "time": self.maturity,
                "op": "+",
                "quantity": 1,
                "unit": self.ccy,
            }
        ]


@dataclass
class BondPut(EventsMixin):
    """A **zero coupon bond put** offers the holder the option to sell a zero coupon bond for
    a fixed strike price, on the option maturity date.

    Args:
        ccy: the currency of the bond.
        opt_maturity: the maturity of the option.
        bond_maturity: the maturity of the bond.
        strike: the option strike.
        track: an optional identifier for the contract.

    Examples:
        >>> BondPut("USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95).print_events()
              time op  quantity unit track
        09/30/2024  >      0.00  USD
        09/30/2024  +      0.95  USD
        03/31/2025  +     -1.00  USD
    """

    ccy: str
    opt_maturity: datetime
    bond_maturity: datetime
    strike: float
    track: str = ""

    def events(self):
        keys = ["track", "time", "op", "quantity", "unit"]
        events_list = [
            [self.track, self.opt_maturity, ">", 0, self.ccy],
            [self.track, self.opt_maturity, "+", self.strike, self.ccy],
            [self.track, self.bond_maturity, "+", -1, self.ccy],
        ]
        return [dict(zip(keys, event)) for event in events_list]


@dataclass
class BondCall(EventsMixin):
    """A **zero coupon bond call** offers the holder the option to buy a zero coupon bond for
    a fixed strike price, on the option maturity date.

    Args:
        ccy: the currency of the bond.
        opt_maturity: the maturity of the option.
        bond_maturity: the maturity of the bond.
        strike: the option strike.
        track: an optional identifier for the contract.

    Examples:
        >>> BondCall("USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95).print_events()
              time op  quantity unit track
        09/30/2024  >      0.00  USD
        09/30/2024  +     -0.95  USD
        03/31/2025  +      1.00  USD
    """

    ccy: str
    opt_maturity: datetime
    bond_maturity: datetime
    strike: float
    track: str = ""

    def events(self):
        keys = ["track", "time", "op", "quantity", "unit"]
        events_list = [
            [self.track, self.opt_maturity, ">", 0, self.ccy],
            [self.track, self.opt_maturity, "+", -self.strike, self.ccy],
            [self.track, self.bond_maturity, "+", 1, self.ccy],
        ]
        return [dict(zip(keys, event)) for event in events_list]


if __name__ == "__main__":
    print("Zero Coupon Bond")
    Bond("USD", datetime(2025, 3, 31)).print_events()

    print("Zero Coupon Bond Call")
    BondCall(
        "USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95
    ).print_events()

    print("Zero Coupon Bond Put")
    BondPut(
        "USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95
    ).print_events()
