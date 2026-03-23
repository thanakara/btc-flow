from omegaconf import DictConfig

from btc_flow.etl.load import load_csv
from btc_flow.core.config import load_cfg
from btc_flow.etl.extract import extract
from btc_flow.etl.transform import transform

# TODO: load_cfg(overrides=["db=postgres"])
cfg: DictConfig = load_cfg()


def run_extract(**context) -> None:
    raw = extract(cfg=cfg)
    context["ti"].xcom_push(key="raw", value=raw)


def run_transform(**context) -> None:
    raw = context["ti"].xcom_pull(key="raw", task_ids="extract")
    record = transform(raw)
    context["ti"].xcom_push(key="record", value=record)


def run_load(**context) -> None:
    record = context["ti"].xcom_pull(key="record", task_ids="transform")
    load_csv(cfg=cfg, record=record)
