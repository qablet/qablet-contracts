# Operations

The **op** column contains a string which can be `+`, `>`, `<`, or a condition

### Payment

`+` in the ops column indicates that the contract holder will receive
the payment specified by the **quantity** and the **unit**,
and then continue to receive whatever else is further down in the timetable
in the same track.

Example: A bond paying 5 USD semi-annually and maturing in two years. 

```python
  track  time op  quantity unit
         0.5  +         5  USD
         1.0  +         5  USD
         1.5  +         5  USD
         2.0  +       105  USD
```


### Choice of contract holder

`>` in the ops column indicates that the **contract holder can choose** from the following two options

- receive the payment specified by the **quantity** and the **unit**, and then terminate the contract.
- or, instead of that payment, receive whatever else is further down in the timetable in the same track.

Example: An European Call Option with strike 2800, expiring in 1 year.

```python
  track  time op  quantity unit
         1.0  >       0.0  USD
         1.0  +   -2800.0  USD
         1.0  +       1.0  SPX
```


### Choice of contract's counterparty

`<` in the ops column indicates that the **counterparty can choose** from the following two options

- pay the holder the payment specified by the **quantity** and the **unit**, and then terminate the contract.
- or, instead of that payment, pay the holder whatever else is further down in the timetable in the same track.

Example: A callable bond, paying 5 USD semi-annually, maturing in two years, and callable at the end of the first year.

```python
  track  time op  quantity unit
         0.5  +         5  USD
         1.0  +         5  USD
         1.0  <       100  USD
         1.5  +         5  USD
         2.0  +       105  USD
```


### Contingent Event

Anything else in the `op` column is the string name of an expression.

 - If the expression evaluates to true, the holder will receive the payment specified by the **quantity** and the **unit**, and then terminate the contract.
 - If the expression evaluates to false, then instead of that payment, holder will receive whatever else is further down in the timetable in the same track.

Example: knock-in or knock-out events in a barrier option.

### Snapper

If the **unit** column contains a Snapper, i.e. a path dependent calculation to be performed at that time, then the **op** column is ignored.
