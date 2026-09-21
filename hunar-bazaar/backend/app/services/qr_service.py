"""
Bridges Python to the C++ AES-128 encryption module (see /crypto) that
produces the encrypted payload embedded in each delivery QR code.

The C++ side is a small CLI (qr_crypto) built via CMake:
    qr_crypto encrypt <hex_key> <plaintext>   -> prints hex ciphertext
    qr_crypto decrypt <hex_key> <hex_ciphertext> -> prints plaintext

Keeping the cipher in C++ mirrors the resume line ("custom AES-128 encryption
system in C++") and lets the same binary be reused by a delivery-agent CLI
or an embedded device, not just this API.
"""
import asyncio
import json

from app.core.config import settings


async def _run_binary(*args: str) -> str:
    proc = await asyncio.create_subprocess_exec(
        settings.qr_crypto_bin,
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"qr_crypto failed: {stderr.decode().strip()}")
    return stdout.decode().strip()


async def encrypt_delivery_payload(order_id: str, delivery_agent_id: str, expiry_ts: int) -> str:
    """Returns hex ciphertext to be rendered as a QR code."""
    plaintext = json.dumps(
        {"order_id": order_id, "agent_id": delivery_agent_id, "exp": expiry_ts}
    )
    return await _run_binary("encrypt", settings.aes_qr_key_hex, plaintext)


async def decrypt_delivery_payload(ciphertext_hex: str) -> dict:
    """Called at the doorstep scan; role-gated to buyer/delivery_agent/admin in the router."""
    plaintext = await _run_binary("decrypt", settings.aes_qr_key_hex, ciphertext_hex)
    return json.loads(plaintext)
