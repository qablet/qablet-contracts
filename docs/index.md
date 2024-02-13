## What is Qablet?

A Qablet timetable defines a financial product using a sequence of payments, choices and conditions. A valuation model implemented with a Qablet parser can value any contract, as long as the contract can be described using a Qablet Timetable.

[The repositary](https://github.com/qablet/qablet-contracts) documented here contains code to create qablet timetables. It does not contain models that price qablet timetables. 
Valuation models are available in other independent projects.

## Overview of Documentation

The **SPECIFICATIONS** section describes the various elements of the language.
Start with the [timetable](specifications/timetable.md).

The **EXAMPLES** section has code samples to create many common financial contracts such as
bonds, options, swaps, and swaptions.
Start with the [Bonds](examples/bond.md).

## Valuation models

Valuation models are available in other independent projects, such as qablet-basic. See [here](https://qablet-academy.github.io/intro/) for a set of notebooks that value contracts using the qablet-basic package.
