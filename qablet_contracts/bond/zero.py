"""
Create timetables for Zero Coupon Bond and related contracts.
"""

from qablet_contracts.timetable import timetable_from_dicts


def zcb_timetable(ccy: str, maturity: float) -> dict:
    """Create timetable for a zero coupon bond.

    Args:
        ccy: the currency of the bond.
        maturity: the maturity of the bond in years.

    """

    events = [
        {
            "track": "",
            "time": maturity,
            "op": "+",
            "quantity": 1,
            "unit": ccy,
        }  # get bond notional at bond expiration
    ]
    return timetable_from_dicts(events)


def zbp_timetable(
    ccy: str, opt_maturity: float, bond_maturity: float, strike: float
) -> dict:
    """Create timetable for a zero coupon bond put.

    Args:
        ccy: the currency of the bond.
        opt_maturity: the maturity of the option in years.
        bond_maturity: the maturity of the option in years.
        strike: the option strike.
    """

    events = [
        {
            "track": "",
            "time": opt_maturity,
            "op": ">",
            "quantity": 0,
            "unit": ccy,
        },  # Choose greater of nothing or continue to remaining events
        {
            "track": "",
            "time": opt_maturity,
            "op": "+",
            "quantity": strike,
            "unit": ccy,
        },  # get strike at expiration
        {
            "track": "",
            "time": bond_maturity,
            "op": "+",
            "quantity": -1,
            "unit": ccy,
        },  # pay bond notional at bond expiration
    ]
    return timetable_from_dicts(events)


if __name__ == "__main__":
    # Create a zero coupon bond timetable
    timetable = zcb_timetable("USD", 1)
    print("zcb:\n", timetable["events"].to_pandas())

    timetable = zbp_timetable("USD", 0.5, 1.0, 0.95)
    print("zbp:\n", timetable["events"].to_pandas())
