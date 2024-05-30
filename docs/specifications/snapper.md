# Snapper

A Snapper represents a **path dependent calculation**, e.g. calculating returns in an equity cliquet. In the following timetable

- the first three events represent a **snapper** operation `CALCFIX`. These operations store results in a **snap**.
- the last event represents a payment for the contract, which pays `ACC`, the value of the snap.

```py
  track        time   op  quantity     unit
4   NaN  12/29/2023  NaN       0.0  CALCFIX
5   NaN  06/28/2024  NaN       0.0  CALCFIX
6   NaN  12/31/2024  NaN       0.0  CALCFIX
8        12/31/2024    +     100.0      ACC
```

A snapper is defined in the dataset, with four parameters. 

 - **type**, which must be "snapper"
 - **inp**, a list of inputs to the snapper **fn**. These can be assets, such as "SPX", whose value comes from the model. These can also be snaps, such as "ACC" or "S_last", which has been stored as a result of previous snapper operation. 
 - **fn**, a python function that takes a list of inputs, and returns a list of outputs. The length of expected inputs list must match the length of **inp**, while the length of the output list must match the length of **out**.
 - **out**, the list of name of snaps where the outputs are stored.  



e.g.
```py
# Define the function
def accumulator_update_fn(inputs):
    [s, s_last, a] = inputs

    ret = s / s_last - 1.0  # ret = S / S_last - 1
    ret = np.maximum(local_floor, ret)
    ret = np.minimum(local_cap, ret)

    return [a + ret, s]  # [A, S_last]

# Define the snapper
"CALCFIX": {
    "type": "snapper",
    "inp": ["SPX", "S_last", "ACC"],
    "fn": accumulator_update_fn,
    "out": ["ACC", "S_last"],
},
```


## Function Signature
See [Phrase Function Signature](phrase.md/#function-signature)