# gp-oracle

[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)]()


Python client for the General Protocols / oracles.cash oracle network.

Features:

- Parse oracle price messages
- Verify BCH Schnorr signatures
- Fetch current oracle prices
- Access all documented oracles.cash REST endpoints
- No blockchain node required
- Python 3.14+

---

## Installation


```bash
uv add git+https://github.com/jettscythe/gp-oracle.git
```

or 

```bash
pip install git+https://github.com/jettscythe/gp-oracle.git
```

### Development

```bash
git clone https://github.com/jettscythe/gp-oracle.git
cd gp-oracle

uv sync
uv pip install -e .
```

---

## Quick Start

Fetch the current BCH/USD price:

```python
from gp_oracle import get_bch_usd_price

price = get_bch_usd_price()

print(price)
```

Example output:

```text
213.78
```

---

## OracleClient

```python
from gp_oracle import OracleClient, OracleId

with OracleClient() as client:
    price = client.latest_price(
        OracleId.USD_BCH
    )

print(price.decimal_value)
```

---

## Verify Oracle Signatures

Every oracle message is signed by the oracle operator.

```python
from gp_oracle import (
    OracleClient,
    OracleId,
    verify_message_signature,
)

with OracleClient() as client:
    message = client.latest_message(
        OracleId.USD_BCH
    )

valid = verify_message_signature(
    message.message,
    message.signature,
    message.public_key,
)

print(valid)
```

Output:

```text
True
```

---

## Parse Price Messages

```python
from gp_oracle import parse_price_message

msg = parse_price_message(
    "936a246a85dc190069dc1900a3530000"
)

print(msg.message_timestamp)
print(msg.price_sequence)
print(msg.price_value)
```

---

## Supported Oracles

### BCH Markets

| Pair | Identifier |
|--------|--------|
| USD/BCH |`OracleId.USD_BCH` |
| EUR/BCH |`OracleId.EUR_BCH` |
| CNY/BCH |`OracleId.CNY_BCH` |
| PHP/BCH |`OracleId.PHP_BCH` |
| AUD/BCH |`OracleId.AUD_BCH` |
| INR/BCH |`OracleId.INR_BCH` |
| XAU/BCH |`OracleId.XAU_BCH` |
| XAG/BCH |`OracleId.XAG_BCH` |
| BTC/BCH |`OracleId.BTC_BCH` |
| ETH/BCH |`OracleId.ETH_BCH` |
| DOGE/BCH |`OracleId.DOGE_BCH` |

---

## Get Oracle Messages

```python
from gp_oracle import OracleClient, OracleId

with OracleClient() as client:
    messages = client.get_oracle_messages(
        OracleId.USD_BCH,
        count=10,
    )

print(messages)
```

---

## Oracle Metadata

```python
with OracleClient() as client:
    metadata = client.get_oracle_metadata(
        OracleId.USD_BCH
    )

print(metadata)
```

---

## Historical Prices

```python
with OracleClient() as client:
    prices = client.get_prices(
        limit=100
    )

print(prices)
```

---

## Price Graph Data

```python
from time import time

now = int(time())

with OracleClient() as client:
    points = client.get_price_graph_points(
        OracleId.USD_BCH,
        min_message_timestamp=now - 86400,
        max_message_timestamp=now,
        aggregation_period=3600,
    )

print(points)
```

---

## Real-Time Updates

```python
from gp_oracle import OracleClient

with OracleClient() as client:
    for message in client.stream_messages():
        print(message)
```

---

## Message Format

Price messages are encoded as four little-endian 32-bit unsigned integers:

```text
messageTimestamp
messageSequence
priceSequence
priceValue
```

Example:

```text
936a246a85dc190069dc1900a3530000
```

Parses as:

```python
PriceMessage(
    message_timestamp=1780771475,
    message_sequence=1694853,
    price_sequence=1694825,
    price_value=21411,
)
```

---

## Signature Verification

The library verifies Bitcoin Cash Schnorr signatures over secp256k1.

Verification is performed locally.

No trusted third party is required.

---

## Testing

Run the test suite:

```bash
uv run pytest
```

---

## Development

Install locally:

```bash
uv pip install -e .
```

Run a quick sanity check:

```bash
uv run python -c "from gp_oracle import get_bch_usd_price; print(get_bch_usd_price())"
```

---

## Disclaimer

This library is not affiliated with General Protocols.

Oracle data is provided by the operators of the oracle network.

Always independently verify signatures before relying on oracle data in production systems.

---

## Credits

- General Protocols
- oracles.cash
- Bitcoin Cash
