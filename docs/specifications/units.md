# Unit

A string representing what is being paid. It can be a 

### Currency
such as `USD`, `EUR`. e.g. in a [Bond](../examples/bond_fixed.md)
```py
          track       time op  quantity unit
                12/31/2023  +      0.05  USD
```

### Stock, index, or a commodity
such as `SPX`, `AAPL`, `CL`. e.g. in a [Vanilla Option](../examples/equity_vanilla.md)
```py
          track       time op  quantity unit
                03/31/2024  +       1.0  SPX
```

### Track
such as the underlying swap in a [Bermuda Swaption](../examples/rate_swaption.md#qablet_contracts.ir.swaption.BermudaSwaption)
```py
          track       time op  quantity unit
          .opt  12/31/2023  >    1.000  .swp
```

### Phrase
such as a payoff formula in a [Autocallable Note](../examples/equity_autocall.md)
```py
          track       time op  quantity    unit
                07/31/2024  +     1.000  PAYOFF
```

### Snap
such as the accumulated returns in an accumulator cliquet. See more in the [Snapper](snapper.md) section.
```py
          track       time op  quantity   unit
                12/31/2024  +    100.0     ACC
```

### Snapper
It can also represent an action, such as the snapper that updates an accumulator from the current return.
```py
          track       time   op  quantity     unit
           NaN  06/30/2022  NaN       0.0  CALCFIX
``` 
