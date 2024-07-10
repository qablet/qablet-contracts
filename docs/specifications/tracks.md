# Tracks

A track identifies the contract, a leg of the contract, or a state of the contract. For simple contracts this might be just blank.

```py
>>> Option("USD", "SPX", 2900, datetime(2024, 3, 31), True).print_events()

      time op  quantity unit track
03/31/2024  >       0.0  USD
03/31/2024  +   -2900.0  USD
03/31/2024  +       1.0  SPX
```

Or you could assign a name to the track.

```py
>>> Option("USD", "SPX", 2900, datetime(2024, 3, 31), True, track="<SPX2900>").print_events()

      time op  quantity unit     track
03/31/2024  >       0.0  USD <SPX2900>
03/31/2024  +   -2900.0  USD <SPX2900>
03/31/2024  +       1.0  SPX <SPX2900>
```

In this example there are two tracks - `.opt` and `.swp`. In the event `0` and `3` the holder has an opportunity to switch from the `.opt`
track (which has no payments) to the `.swp` track (which has payments).
See [Bermuda Swaption](../examples/rate_swaption.md#qablet_contracts.ir.swaption.BermudaSwaption) for more on this example.

```py
      time op  quantity unit track
12/31/2023  >     1.000 .swp  .opt
12/31/2023  +     1.000  USD  .swp
06/30/2024  +    -1.015  USD  .swp
06/30/2024  >     1.000 .swp  .opt
06/30/2024  +     1.000  USD  .swp
12/31/2024  +    -1.015  USD  .swp
```

