# Timetable

A contract is described by a list of events. An event has five properties -
 time, op, quantity, unit, and track. Here is an example of an equity call option contract on SPX, with strike 2800 and one year expiration.
It is described using three events.

```py
            time   op  quantity unit track
        03/31/2024  >       0.0  USD
        03/31/2024  +   -2900.0  USD
        03/31/2024  +       1.0  SPX
```


### Time

The UNIX timestamp (milliseconds) of an event. It can be specified as **datetime** and any of the methods of creating timetable below will convert it to the right format.

### Op

A **string** which can be `+`, `>`, `<`, or a condition. See more in [Operations](operations.md).

### Quantity

The quantity being paid (**float**).

### Unit

A **string** that represents what is being paid. It can be a currency like `USD`, `EUR`, or
a stock like `SPX`, `AAPL`, etc. See the [Units](units.md) section for all possible variants.

### Track

A **string** identifier for the contract, a leg of the contract, or a state of the contract. For simple contracts this might be just blank. See more in [Tracks](tracks.md).


## Create a timetable
The timetable is a dictionary with two components.

- events: the sequence of events stored as a pyarrow recordbatch
- [expressions](expressions.md) (optional): a dictionary defining any [phrases](phrase.md) or [snappers](snapper.md) used in the timetable

### Create using `from_pylist`

A timetable can be created as follows, from a list of dicts.
In this example we define a contract that pays 100 USD on 2024-12-31.

```py
from pyarrow import RecordBatch as rb
from datetime import datetime
from qablet_contracts.timetable import TS_EVENT_SCHEMA

events = [
    {
        "time": datetime(2024, 12, 31),
        "op": "+",
        "quantity": 100.0,
        "unit": "USD",
        "track": "",
    },
]
timetable = {
    "events": rb.from_pylist(events, schema=TS_EVENT_SCHEMA)
}
```

### Create using `EventsMixin`
Alternatively, the same timetable as above can also be created using the `EventsMixin` class as shown below.

```py
from qablet_contracts.timetable import EventsMixin

@dataclass
class Bond(EventsMixin):
    ccy: str
    maturity: datetime
    track: str = ""

    def events(self):
        return [
            {
                "time": self.maturity,
                "op": "+",
                "quantity": 1,
                "unit": self.ccy,
                "track": self.track,
            }
        ]

timetable = Bond("USD", datetime(2024, 12, 31)).timetable()
```

### Create using `from_pandas`
Here we create a timetable with two events using a pandas dataframe.

```py
import pandas as pd

df = pd.DataFrame(
    [
        [datetime(2024, 6, 30), "+", 5.0, "USD", ""],
        [datetime(2024, 12, 31), "+", 100.0, "USD", ""],
    ],
    columns=["time", "op", "quantity", "unit", "track"],
)

timetable = {
    "events": rb.from_pandas(df, schema=TS_EVENT_SCHEMA),
}
```


## Print a timetable

The events of a timetable is a `pyarrow` recordbatch. It is an efficient data structure for storage, read, write and platform interoperabiity. However, it doesn't print pretty.

### Print using `pandas`

We can print by converting it to a pandas dataframe.

```py
timetable["events"].to_pandas()

                       time op  quantity unit track
0 2025-03-31 00:00:00+00:00  +       1.0  USD
```
### Print using `polars`

We can print by converting it to a polars dataframe.

```py
from polars import from_arrow
df = from_arrow(timetable["events"])
print(df)

shape: (1, 5)
┌-------------------------┬-----┬----------┬------┬-------┐
│ time                    ┆ op  ┆ quantity ┆ unit ┆ track │
│ ---                     ┆ --- ┆ ---      ┆ ---  ┆ ---   │
│ datetime[ms, UTC]       ┆ cat ┆ f64      ┆ cat  ┆ cat   │
╞-------------------------╪-----╪----------╪------╪-------╡
│ 2025-03-31 00:00:00 UTC ┆ +   ┆ 1.0      ┆ USD  ┆       │
└-------------------------┴-----┴----------┴------┴-------┘

```

### Print using `print_events`

The contract dataclass has a convenience function `print_events` to print a shorter form using pandas.

```py
contract = Bond("USD", datetime(2025, 3, 31))
contract.print_events()

      time op  quantity unit track
03/31/2025  +       1.0  USD
```