# Timetable

A contract is described by a list of events. An event has five properties -
 track, time, op, quantity, and unit. Here is an example of an equity call option contract on SPX, with strike 2800 and one year expiration.
It is described using three events.

```python
 track  time op  quantity unit
         1.0  >       0.0  USD
         1.0  +   -2800.0  USD
         1.0  +       1.0  SPX
```


### Track

A string identifier for the contract, a leg of the contract, or a state of the contract. For simple contracts this might be just blank. See more in [Tracks](tracks.md).

### Time

The time of an event in years (float) from the valuation date.

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
In this example we define a contract that pays 100 USD after 1 year.

```python
import pyarrow as pa
from qablet_contracts.timetable import EVENT_SCHEMA

events = [
    {
        "track": "",
        "time": 1.0,
        "op": "+",
        "quantity": 100.0,
        "unit": "USD"
    },
]
timetable = {
    "events": pa.RecordBatch.from_pylist(events, schema=EVENT_SCHEMA),
    "expressions": {}
}
```

## Create a Simple Timetable
Alternatively, a simple timetable (without any expressions) can also be created using this method, from a list of dicts.

```python
from api import timetable_from_dicts
timetable = timetable_from_dicts(events)
```

### ::: qablet_contracts.timetable

