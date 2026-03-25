from typing import Any
from unittest.mock import MagicMock

import pytest

from omegaconf import OmegaConf, DictConfig

# NOTE:
# Pytest discovers fixtures automatically without explicit imports.
# Pytest injects them by name, looking specifically for "conftest.py".


@pytest.fixture
def raw_data() -> dict[str, Any]:
    """Sample raw API response."""
    return {
        "mempool": {
            "count": 17099,
            "vsize": 10875630,
            "total_fee": 4110130,
            "fee_histogram": [],
        },
        "fees": {
            "fastestFee": 3,
            "halfHourFee": 2,
            "hourFee": 1,
            "economyFee": 1,
            "minimumFee": 1,
        },
        "extracted_at": "2026-03-22T18:00:00+00:00",
    }


@pytest.fixture
def transformed_record() -> dict[str, Any]:
    """Sample transformed record."""
    return {
        "extracted_at": "2026-03-22T18:00:00+00:00",
        "tx_count": 17099,
        "mempool_vsize_bytes": 10875630,
        "total_fee_sats": 4110130,
        "total_fee_btc": 0.04110130,
        "avg_fee_rate_sat_vb": 0.3780,
        "fee_fastest_sat_vb": 3,
        "fee_half_hour_sat_vb": 2,
        "fee_hour_sat_vb": 1,
        "fee_economy_sat_vb": 1,
        "fee_minimum_sat_vb": 1,
    }


@pytest.fixture
def csv_cfg(tmp_path) -> DictConfig:
    """Hydra-like config for CSV loading."""
    return OmegaConf.create(
        {
            "db": {
                "type": "csv",
                "path": str(tmp_path / "mempool.csv"),
            }
        }
    )


@pytest.fixture
def integration_cfg() -> DictConfig:
    return OmegaConf.create(
        {
            "api": {
                "base_url": "https://mempool.space/api",
                "timeout": 10,
            }
        }
    )


@pytest.fixture
def pg_cfg() -> DictConfig:
    return OmegaConf.create(
        {
            "db": {
                "type": "postgres",
                "host": "localhost",
                "port": 5432,
                "database": "btcflow",
                "user": "btcflow",
                "password": "btcflow",
                "table": "mempool_stats",
            }
        }
    )


@pytest.fixture
def mock_conn() -> MagicMock:
    mock = MagicMock()
    mock.__enter__ = MagicMock(return_value=mock)
    mock.__exit__ = MagicMock(return_value=False)
    mock.cursor.return_value.__enter__ = MagicMock(return_value=mock.cursor.return_value)
    mock.cursor.return_value.__exit__ = MagicMock(return_value=False)
    return mock
