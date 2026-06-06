from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class PriceMessage:
    message_timestamp: int
    message_sequence: int
    price_sequence: int
    price_value: int

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(
            self.message_timestamp,
            tz=timezone.utc,
        )

    @property
    def value(self) -> int:
        return self.price_value

    @property
    def decimal_value(self) -> float:
        return self.price_value / 100.0


@dataclass(frozen=True, slots=True)
class OracleMessage:
    message: str
    signature: str
    public_key: str

    def verify(self) -> bool:
        from .schnorr import verify_message_signature

        return verify_message_signature(
            self.message,
            self.signature,
            self.public_key,
        )

    @property
    def price(self) -> PriceMessage:
        from .parser import parse_price_message

        return parse_price_message(self.message)
