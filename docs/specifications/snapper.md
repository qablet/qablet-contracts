# Snapper

A Snapper represents a **path dependent calculation**, e.g. calculating returns in an equity cliquet. In the following timetable, the first event represents a **snapper** operation `UPDATE`. This operation stores its result in a **snap**. The second event represents a payment for the contract, which pays `A`, the value of the snap.

```python
  track  time       op  quantity  unit
    NaN   0.5   UPDATE       0.0  None
    0.0   3.0        +       1.0     A
```

A snapper is defined in the dataset, with four parameters. 

 - **type**, which must be "snapper"
 - **inp**, a list of inputs to the snap_fn. These can be assets, such as "SPX", whose value comes from the model. These can also be snaps, such as "A" or "S_last", which has been stored as a result of previous snapper operation. 
 - **snap_fn**, a python function that takes the inputs, and returns snap values. The length of expected inputs list must match the length of **inp**, while the length of the output list must match the length of **out**.
 - **out**, the list of name of snap variables where the result is stored.  



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
    "snap_fn": accumulator_update_fn,
    "out": ["A", "S_last"],
},
```

Note: The values of the inputs will be a float, or a 1-D numpy array (e.g. the value of that variable in each Monte-Carlo path, or each point of a Finite Difference grid axis). All numpy arrays will be of the same size, or of length 1. The values of the output of the snap_fn must also be a scalar, of size 1, or same size as the inputs. A snapper written using arithmetic operations like `+`, `-`, `*`, and numpy functions would satisfy these requirements.
