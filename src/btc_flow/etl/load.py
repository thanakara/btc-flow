import csv
import logging

from pathlib import Path

from omegaconf import DictConfig

logger = logging.getLogger(__name__)


FIELDS = [
    "extracted_at",
    "tx_count",
    "mempool_vsize_bytes",
    "total_fee_sats",
    "total_fee_btc",
    "avg_fee_rate_sat_vb",
    "fee_fastest_sat_vb",
    "fee_half_hour_sat_vb",
    "fee_hour_sat_vb",
    "fee_economy_sat_vb",
    "fee_minimum_sat_vb",
]


def load_csv(cfg: DictConfig, record: dict) -> None:
    """Append a transformed record to the CSV file."""
    # TODO: Override this in the future: overrides=["db=postgres"]
    CSV_PATH = Path(cfg.db.path)
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_exists = CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

    logger.info("Appended record to %s", CSV_PATH)
