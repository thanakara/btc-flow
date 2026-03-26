import logging

from pydantic import ValidationError

from btc_flow.etl.models import MempoolRecord

logger = logging.getLogger(__name__)


def validate(record: dict) -> MempoolRecord | None:
    """Validate transformed record. Returns None if invalid."""
    try:
        return MempoolRecord(**record)
    except ValidationError as e:
        logger.warning("Validation failed, skipping record: %s", e)
        return None
