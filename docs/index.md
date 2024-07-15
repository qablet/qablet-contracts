# What is Qablet?

A Qablet timetable defines a financial product using a sequence of payments, choices and conditions. A valuation model implemented with a Qablet parser can value any contract, as long as the contract can be described using a Qablet Timetable such as this one -

```py
      time op  quantity unit track
03/31/2024  >       0.0  USD    #1
03/31/2024  +    2900.0  USD    #1
03/31/2024  +      -1.0  SPX    #1
```


## Overview of Documentation

- The **SPECIFICATIONS** section describes the elements of the language.
Start with the [timetable](specifications/timetable.md).

- The **CONTRACTS** section documents the [qablet-contracts package](https://github.com/qablet/qablet-contracts) which contains qablet timetables
for many common financial contracts such as
[Bonds](examples/bond_zero.md),
[Options](examples/equity_vanilla.md),
[Swaps](examples/rate_swap.md), and [Swaptions](examples/rate_swaption.md).

If you are new to Qablet, 

- Start with a [simple end to end example](https://qablet-academy.github.io/intro/quickstart/)
- Then follow the [Qablet Learning Path](https://github.com/qablet-academy/intro) which is a set of Jupyter notebooks to walk you through simple to advanced uses of Qablet
- [Qablet Demo](https://apps-dash.onrender.com/) is an interactive experience.
