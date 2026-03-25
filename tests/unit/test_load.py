import csv

from pathlib import Path

from omegaconf import OmegaConf

from btc_flow.etl.load import FIELDS, load_csv


def test_load_csv_creates_file(csv_cfg, transformed_record):
    load_csv(cfg=csv_cfg, record=transformed_record)
    assert Path(csv_cfg.db.path).exists()


def test_load_csv_writes_header(csv_cfg, transformed_record):
    load_csv(cfg=csv_cfg, record=transformed_record)
    with open(csv_cfg.db.path) as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == FIELDS


def test_load_csv_writes_record(csv_cfg, transformed_record):
    load_csv(cfg=csv_cfg, record=transformed_record)
    with open(csv_cfg.db.path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["tx_count"] == str(transformed_record["tx_count"])


def test_load_csv_appends_multiple_records(csv_cfg, transformed_record):
    ROWS_EXPECTED = 2
    load_csv(cfg=csv_cfg, record=transformed_record)
    load_csv(cfg=csv_cfg, record=transformed_record)
    with open(csv_cfg.db.path) as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == ROWS_EXPECTED


def test_load_csv_header_written_once(csv_cfg, transformed_record):
    load_csv(cfg=csv_cfg, record=transformed_record)
    load_csv(cfg=csv_cfg, record=transformed_record)
    with open(csv_cfg.db.path) as f:
        lines = f.readlines()
    header_count = sum(1 for line in lines if "extracted_at" in line and "tx_count" in line)
    assert header_count == 1


def test_load_csv_creates_parent_dirs(tmp_path, transformed_record):
    cfg = OmegaConf.create(
        {
            "db": {
                "type": "csv",
                "path": str(tmp_path / "nested" / "dir" / "mempool.csv"),
            }
        }
    )
    load_csv(cfg=cfg, record=transformed_record)
    assert Path(cfg.db.path).exists()
