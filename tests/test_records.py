"""
Tests for the envoy.records module
"""

from envoy.records import *


def test_transaction_record(transaction):
    record = Record(transaction)
    assert record.data == transaction
    assert len(record) == 15

    fields = record.fields()
    assert len(fields) == 15

    for field in fields:
        item = record[field]
        if field == "envelope_count":
            assert isinstance(item, int)

        elif field == "amount":
            assert isinstance(item, float)

        else:
            assert isinstance(item, str)

    data = record.asdict()
    assert data is not transaction


def test_transaction_record_list(transactions):
    records = RecordList(transactions)
    assert records.data == transactions
    assert len(records) == 4

    for record in records:
        assert isinstance(record, Record)

    data = records.copy()
    assert data is not transactions


def test_record_list_of_record_lists():
    records = RecordList(
        [
            [
                {"name": "Edgar Fromage", "age": 49, "profession": "Tailor"},
                {"name": "Mary Tillman", "age": 21, "profession": "Tinker"},
            ],
            [
                {"name": "Rachel Benedict", "age": 22, "profession": "Soldier"},
                {"name": "Morgan Stillton", "age": 61, "profession": "Spy"},
            ],
        ]
    )

    assert len(records) == 2
    for item in records:
        assert len(item) == 2
        assert isinstance(item, RecordList)

        for sub in item:
            assert len(item) == 2
            assert isinstance(sub, Record)


def test_record_of_record_lists():
    record = Record(
        {
            "nested": {
                "people": [
                    {"name": "Edgar Fromage", "age": 49, "profession": "Tailor"},
                    {"name": "Mary Tillman", "age": 21, "profession": "Tinker"},
                ],
                "fruits": ["apple", "pear", "orange", "grapes"],
            },
        }
    )

    assert isinstance(record["nested"], Record)
    assert isinstance(record["nested"]["people"], RecordList)
    assert isinstance(record["nested"]["fruits"], list)
