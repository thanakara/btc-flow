from datetime import datetime

from pydantic import BaseModel, field_validator


# TODO: Add more realistic model/field_validator
class MempoolRecord(BaseModel):
    extracted_at: datetime
    tx_count: int
    mempool_vsize_bytes: int
    total_fee_sats: int
    total_fee_btc: float
    avg_fee_rate_sat_vb: float
    fee_fastest_sat_vb: int
    fee_half_hour_sat_vb: int
    fee_hour_sat_vb: int
    fee_economy_sat_vb: int
    fee_minimum_sat_vb: int

    @field_validator("tx_count", "mempool_vsize_bytes", "total_fee_sats")
    @classmethod
    def must_be_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError(f"Value must be non-negative, got {v}")
        return v

    @field_validator("avg_fee_rate_sat_vb", "total_fee_btc")
    @classmethod
    def must_be_non_negative_float(cls, v: float) -> float:
        if v < 0:
            raise ValueError(f"Value must be non-negative, got {v}")
        return v
