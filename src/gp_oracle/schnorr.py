"""Bitcoin Cash (2019) Schnorr signature verification over secp256k1.

Pure Python, no dependencies. BCH Schnorr differs from BIP-340:
  - challenge uses a plain SHA-256 (not a tagged hash)
  - challenge = SHA256(r || compressed_pubkey || message_hash)
  - validity uses the Jacobi-symbol (quadratic-residue) test on R.y
"""

from __future__ import annotations

import hashlib

# secp256k1 domain parameters
_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
_GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
_G = (_GX, _GY)


def _inv(a: int, m: int) -> int:
    return pow(a, -1, m)


def _point_add(p1, p2):
    if p1 is None:
        return p2
    if p2 is None:
        return p1
    x1, y1 = p1
    x2, y2 = p2
    if x1 == x2 and (y1 + y2) % _P == 0:
        return None
    if p1 == p2:
        m = (3 * x1 * x1) * _inv(2 * y1, _P) % _P
    else:
        m = (y2 - y1) * _inv(x2 - x1, _P) % _P
    x3 = (m * m - x1 - x2) % _P
    y3 = (m * (x1 - x3) - y1) % _P
    return (x3, y3)


def _mul(k: int, point):
    result = None
    addend = point
    while k:
        if k & 1:
            result = _point_add(result, addend)
        addend = _point_add(addend, addend)
        k >>= 1
    return result


def _decompress_pubkey(pub: bytes):
    if len(pub) != 33 or pub[0] not in (0x02, 0x03):
        raise ValueError("expected 33-byte compressed public key")
    x = int.from_bytes(pub[1:], "big")
    if x >= _P:
        raise ValueError("public key x out of range")
    rhs = (pow(x, 3, _P) + 7) % _P
    y = pow(rhs, (_P + 1) // 4, _P)  # works because P % 4 == 3
    if (y * y - rhs) % _P != 0:
        raise ValueError("point not on curve")
    if (y & 1) != (pub[0] & 1):
        y = _P - y
    return (x, y)


def _is_quadratic_residue(value: int) -> bool:
    return pow(value, (_P - 1) // 2, _P) == 1


def verify_signature(message: bytes, signature: bytes, public_key: bytes) -> bool:
    """Verify a BCH Schnorr signature over SHA256(message)."""
    if len(signature) != 64:
        raise ValueError("signature must be 64 bytes")

    r = int.from_bytes(signature[:32], "big")
    s = int.from_bytes(signature[32:], "big")
    if r >= _P or s >= _N:
        return False

    try:
        P = _decompress_pubkey(public_key)
    except ValueError:
        return False

    msg_hash = hashlib.sha256(message).digest()
    e_input = signature[:32] + public_key + msg_hash
    e = int.from_bytes(hashlib.sha256(e_input).digest(), "big") % _N

    # R = s*G - e*P
    R = _point_add(_mul(s, _G), _mul(_N - e, P))
    if R is None:
        return False
    rx, ry = R
    if not _is_quadratic_residue(ry):
        return False
    return rx == r


def verify_message_signature(
    message_hex: str, signature_hex: str, public_key_hex: str
) -> bool:
    """Hex-string convenience wrapper, mirroring the JS verifyMessageSignature."""
    return verify_signature(
        bytes.fromhex(message_hex),
        bytes.fromhex(signature_hex),
        bytes.fromhex(public_key_hex),
    )
