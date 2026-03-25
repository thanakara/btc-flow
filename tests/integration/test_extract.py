from datetime import datetime

from btc_flow.etl.extract import extract, fetch_fee_estimates, fetch_mempool_stats


def test_fetch_mempool_stats_has_required_keys(integration_cfg):
    result = fetch_mempool_stats(cfg=integration_cfg)
    assert "count" in result
    assert "vsize" in result
    assert "total_fee" in result
    assert "fee_histogram" in result


def test_fetch_mempool_stats_values_are_positive(integration_cfg):
    result = fetch_mempool_stats(cfg=integration_cfg)
    assert result["count"] >= 0
    assert result["vsize"] >= 0
    assert result["total_fee"] >= 0


def test_fetch_fee_estimates_has_required_keys(integration_cfg):
    result = fetch_fee_estimates(cfg=integration_cfg)
    assert "fastestFee" in result
    assert "halfHourFee" in result
    assert "hourFee" in result
    assert "economyFee" in result
    assert "minimumFee" in result


def test_fetch_fee_estimates_values_are_positive(integration_cfg):
    result = fetch_fee_estimates(cfg=integration_cfg)
    assert result["fastestFee"] >= 1
    assert result["minimumFee"] >= 1


def test_extract_returns_combined_dict(integration_cfg):
    result = extract(cfg=integration_cfg)
    assert "mempool" in result
    assert "fees" in result
    assert "extracted_at" in result


def test_extract_extracted_at_is_iso_format(integration_cfg):
    result = extract(cfg=integration_cfg)
    datetime.fromisoformat(result["extracted_at"])
