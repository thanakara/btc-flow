from btc_flow.etl.transform import transform


def test_transform_returns_flat_record(raw_data):
    record = transform(raw=raw_data)
    assert isinstance(record, dict)


def test_transform_fields(raw_data, transformed_record):
    record = transform(raw_data)
    assert record.keys() == transformed_record.keys()


def test_transform_tx_count(raw_data):
    record = transform(raw_data)
    assert record["tx_count"] == raw_data["mempool"]["count"]


def test_transform_total_fee_btc(raw_data):
    record = transform(raw_data)
    expected = round(raw_data["mempool"]["total_fee"] / 1e8, 8)
    assert record["total_fee_btc"] == expected


def test_transform_avg_fee_rate(raw_data):
    record = transform(raw_data)
    expected = round(raw_data["mempool"]["total_fee"] / raw_data["mempool"]["vsize"], 4)
    assert record["avg_fee_rate_sat_vb"] == expected


def test_transform_fee_estimates(raw_data):
    record = transform(raw_data)
    assert record["fee_fastest_sat_vb"] == raw_data["fees"]["fastestFee"]
    assert record["fee_half_hour_sat_vb"] == raw_data["fees"]["halfHourFee"]
    assert record["fee_hour_sat_vb"] == raw_data["fees"]["hourFee"]
    assert record["fee_economy_sat_vb"] == raw_data["fees"]["economyFee"]
    assert record["fee_minimum_sat_vb"] == raw_data["fees"]["minimumFee"]


def test_transform_extracted_at_preserved(raw_data):
    record = transform(raw_data)
    assert record["extracted_at"] == raw_data["extracted_at"]


def test_transform_zero_vsize(raw_data):
    """Edge case: zero vsize should not raise ZeroDivisionError."""
    raw_data["mempool"]["vsize"] = 0
    record = transform(raw_data)
    assert record["avg_fee_rate_sat_vb"] == 0.0
