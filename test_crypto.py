import pytest
from lwe_crypto import LWEEngine, RSABenchmarkEngine

def test_lwe_bit_encryption():
    engine = LWEEngine(n=64, q=1021, sigma=2.0)
    pub, sec = engine.generate_keys()
    for bit in [0, 1, 0, 1, 1, 0]:
        ct = engine.encrypt_bit(bit, pub)
        dec = engine.decrypt_bit(ct, sec)
        assert dec == bit

def test_lwe_byte_string_encryption():
    engine = LWEEngine(n=64, q=1021, sigma=2.0)
    pub, sec = engine.generate_keys()
    message = b"SHISIR_CRYPTO_2026"
    ct = engine.encrypt_bytes(message, pub)
    dec = engine.decrypt_bytes(ct, sec)
    assert dec == message

def test_rsa_roundtrip():
    rsa = RSABenchmarkEngine(key_size=512)
    pub, priv = rsa.generate_keys()
    msg = 42
    ct = rsa.encrypt(msg, pub)
    dec = rsa.decrypt(ct, priv)
    assert dec == msg
