# 🔐 W1seGuy

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [W1seGuy](https://tryhackme.com/room/w1seguy) |
| **Difficulty** | 🟢 Easy |
| **Category** | Cryptography |
| **Tools** | Python, CyberChef |

---

## 🎯 Objective

Recover a flag encrypted with a XOR cipher by analysing the ciphertext and recovering the key.

---

## 🔍 Analysis

The challenge provides an encrypted string. XOR cipher is reversible — if you know part of the plaintext you can recover the key.

Flags on TryHackMe always start with `THM{` — this is known plaintext.

---

## 💥 Key Recovery

Using Python to XOR the known plaintext against the ciphertext:
```python
ciphertext = bytes.fromhex("PASTE_HEX_HERE")

known_plain = b"THM{"

# Recover first 4 bytes of key
key_partial = bytes([ciphertext[i] ^ known_plain[i] for i in range(4)])
print("Partial key:", key_partial)

# XOR keys often repeat — extend to full length
# If key length is 5:
key = key_partial + bytes([ciphertext[4] ^ ord("}")])  # guess closing brace

# Decrypt full message
decrypted = bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])
print("Decrypted:", decrypted)
```

Alternatively use CyberChef:
1. Input → From Hex
2. XOR Brute Force with known plaintext `THM{`

**Flag recovered via XOR key analysis.**

---

## 📚 Lessons Learned

- XOR encryption is symmetric and completely reversible with the key
- Known-plaintext attacks work when you know even a small portion of the original message
- CTF flags always start with a known prefix — use this as your known plaintext
- CyberChef's XOR Brute Force feature automates single-byte key recovery

---
*by OwlRC 🦉 | github.com/OwlRC*
