# 💧 Water Bottle

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Water Bottle](https://tryhackme.com/room/waterbottle) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web |
| **Tools** | nmap, Burp Suite, ffuf |

---

## 🎯 Objective
Exploit a web application to find hidden flags through enumeration and web vulnerability exploitation.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP

gobuster dir -u http://TARGET_IP \
  -w /usr/share/wordlists/dirb/common.txt
```

---

## 💥 Exploitation

Inspecting the web application for common vulnerabilities:

```bash
# Check for parameter tampering
curl "http://TARGET_IP/page?id=1"
curl "http://TARGET_IP/page?id=1'"  # SQL injection test

# Check cookies
# Modify cookie values in Burp Suite

# Source code review
curl http://TARGET_IP/ | grep -i "comment\|flag\|hidden\|TODO"
```

---

## 📚 Lessons Learned
- Always enumerate web applications thoroughly before attempting exploitation
- Check all parameters — GET, POST, cookies, and headers for injection points
- Source code comments frequently contain hints, credentials, and flags
- HTTP response headers can reveal technology stack and version information

---
*by OwlRC 🦉 | github.com/OwlRC*
