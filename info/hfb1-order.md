# 🔑 HFB1: Order

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [HFB1: Order](https://tryhackme.com/room/hfb1order) |
| **Difficulty** | ℹ️ Easy |
| **Category** | Cryptography, XOR Cipher |
| **Event** | Hackfest Bonus 1 — Cipher series |
| **Tools** | Python, CyberChef |

---

## 🎯 Objective

Crack a XOR cipher given the ciphertext. Recover the key and decrypt the message to find the flag.

---

## 💥 Exploitation — Known-Plaintext XOR Attack

```python
ciphertext = bytes.fromhex("PASTE_HEX_HERE")
known = b"THM{"

# Recover key bytes using known plaintext
key_partial = bytes([ciphertext[i] ^ known[i] for i in range(4)])
print("Key fragment:", key_partial)

# Extend key (XOR keys often repeat)
key = key_partial + bytes([ciphertext[4] ^ ord("}")])

# Decrypt full message
decrypted = bytes([ciphertext[i] ^ key[i % len(key)] for i in range(len(ciphertext))])
print("Decrypted:", decrypted)
```

Or use **CyberChef** → XOR Brute Force with known plaintext `THM{`.

---

## 📚 Lessons Learned

- XOR is reversible: `ciphertext XOR plaintext = key`
- Known-plaintext attacks recover the key from even a few known bytes
- CTF flag formats (`THM{`) are reliable known-plaintext sources
- Repeating XOR keys are weak — key length found via Hamming distance analysis

---
*by OwlRC 🦉 | github.com/OwlRC*
