import logging

import hydra

from omegaconf import OmegaConf, DictConfig


@hydra.main(config_path="../conf", config_name="config", version_base="1.3")
def main(cfg: DictConfig):
    log = logging.getLogger(__name__)
    OmegaConf.resolve(cfg)

    log.debug("__on_main_begin__")
    log.info(OmegaConf.to_yaml(cfg))
    log.debug("__on_main_end__")


if __name__ == "__main__":
    main()
