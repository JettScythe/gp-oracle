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

## Signature Verification

The library verifies Bitcoin Cash Schnorr signatures over secp256k1.

Verification is performed locally.

No trusted third party is required.


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
