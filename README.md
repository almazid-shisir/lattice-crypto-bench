# Lattice-Crypto-Bench

Benchmarking Learning With Errors (LWE) and Ring-LWE post-quantum primitives against modular RSA.

Author: Al-Mazid Shisir  
Affiliation: Rural Development Academy Laboratory School and College (RDALSC), Bogura, Bangladesh  
ORCID: [0009-0007-0488-0198](https://orcid.org/0009-0007-0488-0198)  
License: MIT  

---

## Overview

Public-key systems like RSA and Elliptic Curve Cryptography rely on integer factorization and discrete logarithms. Both break under polynomial-time quantum algorithms such as Shor's algorithm.

Lattice-based cryptography provides an alternative based on worst-case hardness assumptions, including:
- Shortest Vector Problem (SVP)
- Closest Vector Problem (CVP)
- Shortest Independent Vectors Problem (SIVP)

This repository contains a reference implementation in Python of:
1. Regev-style Learning With Errors (LWE) encryption.
2. Direct execution time comparisons between LWE and textbook modular RSA across key generation, encryption, and decryption steps.

---

## Method

### Learning With Errors (LWE)

Let $n$ represent the lattice security parameter, $q$ a prime modulus, and $\chi$ a discrete Gaussian error distribution with standard deviation $\sigma$:

1. **Key Generation:**
   - Secret key: vector $\mathbf{s} \in \mathbb{Z}_q^n$.
   - Public matrix: $\mathbf{A} \in \mathbb{Z}_q^{m \times n}$.
   - Error vector: $\mathbf{e} \in \chi^m$.
   - Public key: $(\mathbf{A}, \mathbf{b})$ where $\mathbf{b} = (\mathbf{A}\mathbf{s} + \mathbf{e}) \pmod q$.

2. **Encryption:**
   - For bit $m \in \{0, 1\}$, sample binary vector $\mathbf{r} \in \{0, 1\}^m$:
     $$\mathbf{u} = \mathbf{r}^T \mathbf{A} \pmod q$$
     $$v = \mathbf{r}^T \mathbf{b} + m \cdot \lfloor q/2 \rfloor \pmod q$$
   - Ciphertext: $(\mathbf{u}, v)$.

3. **Decryption:**
   - Compute $d = v - \mathbf{u} \cdot \mathbf{s} \pmod q$.
   - Decode: $m = 1$ if $|d| > q/4$, else $0$.

---

## Empirical Benchmark (n=64, q=1021 vs. 1024-bit RSA)

| Stage | 1024-bit RSA | LWE ($n=64, q=1021$) |
| :--- | :--- | :--- |
| Key Generation | ~28.5 ms | ~1.8 ms |
| Encryption (1 byte) | ~0.12 ms | ~0.45 ms |
| Decryption (1 byte) | ~1.95 ms | ~0.08 ms |

---

## Running the Code

```bash
git clone https://github.com/almazid-shisir/lattice-crypto-bench.git
cd lattice-crypto-bench
pip install -r requirements.txt
python lwe_crypto.py
```

---

## Citation

```bibtex
@software{shisir2026latticecryptobench,
  author = {Shisir, Al-Mazid},
  title = {Lattice-Crypto-Bench: Empirical Benchmarking of Post-Quantum Lattice Cryptosystems},
  url = {https://github.com/almazid-shisir/lattice-crypto-bench},
  year = {2026}
}
```
