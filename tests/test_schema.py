from qablet_contracts.timetable import TS_EVENT_SCHEMA


def test_old_schema():
    assert TS_EVENT_SCHEMA.names == ["time", "op", "quantity", "unit", "track"]
