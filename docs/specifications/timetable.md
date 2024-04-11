# Timetable

A contract is described by a list of events. An event has five properties -
 track, time, op, quantity, and unit. Here is an example of an equity call option contract on SPX, with strike 2800 and one year expiration.
It is described using three events.

```python
       track                      time op  quantity unit
0  <SPX2900> 2024-03-31 00:00:00+00:00  >       0.0  USD
1  <SPX2900> 2024-03-31 00:00:00+00:00  +    2900.0  USD
2  <SPX2900> 2024-03-31 00:00:00+00:00  +      -1.0  SPX
```


### Track

A string identifier for the contract, a leg of the contract, or a state of the contract. For simple contracts this might be just blank. See more in [Tracks](tracks.md).

### Time

The UNIX timestamp (milliseconds) of an event.

### Op

A string which can be `+`, `>`, `<`, or a condition. See more in [Operations](operations.md).

### Quantity

The quantity being paid (float).

### Unit

A string that represents what is being paid. It can be a currency like `USD`, `EUR`, or
a stock like `SPX`, `AAPL`, etc. See the [Units](units.md) section for all possible variants.


## How to create a timetable
The timetable is a dictionary with two components.

- events: the sequence of events stored as a pyarrow recordbatch
- [expressions](expressions.md): a dictionary defining any [phrases](phrase.md), [snappers](snapper.md), or [batches](batch.md) used in the timetable


A timetable can be created as follows, from a list of dicts.
In this example we define a contract that pays 100 USD on 2024-12-31.

```python
import pyarrow as pa
import datetime
from qablet_contracts.timetable import TS_EVENT_SCHEMA

events = [
    {
        "track": "",
        "time": datetime(2024, 12, 31),
        "op": "+",
        "quantity": 100.0,
        "unit": "USD",
    },
]
timetable = {
    "events": pa.RecordBatch.from_pylist(events, schema=TS_EVENT_SCHEMA),
    "expressions": {},
}
```

## Create a Timetable using `EventsMixin`
Alternatively, the same timetable as above can also be created using the `EventsMixin` class as shown below.

```python
from qablet_contracts.timetable import EventsMixin

@dataclass
class Bond(EventsMixin):
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

timetable = Bond("USD", datetime(2024, 12, 31)).timetable()
print("zcb:\n", timetable["events"].to_pandas())
```

## `qablet_contracts.timetable`

This module has several utilities to help create timetables.

### ::: qablet_contracts.timetable

