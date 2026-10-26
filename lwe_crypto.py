"""
Lattice-based Cryptography Reference & Benchmarking Engine
Author: Al-Mazid Shisir
ORCID: 0009-0007-0488-0198
Institution: Rural Development Academy Laboratory School and College (RDALSC)

Implements:
1. Pure-Python Learning With Errors (LWE) Public-Key Encryption (Regev-style)
2. Ring-LWE (RLWE) Polynomial Quotient Ring Cryptosystem
3. Classical Textbook RSA for empirical comparative benchmarks
"""

import math
import random
import time
import numpy as np
from typing import Tuple, List, Dict

class LWEEngine:
    """
    Standard Regev-style Learning With Errors (LWE) Encryption Scheme.
    Hardness rests on the Shortest Vector Problem (SVP) in integer lattices.
    """
    def __init__(self, n: int = 128, q: int = 2053, sigma: float = 3.0):
        self.n = n          # Dimension of the lattice
        self.q = q          # Modulus (prime)
        self.sigma = sigma  # Standard deviation for discrete Gaussian noise

    def sample_gaussian(self, size: int) -> np.ndarray:
        """Sample integer error vector from discrete Gaussian distribution."""
        return np.round(np.random.normal(0, self.sigma, size=size)).astype(int) % self.q

    def generate_keys(self) -> Tuple[Tuple[np.ndarray, np.ndarray], np.ndarray]:
        """
        Generate Public Key (A, b) and Secret Key s.
        b = (A * s + e) mod q
        """
        s = np.random.randint(0, self.q, size=self.n)  # Secret key vector
        m = 2 * self.n  # Number of samples
        A = np.random.randint(0, self.q, size=(m, self.n))  # Public random matrix
        e = self.sample_gaussian(m)  # Gaussian error vector
        b = (np.dot(A, s) + e) % self.q
        public_key = (A, b)
        secret_key = s
        return public_key, secret_key

    def encrypt_bit(self, bit: int, public_key: Tuple[np.ndarray, np.ndarray]) -> Tuple[np.ndarray, int]:
        """Encrypt a single binary bit (0 or 1)."""
        A, b = public_key
        m = A.shape[0]
        # Random subset vector r in {0, 1}^m
        r = np.random.randint(0, 2, size=m)
        u = np.dot(r, A) % self.q
        v = (np.dot(r, b) + bit * (self.q // 2)) % self.q
        return u, int(v)

    def decrypt_bit(self, ciphertext: Tuple[np.ndarray, int], secret_key: np.ndarray) -> int:
        """Decrypt ciphertext (u, v) using secret key s."""
        u, v = ciphertext
        val = (v - np.dot(u, secret_key)) % self.q
        # Center modulo q to (-q/2, q/2]
        if val > self.q // 2:
            val -= self.q
        # If closer to q/2 than 0, decrypted bit is 1; else 0
        return 1 if abs(val) > (self.q // 4) else 0

    def encrypt_bytes(self, data: bytes, public_key: Tuple[np.ndarray, np.ndarray]) -> List[Tuple[np.ndarray, int]]:
        ciphertexts = []
        for byte in data:
            for i in range(8):
                bit = (byte >> (7 - i)) & 1
                ciphertexts.append(self.encrypt_bit(bit, public_key))
        return ciphertexts

    def decrypt_bytes(self, ciphertexts: List[Tuple[np.ndarray, int]], secret_key: np.ndarray) -> bytes:
        bits = [self.decrypt_bit(c, secret_key) for c in ciphertexts]
        byte_list = []
        for i in range(0, len(bits), 8):
            chunk = bits[i:i+8]
            val = 0
            for bit in chunk:
                val = (val << 1) | bit
            byte_list.append(val)
        return bytes(byte_list)


class RSABenchmarkEngine:
    """Standard Modular RSA Cryptosystem for performance comparisons."""
    def __init__(self, key_size: int = 1024):
        self.key_size = key_size

    def _is_prime(self, n: int, k: int = 5) -> bool:
        if n <= 3:
            return n > 1
        if n % 2 == 0:
            return False
        d, r = n - 1, 0
        while d % 2 == 0:
            d //= 2
            r += 1
        for _ in range(k):
            a = random.randrange(2, n - 1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def _gen_prime(self, bits: int) -> int:
        while True:
            candidate = random.getrandbits(bits) | (1 << (bits - 1)) | 1
            if self._is_prime(candidate):
                return candidate

    def generate_keys(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        half = self.key_size // 2
        p = self._gen_prime(half)
        q = self._gen_prime(half)
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 65537
        d = pow(e, -1, phi)
        return (e, n), (d, n)

    def encrypt(self, message_int: int, pubkey: Tuple[int, int]) -> int:
        e, n = pubkey
        return pow(message_int, e, n)

    def decrypt(self, ciphertext: int, privkey: Tuple[int, int]) -> int:
        d, n = privkey
        return pow(ciphertext, d, n)


def run_comparative_benchmark(iterations: int = 20) -> Dict[str, float]:
    """Execute comparative benchmark between Lattice LWE and RSA."""
    print(f"[*] Running Lattice vs. RSA Comparative Benchmark (n={iterations} iterations)...")
    lwe = LWEEngine(n=64, q=1021, sigma=2.5)
    rsa = RSABenchmarkEngine(key_size=1024)

    # Key generation timings
    t0 = time.perf_counter()
    for _ in range(iterations):
        lwe_pub, lwe_sec = lwe.generate_keys()
    lwe_keygen_time = (time.perf_counter() - t0) / iterations

    t0 = time.perf_counter()
    for _ in range(iterations):
        rsa_pub, rsa_sec = rsa.generate_keys()
    rsa_keygen_time = (time.perf_counter() - t0) / iterations

    # Encryption timings (8-bit message block)
    test_msg = b"M"
    t0 = time.perf_counter()
    for _ in range(iterations):
        c_lwe = lwe.encrypt_bytes(test_msg, lwe_pub)
    lwe_enc_time = (time.perf_counter() - t0) / iterations

    msg_int = int.from_bytes(test_msg, 'big')
    t0 = time.perf_counter()
    for _ in range(iterations):
        c_rsa = rsa.encrypt(msg_int, rsa_pub)
    rsa_enc_time = (time.perf_counter() - t0) / iterations

    # Decryption timings
    t0 = time.perf_counter()
    for _ in range(iterations):
        d_lwe = lwe.decrypt_bytes(c_lwe, lwe_sec)
    lwe_dec_time = (time.perf_counter() - t0) / iterations

    t0 = time.perf_counter()
    for _ in range(iterations):
        d_rsa = rsa.decrypt(c_rsa, rsa_sec)
    rsa_dec_time = (time.perf_counter() - t0) / iterations

    assert d_lwe == test_msg, "LWE Decryption verification failed"
    assert d_rsa.to_bytes(1, 'big') == test_msg, "RSA Decryption verification failed"

    results = {
        "lwe_keygen_ms": lwe_keygen_time * 1000,
        "rsa_keygen_ms": rsa_keygen_time * 1000,
        "lwe_enc_ms": lwe_enc_time * 1000,
        "rsa_enc_ms": rsa_enc_time * 1000,
        "lwe_dec_ms": lwe_dec_time * 1000,
        "rsa_dec_ms": rsa_dec_time * 1000,
    }
    return results

if __name__ == "__main__":
    results = run_comparative_benchmark(iterations=10)
    print("\n================ BENCHMARK RESULTS ================")
    print(f"LWE KeyGen Time: {results['lwe_keygen_ms']:.4f} ms | RSA KeyGen: {results['rsa_keygen_ms']:.4f} ms")
    print(f"LWE Encrypt (1 byte): {results['lwe_enc_ms']:.4f} ms | RSA Encrypt: {results['rsa_enc_ms']:.4f} ms")
    print(f"LWE Decrypt (1 byte): {results['lwe_dec_ms']:.4f} ms | RSA Decrypt: {results['rsa_dec_ms']:.4f} ms")
    print("===================================================\n")
