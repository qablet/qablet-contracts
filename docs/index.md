# What is Qablet?

A Qablet timetable defines a financial product using a sequence of payments, choices and conditions. A valuation model implemented with a Qablet parser can value any contract, as long as the contract can be described using a Qablet Timetable such as this one -

```
          track        time op  quantity unit
        0    #1  03/31/2024  >       0.0  USD
        1    #1  03/31/2024  +   -2900.0  USD
        2    #1  03/31/2024  +       1.0  SPX
```


## Overview of Documentation

- The **SPECIFICATIONS** section describes the various elements of the language.
Start with the [timetable](specifications/timetable.md).

- The **CONTRACTS** section documents [this repository](https://github.com/qablet/qablet-contracts) which contains classes to create qablet timetables
for many common financial contracts such as
[Bonds](examples/bond_zero.md),
[Options](examples/equity_vanilla.md),
[Swaps](examples/rate_swap.md), and [Swaptions](examples/rate_swaption.md).

## Also See
The repo documented here does not contain models that price qablet timetables. Valuation and backtesting models are available in other independent projects, such as qablet-basic.

- [Qablet Models](https://qablet-academy.github.io/intro/) documents the Monte-Carlo and Finite Difference models in qablet-basic.
- [Qablet Learning Path](https://github.com/qablet-academy/intro) is a set of Jupyter notebooks that value contracts using the qablet-basic package.
- [Qablet Demo](https://apps-dash.onrender.com/) is an interactive experience.
