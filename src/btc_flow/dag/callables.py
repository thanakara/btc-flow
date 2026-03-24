from omegaconf import DictConfig

from btc_flow.etl.load import load_csv, load_postgres
from btc_flow.core.config import load_cfg
from btc_flow.etl.extract import extract
from btc_flow.etl.transform import transform

# TODO: Dynamic switch of db:
# 1. `load_cfg(overrides=["db=postgres"])` OR:
# 2. Manually change config.yaml && `load_cfg()`
cfg: DictConfig = load_cfg()

LOADERS = {
    "csv": load_csv,
    "postgres": load_postgres,
}


def run_extract(**context) -> None:
    raw = extract(cfg=cfg)
    context["ti"].xcom_push(key="raw", value=raw)


def run_transform(**context) -> None:
    raw = context["ti"].xcom_pull(key="raw", task_ids="extract")
    record = transform(raw)
    context["ti"].xcom_push(key="record", value=record)


def run_load(**context) -> None:
    record = context["ti"].xcom_pull(key="record", task_ids="transform")
    loader = LOADERS.get(cfg.db.type)
    if loader is None:
        raise ValueError(f"Unknown db type: {cfg.db.type}")
    loader(cfg=cfg, record=record)
