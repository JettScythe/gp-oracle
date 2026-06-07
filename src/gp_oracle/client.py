"""Client for the General Protocols / oracles.cash REST API."""

from __future__ import annotations
from .schnorr import verify_message_signature
from typing import Any

import httpx
from anyhedge.oracle import Pricepoint, PublicKey

DEFAULT_BASE_URL = "https://oracles.generalprotocols.com"


class OracleClient:
    def __init__(
        self, base_url: str = DEFAULT_BASE_URL, client: httpx.Client | None = None
    ) -> None:
        self._base = base_url.rstrip("/")
        self._client = client or httpx.Client(base_url=self._base, timeout=30.0)

    def list_oracles(self) -> list[dict[str, Any]]:
        r = self._client.get("/api/v1/oracles")
        r.raise_for_status()
        return r.json()["oracles"]

    def get_oracle_messages(
        self,
        public_key: PublicKey | None = None,
        *,
        count: int | None = None,
        min_message_timestamp: int | None = None,
        max_message_timestamp: int | None = None,
        min_message_sequence: int | None = None,
        max_message_sequence: int | None = None,
        min_data_sequence: int | None = None,
        max_data_sequence: int | None = None,
        min_metadata_type: int | None = None,
        max_metadata_type: int | None = None,
    ) -> list[dict[str, Any]]:
        params = {
            "publicKey": public_key,
            "count": count,
            "minMessageTimestamp": min_message_timestamp,
            "maxMessageTimestamp": max_message_timestamp,
            "minMessageSequence": min_message_sequence,
            "maxMessageSequence": max_message_sequence,
            "minDataSequence": min_data_sequence,
            "maxDataSequence": max_data_sequence,
            "minMetadataType": min_metadata_type,
            "maxMetadataType": max_metadata_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        r = self._client.get("/api/v1/oracleMessages", params=params)
        r.raise_for_status()
        return r.json()["oracleMessages"]

    def get_oracle_metadata(
        self,
        public_key: PublicKey | None = None,
        *,
        max_message_sequence: int | None = None,
        count: int | None = None,
    ) -> list[dict[str, Any]]:
        params = {
            "publicKey": public_key,
            "maxMessageSequence": max_message_sequence,
            "count": count,
        }
        params = {k: v for k, v in params.items() if v is not None}
        r = self._client.get("/api/v1/oracleMetadata", params=params)
        r.raise_for_status()
        return r.json()["oracleMetadata"]

    def get_prices(
        self, *, max_price_sequence: int | None = None, limit: int | None = None
    ) -> list[dict[str, Any]]:
        params = {"maxPriceSequence": max_price_sequence, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        r = self._client.get("/api/v1/prices", params=params)
        r.raise_for_status()
        return r.json()["prices"]

    # --- Price visualization ---
    def get_price_graph_points(
        self,
        public_key: PublicKey | None = None,
        *,
        min_message_timestamp: int,
        max_message_timestamp: int,
        aggregation_period: int,
    ) -> list[dict[str, Any]]:
        params = {
            "publicKey": public_key,
            "minMessageTimestamp": min_message_timestamp,
            "maxMessageTimestamp": max_message_timestamp,
            "aggregationPeriod": aggregation_period,
        }
        r = self._client.get("/api/v2/priceGraphPoints", params=params)
        r.raise_for_status()
        return r.json()["priceGraphPoints"]

    def get_price_graph_image(self, public_key: str, **kwargs: Any) -> str:
        params = {"publicKey": public_key, **kwargs}
        r = self._client.get("/art/v0/priceGraphImage", params=params)
        r.raise_for_status()
        return r.text  # SVG

    # --- Misc ---
    def get_recovery_progress(self, public_key: PublicKey) -> dict[str, Any]:
        r = self._client.get(
            "/api/v1/recoveryProgress", params={"publicKey": public_key}
        )
        r.raise_for_status()
        return r.json()["recoveryProgress"]

    # --- Real-time (SSE) ---
    def stream_messages(self):
        """Yield parsed SSE message dicts: {message, signature, publicKey}."""
        import json

        with self._client.stream("GET", "/sse/v1/messages") as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if line.startswith("data:"):
                    yield json.loads(line[len("data:") :].strip())

    def latest_message(
        self,
        public_key: PublicKey,
    ) -> Pricepoint:
        r = self._client.get(
            "/api/v1/oracleMessages",
            params={
                "publicKey": public_key,
                "count": 1,
            },
        )
        r.raise_for_status()
        msg = r.json()["oracleMessages"][0]
        pp = Pricepoint(
            oracle_pubkey=PublicKey(msg["publicKey"]),
            message=msg["message"],
            signature=msg["signature"],
        )
        assert verify_message_signature(pp.message, pp.signature, public_key)
        return pp

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> OracleClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
