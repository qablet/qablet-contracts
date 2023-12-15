# Define the timetable struct

import pyarrow as pa

# timetable is a dictionary with the following fields:
# - events: a list of events (pyarrow struct array)
# - expressions: a dictionary of expressions (key: string, value: function)

DICT_TYPE = pa.dictionary(pa.int64(), pa.string())
EVENT_SCHEMA = pa.schema(
    [
        pa.field("track", DICT_TYPE),
        pa.field("time", pa.float64()),  # TODO: use pa.timestamp() instead?
        pa.field("op", pa.string()),  # TODO: use pa.dictionary() instead?
        pa.field("quantity", pa.float64()),
        pa.field("unit", DICT_TYPE),
    ]
)


def timetable_from_dicts(events) -> dict:
    """Create timetable from a list of dicts (recordbatch version)."""
    return {
        "events": pa.RecordBatch.from_pylist(events, schema=EVENT_SCHEMA),
        "expressions": {},
    }
