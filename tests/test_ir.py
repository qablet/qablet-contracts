import pandas as pd

from qablet_contracts.ir.swap import Swap
from qablet_contracts.ir.swaption import BermudaSwaption, Swaption
from qablet_contracts.timetable import utc_dt


def test_classes():
    dates = pd.bdate_range(
        utc_dt(2023, 12, 31),
        utc_dt(2024, 12, 31),
        freq="2QE",
    )
    strike_rate = 0.03

    tt = Swap("USD", dates, strike_rate=0.03).timetable()
    assert len(tt["events"]) == 4

    tt = Swaption("USD", dates, strike_rate).timetable()
    assert len(tt["events"]) == 5

    tt = BermudaSwaption("USD", dates, strike_rate).timetable()
    assert len(tt["events"]) == 6
