from datetime import UTC, datetime, timedelta

from airflow import DAG

from btc_flow.dag.tasks import make_task
from btc_flow.dag.callables import cfg, run_load, run_extract, run_transform

with DAG(
    dag_id=cfg.dag.id,
    schedule=cfg.dag.schedule,
    catchup=cfg.dag.catchup,
    max_active_runs=cfg.dag.max_active_runs,
    tags=list(cfg.dag.tags),
    default_args={
        "start_date": datetime(2026, 3, 22, tzinfo=UTC),
        "retries": cfg.dag.retries,
        "retry_delay": timedelta(seconds=cfg.dag.retry_delay_seconds),
    },
) as dag:
    tasks = [
        make_task(task_id="extract", python_callable=run_extract),
        make_task(task_id="transform", python_callable=run_transform),
        make_task(task_id="load", python_callable=run_load),
    ]

    for idx in range(len(tasks) - 1):
        tasks[idx] >> tasks[idx + 1]
