# 🗺️ Nmap: The Basics (nmap01)

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Nmap: The Basics](https://tryhackme.com/room/nmap01) |
| **Difficulty** | 🟢 Easy |
| **Category** | Networking, Enumeration |
| **Tools** | nmap, arp-scan, masscan |

---

## 🎯 Objective

Learn how Nmap discovers live hosts and enumerates services using ARP, ICMP, TCP, and UDP probes before performing port scans.

---

## 📖 Key Concepts

### Host Discovery Methods

| Method | Command | Use Case |
|---|---|---|
| ARP Scan | `nmap -PR TARGET` | Same subnet — most reliable locally |
| ICMP Echo | `nmap -PE TARGET` | Cross-subnet ping |
| ICMP Timestamp | `nmap -PP TARGET` | Bypass ICMP echo blocks |
| TCP SYN | `nmap -PS22,80,443 TARGET` | Common ports probe |
| TCP ACK | `nmap -PA22,80,443 TARGET` | Bypass SYN filters |
| UDP | `nmap -PU53,161 TARGET` | UDP services discovery |

### Target Specification

```bash
# Single host
nmap 10.10.10.10

# Range
nmap 10.10.10.1-20

# Subnet
nmap 10.10.10.0/24

# From file
nmap -iL targets.txt

# Exclude hosts
nmap 10.10.10.0/24 --exclude 10.10.10.5
```

### Common Scan Types

```bash
# SYN scan (default, requires root)
sudo nmap -sS TARGET

# TCP connect scan (no root needed)
nmap -sT TARGET

# UDP scan
sudo nmap -sU TARGET

# Service/version detection
nmap -sV TARGET

# OS detection
sudo nmap -O TARGET

# Full aggressive scan
nmap -A TARGET

# All ports
nmap -p- TARGET

# Specific ports
nmap -p 22,80,443,8080 TARGET
```

### Output Formats

```bash
nmap -oN output.txt TARGET    # Normal
nmap -oX output.xml TARGET    # XML
nmap -oG output.gnmap TARGET  # Grepable
nmap -oA output TARGET        # All formats
```

---

## 🛠️ Additional Tools

```bash
# ARP scan — faster for local networks
sudo arp-scan -l
sudo arp-scan 10.10.10.0/24

# Masscan — extremely fast large network scanning
sudo masscan 10.10.10.0/24 -p 80,443 --rate=1000
```

---

## 📚 Lessons Learned

- ARP scans only work within the same subnet — ICMP and TCP probes work across routers
- SYN scans require root privileges but are faster and stealthier than connect scans
- Always use `-oA` to save results — you'll want to reference them later
- Combine nmap with masscan for large network ranges: masscan for speed, nmap for detail

---
*by OwlRC 🦉 | github.com/OwlRC*
