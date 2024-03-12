# Tracks

A track identifies the contract, a leg of the contract, or a state of the contract. For simple contracts this might be just blank.

```python
>>> timetable = option_timetable("USD", "SPX", 2900, 0.5, True)
>>> print(timetable["events"].to_pandas())

  track  time op  quantity unit
0         0.5  >       0.0  USD
1         0.5  +   -2900.0  USD
2         0.5  +       1.0  SPX
```

Or you could assign a name to the track.

```python
>>> timetable = option_timetable("USD", "SPX", 2900, 0.5, True, track="ID_01")
>>> print(timetable["events"].to_pandas())

   track  time op  quantity unit
0  ID_01   0.5  >       0.0  USD
1  ID_01   0.5  +   -2900.0  USD
2  ID_01   0.5  +       1.0  SPX
```

In this example there are two tracks - `.opt` and `.swp`. In the event `0` and `3` the holder has an opportunity to switch from the `.opt`
track (which has no payments) to the `.swp` track (which has payments).
See [Bermuda Swaption](/examples/rate_swaption/#qablet_contracts.rate.swaption.bermuda_swaption_timetable) for more on this example.

```python
  track  time op  quantity  unit
0  .opt   0.5  >     1.000  .swp
1  .swp   0.5  +     1.000   USD
2  .swp   1.0  +    -1.025   USD
3  .opt   1.0  >     1.000  .swp
4  .swp   1.0  +     1.000   USD
5  .swp   1.5  +    -1.025   USD
```

