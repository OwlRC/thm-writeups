# 👁️ Neighbour

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Neighbour](https://tryhackme.com/room/neighbour) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | Browser, Burp Suite |

---

## 🎯 Objective

Exploit an IDOR (Insecure Direct Object Reference) vulnerability to access another user's account.

---

## 🔍 Reconnaissance

Navigate to `http://TARGET_IP` — a simple login page is presented.

**Default credentials work:** `guest:guest`

---

## 💥 Exploitation — IDOR

After logging in as guest the URL changes to:
```
http://TARGET_IP/profile.php?user=guest
```

Modifying the `user` parameter:
```
http://TARGET_IP/profile.php?user=admin
```

Access granted to the admin profile — flag is displayed on the page.

---

## 📚 Lessons Learned

- IDOR is one of the OWASP Top 10 most critical vulnerabilities
- Always test URL parameters — change user IDs, usernames, and object references
- Predictable identifiers (guest → admin) are the most obvious IDOR targets
- Burp Suite's Repeater makes it easy to modify and replay requests

---
*by OwlRC 🦉 | github.com/OwlRC*
