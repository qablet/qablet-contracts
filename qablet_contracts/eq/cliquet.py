"""
This module contains examples of equity cliquet contracts.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from qablet_contracts.timetable import EventsMixin


@dataclass
class Accumulator(EventsMixin):
    """In an **Accumulator** the asset returns are calculated over a series of consecutive periods.
    Each return is subject to a local floor and cap, then accumulated by adding, and finally the
    accumulated payoff is subject to a global floor.

    Args:
        ccy: the currency of the bond.
        asset_name: the name of the underlying asset.
        fix_dates: the fixing times of the cliquet.
        global_floor: the global floor of the cliquet.
        local_floor: the local floor of the cliquet.
        local_cap: the local cap of the cliquet.
        notional: the notional of the cliquet.
        track: an optional identifier for the contract.

    Examples:
        >>> fix_dates = pd.bdate_range(datetime(2021, 12, 31), datetime(2024, 12, 31), freq="2BQE")
        >>> Accumulator("USD", "SPX", fix_dates, 0.0, -0.03, 0.05).print_events()
              time  op  quantity   unit track
        12/31/2021 NaN       0.0  start   NaN
        06/30/2022 NaN       0.0 addfix   NaN
        12/30/2022 NaN       0.0 addfix   NaN
        06/30/2023 NaN       0.0 addfix   NaN
        12/29/2023 NaN       0.0 addfix   NaN
        06/28/2024 NaN       0.0 addfix   NaN
        12/31/2024 NaN       0.0 addfix   NaN
        12/31/2024   >       0.0    USD
        12/31/2024   +     100.0    ACC
    """

    ccy: str
    asset_name: str
    fix_dates: List[datetime]
    global_floor: float
    local_floor: float
    local_cap: float
    notional: float = 100.0
    track: str = ""
    state: dict = field(default_factory=dict)

    def events(self):
        maturity = self.fix_dates[-1]

        events = [
            {
                "track": None,
                "time": self.fix_dates[0],
                "op": None,
                "quantity": 0,
                "unit": "start",  # start accumulator
            }
        ]
        for fixing_time in self.fix_dates[1:]:
            events.append(
                {
                    "track": None,
                    "time": fixing_time,
                    "op": None,
                    "quantity": 0,
                    "unit": "addfix",  # update accumulator
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
                "quantity": self.notional,
                "unit": "ACC",
            }
        )
        return events

    def expressions(self):
        last_acc = self.state.get("ACC", 0.0)

        if "S_PREV" in self.state:

            def accumulator_init_fn(inputs):
                [s] = inputs
                return [last_acc, self.state["S_PREV"]]  # [ACC, S_PREV]
        else:

            def accumulator_init_fn(inputs):
                [s] = inputs
                return [last_acc, s]  # [ACC, S_PREV]

        def accumulator_update_fn(inputs):
            [s, s_prev, a] = inputs

            ret = s / s_prev - 1.0  # ret = S / S_PREV - 1
            ret = np.maximum(self.local_floor, ret)
            ret = np.minimum(self.local_cap, ret)

            return [a + ret, s]  # [ACC, S_PREV]

        return {
            "start": {
                "type": "snapper",
                "inp": [self.asset_name],
                "fn": accumulator_init_fn,
                "out": ["ACC", "S_PREV"],
            },
            "addfix": {
                "type": "snapper",
                "inp": [self.asset_name, "S_PREV", "ACC"],
                "fn": accumulator_update_fn,
                "out": ["ACC", "S_PREV"],
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
    Accumulator(
        "USD",
        "SPX",
        fix_dates,
        global_floor,
        local_floor,
        local_cap,
        state={"S_PREV": 1.0},
    ).print_events()
