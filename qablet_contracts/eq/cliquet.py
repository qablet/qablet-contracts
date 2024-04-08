"""
This module contains examples of creating timetables for equity cliquet contracts.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from qablet_contracts.timetable import EventsMixin


@dataclass
class Accumulator(EventsMixin):
    ccy: str
    asset_name: str
    fix_dates: List[datetime]
    global_floor: float
    local_floor: float
    local_cap: float
    # last_fix: Optional[float] = None
    # last_acc: float = 0.0
    track: str = ""

    """An **Accumulator Cliquet**.

    Args:
        ccy: the currency of the bond.
        asset_name: the name of the underlying asset.
        fix_dates: the fixing times of the cliquet.
        global_floor: the global floor of the cliquet.
        local_floor: the local floor of the cliquet.
        local_cap: the local cap of the cliquet.
        last_fix: the last fixing, None if no fixing has happened yet.
        last_acc: the accumulated return so far.
        track: an optional identifier for the contract.

    Examples:
        >>> tt = clique_timetable("USD", "SPX", [1.0, 2.0, 3.0], 0.01, -0.03, 0.05)
        >>> tt["events"].to_pandas()
          track  time   op  quantity     unit
        0   NaN   0.0  NaN       0.0    _INIT
        1   NaN   0.5  NaN       0.0  _UPDATE
        2   NaN   1.0  NaN       0.0  _UPDATE
        3   NaN   1.5  NaN       0.0  _UPDATE
        4   NaN   2.0  NaN       0.0  _UPDATE
        5   NaN   2.5  NaN       0.0  _UPDATE
        6   NaN   3.0  NaN       0.0  _UPDATE
        7         3.0    >       0.0      USD
        8         3.0    +       1.0       _A
    """

    def events(self):
        maturity = self.fix_dates[-1]

        events = [
            {
                "track": None,
                "time": self.fix_dates[0],
                "op": None,
                "quantity": 0,
                "unit": "_INIT",  # initialize accumulator
            }
        ]
        for fixing_time in self.fix_dates[1:]:
            events.append(
                {
                    "track": None,
                    "time": fixing_time,
                    "op": None,
                    "quantity": 0,
                    "unit": "_UPDATE",  # update accumulator
                }
            )
        events.append(
            {
                "track": self.track,
                "time": maturity,
                "op": ">",  # global floor
                "quantity": self.global_floor,
                "unit": self.ccy,
            }
        )
        events.append(
            {
                "track": self.track,
                "time": maturity,
                "op": "+",  # pay the accumulated amount
                "quantity": 1,
                "unit": "_A",
            }
        )
        return events

    def expressions(self):
        last_acc = 0.0

        def accumulator_init_fn(inputs):
            [s] = inputs
            return [last_acc, s]  # [A, S_last]

        def accumulator_update_fn(inputs):
            [s, s_last, a] = inputs

            ret = s / s_last - 1.0  # ret = S / S_last - 1
            ret = np.maximum(self.local_floor, ret)
            ret = np.minimum(self.local_cap, ret)

            return [a + ret, s]  # [A, S_last]

        return {
            "_INIT": {
                "type": "snapper",
                "inp": [self.asset_name],
                "fn": accumulator_init_fn,
                "out": ["_A", "_S_last"],
            },
            "_UPDATE": {
                "type": "snapper",
                "inp": [self.asset_name, "_S_last", "_A"],
                "fn": accumulator_update_fn,
                "out": ["_A", "_S_last"],
            },
        }


if __name__ == "__main__":
    # Create the cliquet

    fix_dates = pd.bdate_range(
        datetime(2021, 12, 31), datetime(2024, 12, 31), freq="2BQE"
    )

    global_floor = 0.0
    local_floor = -0.03
    local_cap = 0.05
    timetable = Accumulator(
        "USD", "SPX", fix_dates, global_floor, local_floor, local_cap
    ).timetable()

    print(timetable["events"].to_pandas())
