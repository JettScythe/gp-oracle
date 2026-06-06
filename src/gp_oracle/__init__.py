from .client import OracleClient
from .constants import OracleId
from .parser import parse_price_message
from .schnorr import verify_message_signature


def get_bch_usd_price() -> float:
    with OracleClient() as client:
        return client.latest_price(OracleId.USD_BCH).decimal_value


__all__ = [
    "OracleClient",
    "OracleId",
    "parse_price_message",
    "verify_message_signature",
    "get_bch_usd_price",
]

