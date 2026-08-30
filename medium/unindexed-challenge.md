# 🔍 Unindexed Challenge

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Unindexed Challenge](https://tryhackme.com/room/unindexedchallenge) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web |
| **Tools** | gobuster, ffuf, curl, Burp Suite |

---

## 🎯 Objective
Discover hidden web content that has been intentionally excluded from search engine indexing.

---

## 🔍 Enumeration

```bash
# Directory brute force
gobuster dir -u http://TARGET_IP \
  -w /usr/share/wordlists/dirb/common.txt \
  -x php,html,txt,bak

# FUZZ with ffuf
ffuf -u http://TARGET_IP/FUZZ \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -mc 200,301,302

# Check robots.txt and sitemap
curl http://TARGET_IP/robots.txt
curl http://TARGET_IP/sitemap.xml
```

---

## 💥 Exploitation

Discovering hidden paths via content discovery — flag found within an unlinked, unindexed page.

Common hidden locations to check:
```
/admin
/backup
/dev
/test
/.git
/config
/api
/v1, /v2
```

---

## 📚 Lessons Learned
- Content hidden from search engines is still accessible if the path is guessed or brute forced
- Security through obscurity is not security — proper access controls are required
- `robots.txt` lists pages webmasters DON'T want indexed — check it always
- `/.git` exposed on web servers leaks source code — check for this in all web assessments

---
*by OwlRC 🦉 | github.com/OwlRC*
