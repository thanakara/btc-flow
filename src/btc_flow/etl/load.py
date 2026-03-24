import csv
import logging

from pathlib import Path

import psycopg2

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

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS {table} (
    id                  SERIAL PRIMARY KEY,
    extracted_at        TIMESTAMPTZ NOT NULL,
    tx_count            INTEGER,
    mempool_vsize_bytes BIGINT,
    total_fee_sats      BIGINT,
    total_fee_btc       NUMERIC(16, 8),
    avg_fee_rate_sat_vb NUMERIC(10, 4),
    fee_fastest_sat_vb  INTEGER,
    fee_half_hour_sat_vb INTEGER,
    fee_hour_sat_vb     INTEGER,
    fee_economy_sat_vb  INTEGER,
    fee_minimum_sat_vb  INTEGER
);
"""

INSERT_SQL = """
INSERT INTO {table} ({fields})
VALUES ({placeholders});
"""


def load_csv(cfg: DictConfig, record: dict) -> None:
    """Append a transformed record to the CSV file."""
    CSV_PATH = Path(cfg.db.path)
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    file_exists = CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

    logger.info("Appended record to %s", CSV_PATH)


def load_postgres(cfg: DictConfig, record: dict) -> None:
    """Insert a transformed record into PostgreSQL."""
    # @package db:=
    db = cfg.db
    table = db.table

    conn = psycopg2.connect(
        host=db.host,
        port=db.port,
        dbname=db.database,
        user=db.user,
        password=db.password,
    )

    try:
        with conn:
            with conn.cursor() as cur:
                # NOTE: CREATE IF NOT EXISTS is important here:
                cur.execute(CREATE_TABLE_SQL.format(table=table))
                cur.execute(
                    INSERT_SQL.format(
                        table=table,
                        fields=", ".join(FIELDS),
                        placeholders=", ".join(["%s"] * len(FIELDS)),
                    ),
                    [record[f] for f in FIELDS],
                )
        logger.info("Inserted record into %s", table)
    finally:
        conn.close()
