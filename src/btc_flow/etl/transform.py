import logging

logger = logging.getLogger(__name__)


def transform(raw: dict) -> dict:
    """Transform raw mempool API data into a flat, enriched record."""
    mempool = raw["mempool"]
    fees = raw["fees"]

    total_fee_btc = mempool["total_fee"] / 1e8
    avg_fee_rate = mempool["total_fee"] / mempool["vsize"] if mempool["vsize"] else 0

    record = {
        "extracted_at": raw["extracted_at"],
        "tx_count": mempool["count"],
        "mempool_vsize_bytes": mempool["vsize"],
        "total_fee_sats": mempool["total_fee"],
        "total_fee_btc": round(total_fee_btc, 8),
        "avg_fee_rate_sat_vb": round(avg_fee_rate, 4),
        "fee_fastest_sat_vb": fees["fastestFee"],
        "fee_half_hour_sat_vb": fees["halfHourFee"],
        "fee_hour_sat_vb": fees["hourFee"],
        "fee_economy_sat_vb": fees["economyFee"],
        "fee_minimum_sat_vb": fees["minimumFee"],
    }

    logger.info(
        "Transformed record: %d txs, avg fee=%.4f sat/vB",
        record["tx_count"],
        record["avg_fee_rate_sat_vb"],
    )
    return record
