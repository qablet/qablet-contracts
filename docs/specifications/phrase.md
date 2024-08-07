# Expressions


The event table often requires one or more of the following to capture the features of contract.

- A **Phrase** that represents a value calculated from one or more assets. e.g. calculating the barrier condition in a knock out option.
- A [Snapper](snapper.md) that represents a **path dependent calculation**, e.g. calculating returns in an equity cliquet.

# Phrase

A Phrase is defined with three parameters.

 - **type**, which must be "phrase"
 - **inp**, a list of inputs to the phrase **fn**. An input can be an asset, such as "SPX", whose value comes from the model. It can also be a snap which has been stored as a result of previous snapper operation. It can also be another phrase.
 - **fn**, a python function that takes a list of inputs, and returns a list of outputs. The length of expected inputs list must match the length of **inp**, while the length of the output list must be exactly one.


e.g. for a Down-and-Out Barrier Option the knock out condition `ko` is defined as
```py

def ko_fn(inputs):
    [S] = inputs
    return [S < barrier]

"ko": {
    "type": "phrase",
    "inp": [asset_name],
    "fn": ko_fn,
}

```

and used in the timetable as an `op`
```py
      time op  quantity unit track
03/31/2024 ko       0.0  USD
```

See [Barrier Option](../examples/equity_barrier.md/#qablet_contracts.eq.barrier.OptionKO) for more on this example.

## Function Signature

The function should expect that inputs is a list of items. 

- The length of the list will match the length of **inp**.
- Each item in the list can be a float, or a 1-D numpy array of size 1 or N (where N is the number of Monte-Carlo paths, or the length of the Finite Difference grid's asset-axis).

The function should return a list of items.

- For a phrase the length of the output list must be exactly **one**, while for a snapper the length of the output list must match the length of **out**.
- Each item in the list should be a float, or a 1-D numpy array of size 1 or N. This is consistent with [numpy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html), therefore a function written using arithmetic operations like `+`, `-`, `*`, or element-wise numpy functions (e.g. `numpy.maximum`, `np.sqrt`) would satisfy the requirement.
