"""Parse General Protocols oracle price messages.

A price message is 16 bytes packing four little-endian uint32 values:
    messageTimestamp, messageSequence, priceSequence, priceValue
"""

from __future__ import annotations
import struct
from .models import PriceMessage

_PRICE_STRUCT = struct.Struct("<IIII")


def parse_price_message(message: str | bytes) -> PriceMessage:
    raw = bytes.fromhex(message) if isinstance(message, str) else message
    if len(raw) != _PRICE_STRUCT.size:
        raise ValueError(
            f"price message must be {_PRICE_STRUCT.size} bytes, got {len(raw)}"
        )
    ts, mseq, pseq, price = _PRICE_STRUCT.unpack(raw)
    return PriceMessage(ts, mseq, pseq, price)
