from .client import OracleClient
from anyhedge.oracle import UsdEM2, InrEM0, EurEM2, PhpEM0


def get_bch_usd_price() -> float:
    with OracleClient() as client:
        return client.latest_message(UsdEM2.public_key).price_standardUnits_per_bch


def get_bch_inr_price() -> int | float:
    with OracleClient() as client:
        return client.latest_message(InrEM0.public_key).price_standardUnits_per_bch


def get_bch_eur_price() -> float:
    with OracleClient() as client:
        return client.latest_message(EurEM2.public_key).price_standardUnits_per_bch


def get_bch_php_price() -> int | float:
    with OracleClient() as client:
        return client.latest_message(PhpEM0.public_key).price_standardUnits_per_bch


__all__ = [
    "OracleClient",
    "get_bch_usd_price",
    "get_bch_eur_price",
    "get_bch_inr_price",
    "get_bch_php_price",
]
