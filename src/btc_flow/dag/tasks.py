from collections.abc import Callable

from airflow.providers.standard.operators.python import PythonOperator


def make_task(task_id: str, python_callable: Callable) -> PythonOperator:
    return PythonOperator(
        task_id=task_id,
        python_callable=python_callable,
    )
