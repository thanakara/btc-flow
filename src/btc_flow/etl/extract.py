import logging

from datetime import UTC, datetime

import requests

from omegaconf import DictConfig

logger = logging.getLogger(__name__)


def fetch_mempool_stats(cfg: DictConfig) -> dict:
    """Fetch current mempool statistics."""
    url = f"{cfg.api.base_url}/mempool"
    response = requests.get(url, timeout=cfg.api.timeout)
    response.raise_for_status()
    data = response.json()
    logger.info("Fetched mempool stats: %d transactions in mempool", data["count"])
    return data


def fetch_fee_estimates(cfg: DictConfig) -> dict:
    """Fetch current recommended fee estimates."""
    url = f"{cfg.api.base_url}/v1/fees/recommended"
    response = requests.get(url, timeout=cfg.api.timeout)
    response.raise_for_status()
    data = response.json()
    logger.info("Fetched fee estimates: fastest=%d sat/vB", data["fastestFee"])
    return data


# This is the single entrypoint the DAG will call
def extract(cfg: DictConfig) -> dict:
    """Run full extraction and return combined raw data."""
    logger.info("Starting extraction from mempool.space")
    return {
        "mempool": fetch_mempool_stats(cfg=cfg),
        "fees": fetch_fee_estimates(cfg=cfg),
        "extracted_at": datetime.now(UTC).isoformat(),
    }
