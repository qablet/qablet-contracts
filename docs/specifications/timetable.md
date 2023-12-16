# Timetable

A contract is described by a list of events. An event has five properties:

- track
- time
- op
- quantity
- unit

A simple contract can be created using this method

::: qablet_contracts.timetable

### Example

```python
from api import timetable_from_dicts

events = [
    {
        "track": "",
        "time": 1.0,
        "op": "+",
        "quantity": 100.0,
        "unit": "USD"
    },
]
timetable = timetable_from_dicts(events)
print(timetable["events"].to_pandas())
```

Output:
```python
  track  time op  quantity unit
0         1.0  +     100.0  USD
```

## Track

A String representing the contract, a leg of the contract, or a state of the contract.

## Time

The time of an event in years (f64).

## Op

A string which can be `+`, `>`, `<`, or a condition. See more in the Operations section.

## Quantity

The quantity being paid (f64).

## Unit

A string represents what is being paid. It can be a 

  - a currency like `USD`, `EUR`
  - a stock, or a commodity, like `AAPL`, `CL` 
  - a Track
  - an Expression, e.g. a libor fixing, a barrier, or a digital.
  - a Batch event
  - a Snapper, or a Snap

See more in the Units section.