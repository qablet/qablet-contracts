# Unit

A string representing what is being paid. It can be a 

  - a currency like `USD`, `EUR`. e.g. in a [Bond](../examples/bond_fixed.md)
```
                12/31/2023  +      0.05  USD
```

  - a stock, or a commodity, like `AAPL`, `CL`. e.g. in a [Vanilla Option](../examples/equity_vanilla.md)
```
                03/31/2024  +       1.0  SPX
```

  - a Track, e.g. the fixed leg of a swap. e.g. in a [Bermuda Swaption](../examples/rate_swaption.md#qablet_contracts.rate.swaption.bermuda_swaption_timetable)
```
          .opt  12/31/2023  >     1.000  .swp
```

  - a Phrase, e.g. a libor fixing, or a digital payoff. e.g. see [Autocallable Note](../examples/equity_autocall.md)
```
                07/31/2024  +    1.000  PAYOFF
```

  - a Snap, i.e. a path dependent quantity, e.g. an accumulator cliquet. See more in the [Snapper](snapper.md) section.
```
                12/31/2024  +    100.0     ACC
```

It can also represent an action, such as

  - a Snapper, e.g update an accumulator from the current return.
```
           NaN  06/30/2022  NaN    0.0  CALCFIX
``` 
