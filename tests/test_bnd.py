from datetime import datetime

from qablet_contracts.bnd.fixed import FixedBond, FixedCashFlows
from qablet_contracts.bnd.zero import Bond, BondCall, BondPut


def test_classes():
    tt = Bond("USD", datetime(2025, 3, 31)).timetable()
    assert len(tt["events"]) == 1

    tt = BondCall(
        "USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95
    ).timetable()
    assert len(tt["events"]) == 3

    tt = BondPut(
        "USD", datetime(2024, 9, 30), datetime(2025, 3, 31), 0.95
    ).timetable()
    assert len(tt["events"]) == 3

    tt = FixedCashFlows(
        "USD",
        [
            datetime(2023, 12, 31),
            datetime(2024, 6, 30),
            datetime(2024, 12, 31),
        ],
        [0.05, 0.05, 1.05],
    ).timetable()
    assert len(tt["events"]) == 3

    tt = FixedBond(
        "USD", 0.05, datetime(2023, 12, 31), datetime(2025, 12, 31), "2QE"
    ).timetable()
    assert len(tt["events"]) == 4
