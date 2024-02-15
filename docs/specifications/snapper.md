# Snapper

A Snapper represents a **path dependent calculation**, e.g. calculating returns in an equity cliquet. In the following timetable

- the first event at time 0.5 represents a **snapper** operation `UPDATE`. This operation stores its result in a **snap**.
- the second event at time 3.0 represents a payment for the contract, which pays `A`, the value of the snap.

```python
  track  time op  quantity     unit
    NaN   0.5  s      0.00   UPDATE
          3.0  +      1.00        A
```

A snapper is defined in the dataset, with four parameters. 

 - **type**, which must be "snapper"
 - **inp**, a list of inputs to the snapper **fn**. These can be assets, such as "SPX", whose value comes from the model. These can also be snaps, such as "A" or "S_last", which has been stored as a result of previous snapper operation. 
 - **fn**, a python function that takes a list of inputs, and returns a list of outputs. The length of expected inputs list must match the length of **inp**, while the length of the output list must match the length of **out**.
 - **out**, the list of name of snaps where the outputs are stored.  



e.g.
```python
# Define the function
def accumulator_update_fn(inputs):
    [s, s_last, a] = inputs

    ret = s / s_last - 1.0  # ret = S / S_last - 1
    ret = np.maximum(local_floor, ret)
    ret = np.minimum(local_cap, ret)

    return [a + ret, s]  # [A, S_last]

# Define the snapper
"UPDATE": {
    "type": "snapper",
    "inp": ["SPX", "S_last", "A"],
    "fn": accumulator_update_fn,
    "out": ["A", "S_last"],
},
```


## Function Signature
See [Phrase Function Signature](phrase.md/#function-signature)