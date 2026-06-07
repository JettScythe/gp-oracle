from .client import OracleClient
from anyhedge.oracle import UsdEM2


def get_bch_usd_price() -> float:
    with OracleClient() as client:
        return client.latest_message(UsdEM2.public_key).price_standardUnits_per_bch


__all__ = [
    "OracleClient",
    "get_bch_usd_price",
]
