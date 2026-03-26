import logging

from btc_flow.etl.load import FIELDS
from btc_flow.etl.models import MempoolRecord
from btc_flow.etl.validate import validate


def test_validate_returns_mempool_record(transformed_record):
    result = validate(transformed_record)
    assert isinstance(result, MempoolRecord)


def test_validate_returns_none_on_invalid_record():
    result = validate({"invalid": "data"})
    assert result is None


def test_validate_negative_tx_count(transformed_record):
    transformed_record["tx_count"] = -1
    result = validate(transformed_record)
    assert result is None


def test_validate_negative_vsize(transformed_record):
    transformed_record["mempool_vsize_bytes"] = -1
    result = validate(transformed_record)
    assert result is None


def test_validate_negative_total_fee_sats(transformed_record):
    transformed_record["total_fee_sats"] = -1
    result = validate(transformed_record)
    assert result is None


def test_validate_negative_total_fee_btc(transformed_record):
    transformed_record["total_fee_btc"] = -1.0
    result = validate(transformed_record)
    assert result is None


def test_validate_negative_avg_fee_rate(transformed_record):
    transformed_record["avg_fee_rate_sat_vb"] = -1.0
    result = validate(transformed_record)
    assert result is None


def test_validate_logs_warning_on_failure(transformed_record, caplog):
    transformed_record["tx_count"] = -1
    with caplog.at_level(logging.WARNING):
        validate(transformed_record)
    assert "Validation failed" in caplog.text


def test_validate_model_dump_matches_fields(transformed_record):
    result = validate(transformed_record)
    assert result is not None
    dumped = result.model_dump()
    for field in FIELDS:
        assert field in dumped


def test_validate_zero_fees_is_valid(transformed_record):
    transformed_record["avg_fee_rate_sat_vb"] = 0.0
    transformed_record["total_fee_btc"] = 0.0
    result = validate(transformed_record)
    assert result is not None
