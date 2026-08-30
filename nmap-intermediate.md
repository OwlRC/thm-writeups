# 🗺️ Nmap: Intermediate

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Nmap: Intermediate](https://tryhackme.com/room/intermediatenmap) |
| **Difficulty** | 🟢 Easy |
| **Category** | Networking, Enumeration |
| **Tools** | nmap, NSE scripts |

---

## 🎯 Objective

Go beyond basic scanning — learn NSE scripts, timing templates, firewall evasion, and output analysis.

---

## 📖 NSE Scripts (Nmap Scripting Engine)

```bash
# Run default scripts
nmap -sC TARGET

# Run specific script
nmap --script=http-title TARGET

# Run script category
nmap --script=vuln TARGET
nmap --script=auth TARGET
nmap --script=discovery TARGET

# Multiple scripts
nmap --script=http-enum,http-methods TARGET

# Script with arguments
nmap --script=http-brute --script-args userdb=users.txt,passdb=pass.txt TARGET
```

### Useful Script Categories

| Category | Use Case |
|---|---|
| `auth` | Authentication bypass checks |
| `vuln` | Vulnerability detection |
| `exploit` | Exploitation attempts |
| `brute` | Brute force credentials |
| `discovery` | Network discovery |
| `default` | Default safe scripts |

---

## ⏱️ Timing Templates

```bash
nmap -T0 TARGET  # Paranoid — IDS evasion
nmap -T1 TARGET  # Sneaky — slow
nmap -T2 TARGET  # Polite — lower bandwidth
nmap -T3 TARGET  # Normal (default)
nmap -T4 TARGET  # Aggressive — faster
nmap -T5 TARGET  # Insane — fastest, noisy
```

---

## 🔒 Firewall Evasion

```bash
# Fragment packets
nmap -f TARGET

# Use decoys
nmap -D RND:10 TARGET
nmap -D 10.0.0.1,10.0.0.2,ME TARGET

# Source port spoofing
nmap --source-port 53 TARGET

# Append random data
nmap --data-length 200 TARGET

# Slow down scan
nmap --scan-delay 1s TARGET

# Randomize host order
nmap --randomize-hosts TARGET
```

---

## 📚 Lessons Learned

- NSE scripts turn nmap from a scanner into a vulnerability assessment tool
- `-T4` is the sweet spot for CTFs — fast without being unreliable
- Fragmentation (`-f`) is effective against basic packet inspection firewalls
- Always save output with `-oA` — you can grep grepable output for specific services

---
*by OwlRC 🦉 | github.com/OwlRC*
