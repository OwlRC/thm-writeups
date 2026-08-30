# 🎮 HFB1: The Game

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [HFB1: The Game](https://tryhackme.com/room/hfb1thegame) |
| **Difficulty** | ℹ️ Easy |
| **Category** | Reverse Engineering |
| **Event** | Hackfest Bonus 1 — Cipher series |
| **Tools** | strings, grep, file |

---

## 🎯 Objective

Cipher has hidden secrets inside a Tetris game executable (`Tetrix.exe`) — 93MB, suspiciously large for Tetris. Find what's inside.

---

## 💥 Exploitation

```bash
file Tetrix.exe
# PE32 executable for MS Windows

strings Tetrix.exe | grep -E "(THM\{|FLAG\{)"
# THM{REDACTED}
```

Flag found immediately. Confirm uniqueness:

```bash
strings Tetrix.exe | grep "THM{" | sort -u
```

---

## 📚 Lessons Learned

- `strings` is always the first tool on an unknown binary — finds embedded plaintext in seconds
- Abnormal file sizes signal embedded data or hidden payloads
- Flags stored as plaintext in executables are trivially extractable
- Always `strings` before attempting full reverse engineering

---
*by OwlRC 🦉 | github.com/OwlRC*
