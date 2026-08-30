# 🔐 Checkpoint

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Checkpoint](https://tryhackme.com/room/checkpoint) |
| **Difficulty** | 🔴 Hard |
| **Category** | Network Security, Firewall Analysis |
| **Tools** | nmap, Wireshark, custom scripts |

---

## 🎯 Objective
Analyse and bypass firewall rules to access restricted network segments and services.

---

## 🔍 Reconnaissance

```bash
# Identify open ports through firewall
nmap -sS -p- --min-rate 5000 TARGET_IP

# Identify filtered ports
nmap -sA TARGET_IP  # ACK scan reveals firewall rules

# UDP scanning
sudo nmap -sU --top-ports 100 TARGET_IP
```

---

## 💥 Firewall Bypass Techniques

```bash
# Fragment packets to evade deep packet inspection
nmap -f TARGET_IP

# Use specific source ports (DNS port 53 often allowed)
nmap --source-port 53 TARGET_IP

# Decoy scan
nmap -D RND:10 TARGET_IP

# Slow scan to evade rate-based detection
nmap -T1 --scan-delay 2s TARGET_IP

# IPv6 (if IPv4 is filtered)
nmap -6 TARGET_IP6_ADDRESS
```

---

## 📚 Lessons Learned
- Firewalls filter based on rules — understanding those rules allows targeted bypass
- ACK scans reveal stateful firewall rules by differentiating filtered vs closed ports
- Source port manipulation exploits firewall rules that trust specific ports (DNS, HTTP)
- Defense in depth means multiple security controls, not just a perimeter firewall

---
*by OwlRC 🦉 | github.com/OwlRC*
