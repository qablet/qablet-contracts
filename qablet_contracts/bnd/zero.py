"""
This module contains examples of creating timetables for Zero Coupon Bond and related contracts.
"""

from dataclasses import dataclass
from datetime import datetime

from qablet_contracts.timetable import EventsMixin


@dataclass
class Bond(EventsMixin):
    ccy: str
    maturity: datetime
    track: str = ""

    """A zero coupon bond.

    Args:
        ccy: the currency of the bond.
        maturity: the maturity of the bond in years.
        track: an optional identifier for the contract.

    Examples:
        >>> tt = zcb_timetable("USD", 1)
        >>> tt["events"].to_pandas()
          track  time op  quantity unit
        0         1.0  +       1.0  USD
    """

    def events(self):
        return [
            {
                "track": self.track,
                "time": self.maturity,
                "op": "+",
                "quantity": 1,
                "unit": self.ccy,
            }  # get bond notional at bond expiration
        ]

    # def timetable(self):
    #     return {"events": self.events(), "expressions": {}}


@dataclass
class BondPut(EventsMixin):
    ccy: str
    opt_maturity: datetime
    bond_maturity: datetime
    strike: float
    track: str = ""
    """Create timetable for a **zero coupon bond put**.

    Args:
        ccy: the currency of the bond.
        opt_maturity: the maturity of the option in years.
        bond_maturity: the maturity of the option in years.
        strike: the option strike.
        track: an optional identifier for the contract.

    Examples:
        >>> tt = zbp_timetable("USD", 0.5, 1.0, 0.95)
        >>> tt["events"].to_pandas()
          track  time op  quantity unit
        0         0.5  >      0.00  USD
        1         0.5  +      0.95  USD
        2         1.0  +     -1.00  USD
    """

    def events(self):
        return [
            {
                "track": self.track,
                "time": self.opt_maturity,
                "op": ">",
                "quantity": 0,
                "unit": self.ccy,
            },  # Choose greater of nothing (get 0) or exercise (continue to remaining events)
            {
                "track": self.track,
                "time": self.opt_maturity,
                "op": "+",
                "quantity": self.strike,
                "unit": self.ccy,
            },  # get strike at expiration
            {
                "track": self.track,
                "time": self.bond_maturity,
                "op": "+",
                "quantity": -1,
                "unit": self.ccy,
            },  # pay bond notional at bond expiration
        ]


if __name__ == "__main__":
    # Create a zero coupon bond timetable
    timetable = Bond("USD", datetime(2025, 3, 31)).timetable()
    print("zcb:\n", timetable["events"].to_pandas())

    timetable = BondPut(
        "USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95
    ).timetable()
    print("zbp:\n", timetable["events"].to_pandas())
