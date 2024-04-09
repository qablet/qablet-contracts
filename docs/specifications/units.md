# Unit

A string representing what is being paid. It can be a 

  - a currency like `USD`, `EUR`. e.g. see [Bonds](../examples/bond_fixed.md)
  - a stock, or a commodity, like `AAPL`, `CL`. e.g. see [Vanilla Option](../examples/equity_vanilla.md)
  - a Track, e.g. the fixed leg of a swap. e.g. see [Bermuda Swaption](../examples/rate_swaption.md#qablet_contracts.rate.swaption.bermuda_swaption_timetable)
  - a Phrase, e.g. a libor fixing, or a digital payoff. e.g. see [Autocallable Note](../examples/equity_autocall.md)
  - a Batch event, e.g. issuers option to deliver one of many bonds. See more in the [Batch](batch.md) section.
  - a Snap, i.e. a path dependent quantity, e.g. an accumulator cliquet. See more in the [Snapper](snapper.md) section.


It can also represent an action, such as

  - a Snapper, e.g update an accumulator from the current return.
 
