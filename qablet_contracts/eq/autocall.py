"""
This module contains examples of autocallable notes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List

import numpy as np
import pandas as pd

from qablet_contracts.ir.dcf import dcf_30_360 as dcf
from qablet_contracts.timetable import EventsMixin


@dataclass
class DiscountCert(EventsMixin):
    """An **Autocallable Discount Certificate** is called if the asset price is above the barrier level
    on any of the barrier observation dates. If called, the note pays the principal and the coupon accreted
    till the call date. Otherwise, at maturity, if the asset is above strike, it pays the principal and the
    coupon at maturity. If the asset is below strike, the principal payment is scaled down proportionately
    with the asset price.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        initial_spot: the initial spot price of the asset.
        strike: downside participation below this strike.
        maturity: the maturity of the option in years.
        barrier: the note is called above this barrier level.
        barrier_dates: the barrier observation points.
        cpn_rate: the coupon rate.
        notional: the notional amount.
        track: an optional identifier for the contract.

    Examples:
        >>> start = datetime(2024, 3, 31)
        >>> maturity = datetime(2024, 7, 31)
        >>> barrier_dates = pd.date_range(start, maturity, freq="ME", inclusive="right")
        >>> DiscountCert("USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.092)print_events()
              time   op   quantity   unit track
        04/30/2024 call 100.836815    USD
        05/31/2024 call 101.680633    USD
        06/30/2024 call 102.531512    USD
        07/31/2024 call 103.389511    USD
        07/31/2024    +   1.000000 payoff
    """

    ccy: str
    asset_name: str
    initial_spot: float
    strike: float
    accrual_start: datetime
    maturity: datetime
    barrier: float
    barrier_dates: List[datetime]
    cpn_rate: float
    notional: float = 100.0
    track: str = ""

    def events(self):
        events = []
        # Autocall events
        for barrier_date in self.barrier_dates:
            # daycount_fraction
            frac = dcf(barrier_date, self.accrual_start)
            events.append(
                {
                    "track": self.track,
                    "time": barrier_date,
                    "op": "call",
                    "quantity": self.notional * np.exp(frac * self.cpn_rate),
                    "unit": self.ccy,
                }
            )

        # payoff at maturity
        events.append(
            {
                "track": "",
                "time": self.maturity,
                "op": "+",
                "quantity": 1.0,
                "unit": "payoff",
            }
        )
        return events

    def fixed_payoff(self):
        return self.notional * np.exp(
            dcf(self.maturity, self.accrual_start) * self.cpn_rate
        )

    def expressions(self):
        # Define the autocall condition
        def ko_fn(inputs):
            [S] = inputs
            return [S > (self.barrier * self.initial_spot / self.notional)]

        call = {
            "type": "phrase",
            "inp": [self.asset_name],
            "fn": ko_fn,
        }

        # Define the final payoff
        def payoff_fn(inputs):
            [s] = inputs
            eq_pay = s * (self.notional / self.initial_spot)
            return [
                np.where(eq_pay < self.strike, eq_pay, self.fixed_payoff())
            ]

        payoff = {
            "type": "phrase",
            "inp": [self.asset_name],
            "fn": payoff_fn,
        }

        return {"payoff": payoff, "call": call}


@dataclass
class ReverseCB(DiscountCert):
    """An **Autocallable Reverse Convertible** is called if the asset price is above the barrier level
    on any of the barrier observation dates. Otherwise, at maturity, if the asset is above strike, it pays the principal and the
    coupon at maturity. If the asset is below strike, the principal payment is scaled down proportionately
    with the asset price. The note pays periodic coupons until called or matured.

    Args:
        ccy: the currency of the option.
        asset_name: the name of the underlying asset.
        initial_spot: the initial spot price of the asset.
        strike: downside participation below this strike.
        maturity: the maturity of the option in years.
        barrier: the note is called above this barrier level.
        barrier_dates: the barrier observation points.
        cpn_rate: the coupon rate.
        notional: the notional amount.
        track: an optional identifier for the contract.

    Examples:
        >>> start = datetime(2024, 3, 31)
        >>> maturity = datetime(2024, 7, 31)
        >>> barrier_dates = pd.date_range(start, maturity, freq="ME", inclusive="right")
        >>> ReverseCB("USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.10).print_events()
              time   op   quantity   unit track
        04/30/2024    +   0.833333    USD
        04/30/2024 call 100.000000    USD
        05/31/2024    +   0.833333    USD
        05/31/2024 call 100.000000    USD
        06/30/2024    +   0.833333    USD
        06/30/2024 call 100.000000    USD
        07/31/2024    +   0.833333    USD
        07/31/2024 call 100.000000    USD
        07/31/2024    +   1.000000 payoff
    """

    def events(self):
        events = []
        cpn_start_dates = [self.accrual_start] + list(self.barrier_dates[:-1])
        # Autocall events
        for start, end in zip(cpn_start_dates, self.barrier_dates):
            # daycount_fraction
            frac = dcf(end, start)
            events.append(
                {
                    "track": self.track,
                    "time": end,
                    "op": "+",
                    "quantity": self.notional * frac * self.cpn_rate,
                    "unit": self.ccy,
                }
            )
            events.append(
                {
                    "track": self.track,
                    "time": end,
                    "op": "call",
                    "quantity": self.notional,
                    "unit": self.ccy,
                }
            )

        # payoff at maturity
        events.append(
            {
                "track": "",
                "time": self.maturity,
                "op": "+",
                "quantity": 1.0,
                "unit": "payoff",
            }
        )
        return events

    def fixed_payoff(self):
        return self.notional


if __name__ == "__main__":
    # Create the autocallable contract
    start = datetime(2024, 3, 31)
    maturity = datetime(2024, 7, 31)
    barrier_dates = pd.date_range(
        start, maturity, freq="ME", inclusive="right"
    )
    DiscountCert(
        "USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.10
    ).print_events()

    ReverseCB(
        "USD", "AAPL", 100, 80, start, maturity, 102, barrier_dates, 0.10
    ).print_events()
