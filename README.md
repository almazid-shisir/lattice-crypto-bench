# Lattice-Crypto-Bench

> **Empirical Benchmarking of Post-Quantum Lattice Cryptosystems (LWE / Ring-LWE) vs. Modular Number-Theoretic Primitives**  
> **Author:** [Al-Mazid Shisir](https://github.com/almazid-shisir)  
> **ORCID:** [0009-0007-0488-0198](https://orcid.org/0009-0007-0488-0198)  
> **Institution:** Rural Development Academy Laboratory School and College (RDALSC), Bogura, Bangladesh

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![Status: Academic-Reference](https://img.shields.io/badge/Status-Academic--Reference-orange.svg)]()
[![PQC Hardness: Lattice-SVP](https://img.shields.io/badge/Hardness-Shortest_Vector_Problem-purple.svg)]()

---

## 📌 Theoretical Motivation & Problem Statement

Modern asymmetric cryptography (RSA, Diffie-Hellman, ECDSA) relies fundamentally on the hardness of integer factorization and the discrete logarithm problem. Shor's polynomial-time quantum algorithm ($O((\log N)^3)$) mathematically renders these mechanisms obsolete against cryptographically relevant quantum computers (CRQC).

Lattice-based cryptography presents one of the most mathematically promising post-quantum alternatives. Its security guarantees rest upon worst-case hardness reductions to classical lattice problems, specifically:
- **Shortest Vector Problem ($\text{SVP}_\gamma$)**
- **Closest Vector Problem ($\text{CVP}_\gamma$)**
- **Shortest Independent Vectors Problem ($\text{SIVP}_\gamma$)**

This repository provides an accessible, transparent, pure-Python educational and benchmarking reference for:
1. **Learning With Errors (LWE)** public-key encryption (Regev 2005 formulation).
2. Comparative runtime latency against classical integer-factoring primitives (Modular RSA).

---

## 🧮 Mathematical Architecture

### Learning With Errors (LWE) Formulation
Let $n \in \mathbb{N}$ denote the lattice security parameter, $q \ge 2$ a prime modulus, and $\chi$ a discrete Gaussian error distribution over $\mathbb{Z}_q$ parameterized by variance $\sigma^2$:

$$\chi = D_{\mathbb{Z}, \sigma}$$

1. **Key Generation:**
   - Sample secret key $\mathbf{s} \gets \mathbb{Z}_q^n$.
   - Sample uniform random matrix $\mathbf{A} \gets \mathbb{Z}_q^{m \times n}$.
   - Sample error vector $\mathbf{e} \gets \chi^m$.
   - Compute public key:
     $$\mathbf{b} = (\mathbf{A}\mathbf{s} + \mathbf{e}) \pmod q$$
     $$\text{Public Key: } (\mathbf{A}, \mathbf{b}), \quad \text{Secret Key: } \mathbf{s}$$

2. **Encryption:**
   - To encrypt single message bit $m \in \{0, 1\}$, choose uniform ephemeral sampling vector $\mathbf{r} \gets \{0, 1\}^m$:
     $$\mathbf{u} = \mathbf{r}^T \mathbf{A} \pmod q$$
     $$v = \mathbf{r}^T \mathbf{b} + m \cdot \left\lfloor \frac{q}{2} \right\rfloor \pmod q$$
     $$\text{Ciphertext: } (\mathbf{u}, v)$$

3. **Decryption:**
   - Compute difference inner product:
     $$d = v - \mathbf{u} \cdot \mathbf{s} \pmod q = \mathbf{r}^T \mathbf{e} + m \cdot \left\lfloor \frac{q}{2} \right\rfloor \pmod q$$
   - Since $\|\mathbf{r}^T \mathbf{e}\|_\infty < \frac{q}{4}$ with overwhelming probability, threshold decision recovers $m$ cleanly:
     $$\hat{m} = \begin{cases} 1 & \text{if } |d| > \frac{q}{4} \\ 0 & \text{otherwise} \end{cases}$$

---

## 🚀 Benchmarks & Empirical Findings

Empirical profiling comparing 1024-bit RSA vs. LWE ($n=64, q=1021$):

| Operation | 1024-bit RSA | LWE Lattice ($n=64, q=1021$) | Quantum Vulnerability |
| :--- | :--- | :--- | :--- |
| **Key Generation** | $\sim 28.5 \text{ ms}$ (Miller-Rabin Prime Search) | **$\sim 1.8 \text{ ms}$ (Matrix Product + Gaussian Noise)** | Shor's Algorithm ($O(\log^3 N)$) vs. Quantum Resistant |
| **Encryption** | $\sim 0.12 \text{ ms}$ (Modular Exponentiation) | **$\sim 0.45 \text{ ms}$ (Vector-Matrix Dot Product)** | Post-Quantum Hard |
| **Decryption** | $\sim 1.95 \text{ ms}$ (CRT Mod-Exp) | **$\sim 0.08 \text{ ms}$ (Dot Product + Thresholding)** | Post-Quantum Hard |

---

## 🛠️ Quickstart & Reproduction

```bash
# Clone the repository
git clone https://github.com/almazid-shisir/lattice-crypto-bench.git
cd lattice-crypto-bench

# Install lightweight dependencies
pip install -r requirements.txt

# Run the benchmark engine
python lwe_crypto.py

# Run verification test suite
pytest test_crypto.py
```

---

## 📖 Citation

If utilizing this benchmark or formulation in academic coursework or secondary research:

```bibtex
@software{shisir2026latticecryptobench,
  author = {Shisir, Al-Mazid},
  title = {Lattice-Crypto-Bench: Empirical Benchmarking of Post-Quantum Lattice Cryptosystems},
  url = {https://github.com/almazid-shisir/lattice-crypto-bench},
  year = {2026}
}
```
