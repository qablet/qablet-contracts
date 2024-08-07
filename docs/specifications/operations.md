# Operations

The **op** column contains a string which can be `+`, `>`, `<`, or a condition.

## Payment
```
+
```

`+` in the ops column indicates that the contract holder will receive
the payment specified by the **quantity** and the **unit**,
and then continue to receive whatever else is further down in the timetable
in the **same track**.

Example: A bond paying 5% semi-annually and maturing in two years. 

```py
      time op  quantity unit track
06/30/2024  +     0.025  USD
12/31/2024  +     0.025  USD
06/30/2025  +     0.025  USD
12/31/2025  +     1.025  USD
```


## Choice of holder
```
>
```

`>` in the ops column indicates that the **contract holder can choose** from the following two options

- receive the payment specified by the **quantity** and the **unit**, and then terminate the contract.
- or, instead of that payment, receive whatever else is further down in the timetable in the same track.

Example: An European Call Option with strike 2900, expiring in 2024-03-31.

```py
      time op  quantity unit track
03/31/2024  >       0.0  USD
03/31/2024  +   -2900.0  USD
03/31/2024  +       1.0  SPX
```


!!! note
    A **choice** is different from a **condition**. In a choice, the holder of the contract (or counterparty)
    makes a decision. This decision takes future expectations into account, i.e. what is coming further down in the timetable.
    For the holder's choice, a reasonable model would choose the option with a greater expected value of future events.

## Choice of counterparty
```
<
```

`<` in the ops column indicates that the **counterparty can choose** from the following two options

- pay the holder the payment specified by the **quantity** and the **unit**, and then terminate the contract.
- or, instead of that payment, pay the holder whatever else is further down in the timetable in the same track.

Example: A callable bond, paying 5% USD semi-annually, maturing in two years, and callable at the end of the first year.

```py
      time op  quantity unit track
06/30/2024  +     0.025  USD
12/31/2024  +     0.025  USD
12/31/2024  <     1.000  USD
06/30/2025  +     0.025  USD
12/31/2025  +     1.025  USD
```


## Condition
```
ko
```

Any other string in the `op` column is assumed to be a [phrase](phrase.md).

 - If the phrase evaluates to true, the holder will receive the payment specified by the **quantity** and the **unit**, and then terminate the contract.
 - If the phrase evaluates to false, then instead of that payment, holder will receive whatever else is further down in the timetable in the same track.
 - If the phrase returns a float array instead of a bool array, the holder will receive a weighted sum of both outcomes.

Example: knock-in or knock-out events in a barrier option. In the example below `ko` is a phrase that describes the barrier condition. If the condition is met
the option is knocked out with a rebate of 1.0. If the barrier is not met, the contract continues further down the track.

```py
      time op  quantity unit track
03/31/2024 ko       0.0  USD
05/31/2024 ko       0.0  USD
07/31/2024 ko       0.0  USD
09/30/2024 ko       0.0  USD
09/30/2024  >       0.0  USD
09/30/2024  +    -100.0  USD
09/30/2024  +       1.0   EQ
```

See a complete example in [Barrier Options](../examples/equity_barrier.md).

## Snapper
```

```

If the **unit** is a [Snapper](snapper.md), i.e. a path dependent calculation to be performed at that time, then **op** should be `None` or `"s"`.
