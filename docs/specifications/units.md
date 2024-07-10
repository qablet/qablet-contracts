# Unit

A string representing what is being paid.

### Asset
It can be a currency such as `USD`, `EUR`. e.g. in a [Bond](../examples/bond_fixed.md)
```py
      time op  quantity unit track
06/30/2024  +     0.025  USD
```

It can be a stock, index, or a commodity such as `SPX`, `AAPL`, `CL`. e.g. in a [Vanilla Option](../examples/equity_vanilla.md)
```py
      time op  quantity unit track
03/31/2024  +       1.0  SPX
```

### Track
In can represent a track, e.g. in a [Bermuda Swaption](../examples/rate_swaption.md#qablet_contracts.ir.swaption.BermudaSwaption)
this event indicates the choice to switch to the underlying swap (track `.swp`)
instead of continuing on the current track (`.opt`)
```py
      time op  quantity unit track
12/31/2023  >     1.000 .swp  .opt
```

### Phrase
such as a payoff formula in a [Autocallable Note](../examples/equity_autocall.md)
```py
      time   op   quantity   unit track     
07/31/2024    +   1.000000 payoff
```

### Snap
such as the accumulated returns in an accumulator cliquet. See more in the [Snapper](snapper.md) section.
```py
      time  op  quantity   unit track
12/31/2024   +     100.0    ACC
```

### Snapper
It can also represent an action, such as the snapper that updates an accumulator from the current return.
```py
      time  op  quantity   unit track
06/30/2022 NaN       0.0 addfix   NaN
``` 
