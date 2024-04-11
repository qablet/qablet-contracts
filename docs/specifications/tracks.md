# Tracks

A track identifies the contract, a leg of the contract, or a state of the contract. For simple contracts this might be just blank.

```python
>>> timetable = Option(
    "USD", "SPX", 2900, datetime(2024, 3, 31), True
).timetable()
>>> print(timetable["events"].to_pandas())

  track                      time op  quantity unit
0       2024-03-31 00:00:00+00:00  >       0.0  USD
1       2024-03-31 00:00:00+00:00  +   -2900.0  USD
2       2024-03-31 00:00:00+00:00  +       1.0  SPX
```

Or you could assign a name to the track.

```python
>>> timetable = Option(
    "USD", "SPX", 2900, datetime(2024, 3, 31), True, "<SPX2900>"
).timetable()
>>> print(timetable["events"].to_pandas())

       track                      time op  quantity unit
0  <SPX2900> 2024-03-31 00:00:00+00:00  >       0.0  USD
1  <SPX2900> 2024-03-31 00:00:00+00:00  +   -2900.0  USD
2  <SPX2900> 2024-03-31 00:00:00+00:00  +       1.0  SPX
```

In this example there are two tracks - `.opt` and `.swp`. In the event `0` and `3` the holder has an opportunity to switch from the `.opt`
track (which has no payments) to the `.swp` track (which has payments).
See [Bermuda Swaption](../examples/rate_swaption.md#qablet_contracts.rate.swaption.bermuda_swaption_timetable) for more on this example.

```python
  track                      time op  quantity  unit
0  .opt 2023-12-31 00:00:00+00:00  >     1.000  .swp
1  .swp 2023-12-31 00:00:00+00:00  +     1.000   USD
2  .swp 2024-06-30 00:00:00+00:00  +    -1.015   USD
3  .opt 2024-06-30 00:00:00+00:00  >     1.000  .swp
4  .swp 2024-06-30 00:00:00+00:00  +     1.000   USD
5  .swp 2024-12-31 00:00:00+00:00  +    -1.015   USD
```

