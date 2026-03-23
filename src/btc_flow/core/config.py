import os

from pathlib import Path

from hydra import compose, initialize_config_dir
from omegaconf import DictConfig

# AIRFLOW_HOME is injected into the container: /opt/airflow as ENV.
# In order to work both locally and inside the container:
CONFIG_DIR = str(Path(os.environ.get("AIRFLOW_HOME", Path(__file__).parents[3])) / "src" / "conf")


def load_cfg(overrides: list[str] | None = None) -> DictConfig:
    """Load Hydra config from the standard config directory."""
    with initialize_config_dir(config_dir=CONFIG_DIR, version_base=None):
        return compose(config_name="config", overrides=overrides or [])
