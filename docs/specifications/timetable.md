# Timetable

A contract is described by a list of events. An event has five properties:

- track
- time
- op
- quantity
- unit

Here is an example of an equity call option contract on SPX, with strike 2800 and one year expiration.
It is described using three events.

```python
 track  time op  quantity unit
         1.0  >       0.0  USD
         1.0  +   -2800.0  USD
         1.0  +       1.0  SPX
```


### Track

A string identifier for the contract, a leg of the contract, or a state of the contract.

### Time

The time of an event in years (float) from the valuation date.

### Op

A string which can be `+`, `>`, `<`, or a condition. See more in the [Operations](operations.md) section.

### Quantity

The quantity being paid (float).

### Unit

A string that represents what is being paid. It can be a currency like `USD`, `EUR`, or
a stock like `SPX`, `AAPL`, etc. See the [Units](units.md) section for all possible variants.


## How to create a timetable
The timetable is a dictionary with two components.

- events, the sequence of events stored as a pyarrow recordbatch
- expresions, a dictionary defining any snappers, batches, or expressions used in the timetable

A simple timetable can be created using this method, from a list of dicts.


::: qablet_contracts.timetable

## Example

Define a contract that pays 100 USD after 1 year.

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
