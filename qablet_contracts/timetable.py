# Define the timetable schema

from abc import ABC, abstractmethod
from typing import Dict, List

import pyarrow as pa

DICT_TYPE = pa.dictionary(pa.int64(), pa.string())

# Event Schema for the timetable, using timestamp for time
TS_TYPE = pa.timestamp("ms", tz="UTC")
TS_EVENT_SCHEMA = pa.schema(
    [
        pa.field("time", TS_TYPE),
        pa.field("op", DICT_TYPE),
        pa.field("quantity", pa.float64()),
        pa.field("unit", DICT_TYPE),
        pa.field("track", DICT_TYPE),
    ]
)


def py_to_ts(py_dt):
    """Convert a python datetime to a pyarrow timestamp (milliseconds)."""
    return pa.scalar(py_dt, type=TS_TYPE)


class Contract(ABC):
    """A base class for contracts."""

    @abstractmethod
    def timetable(self): ...

    def to_string(self, index=False) -> str:
        df = self.timetable()["events"].to_pandas()
        df["time"] = df["time"].dt.strftime(
            "%m/%d/%Y"
        )  # replace timestamp by Date
        return df.to_string(index=index)

    def print_events(self):
        print(self.to_string(index=False))


class EventsMixin(Contract):
    """A mixin class for contracts that generates a timetable from events list.
    A derived class needs to implement the events method that returns a list of dicts,
    and the expressions method (optional) that returns a dictionary of expressions, batches, and snappers."""

    @abstractmethod
    def events(self) -> List[Dict]: ...

    def expressions(self) -> Dict:
        return {}

    def timetable(self):
        return {
            "events": pa.RecordBatch.from_pylist(
                self.events(), schema=TS_EVENT_SCHEMA
            ),
            "expressions": self.expressions(),
        }
