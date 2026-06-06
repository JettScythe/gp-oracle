"""Smoke test: fetch a live oracle message, verify its signature, parse it.

This is the only test we have that exercises real signed data, so it's
our source of truth for whether the Schnorr verifier is correct.
"""

from gp_oracle import (
    OracleClient,
    parse_price_message,
    verify_message_signature,
)

PUBKEY = "02d09db08af1ff4e8453919cc866a4be427d7bfe18f2c05e5444c196fcf6fd2818"


def test_live_message_verifies_and_parses():
    with OracleClient() as oracle:
        msgs = oracle.get_oracle_messages(PUBKEY, count=1)

    assert len(msgs) == 1
    m = msgs[0]

    # The point of this whole project: the signature must verify.
    assert verify_message_signature(m["message"], m["signature"], m["publicKey"])

    # And the parser must yield sensible values.
    price = parse_price_message(m["message"])
    assert price.message_timestamp > 0
    assert price.message_sequence >= 0
    assert price.price_sequence >= 0
    assert 0 < price.price_value < 1_000_000  # sanity bound

