# 🕵️ HFB1: Hide and Seek

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [HFB1: Hide and Seek](https://tryhackme.com/room/hfb1hideandseek) |
| **Difficulty** | ℹ️ Easy |
| **Category** | Linux, Persistence, Forensics |
| **Event** | Hackfest Bonus 1 — Cipher series |
| **Tools** | SSH, ps, systemctl, crontab, find |

---

## 🎯 Objective

A Linux box has been compromised. Find the post-compromise persistence mechanisms hidden by the attacker. A hint poem describes each technique.

---

## 🔍 Hint Poem

```
Time is on my side, always running like clockwork.         → Cron job
A secret handshake gets me in every time.                  → SSH authorized_keys
Whenever you set the stage, I make my entrance.            → bashrc / bash_profile
I run with the big dogs, booting up alongside the system.  → Systemd service
I love welcome messages.                                   → MOTD / login script
```

---

## 💥 Finding All Persistence Mechanisms

```bash
# Cron jobs
crontab -l && cat /etc/crontab && ls /etc/cron.*

# SSH authorized keys
cat ~/.ssh/authorized_keys
cat /root/.ssh/authorized_keys

# Shell startup scripts
cat ~/.bashrc && cat ~/.bash_profile && cat /etc/profile

# Systemd services — look for cipher.service
systemctl list-units --type=service
cat /etc/systemd/system/cipher.service

# MOTD
ls /etc/update-motd.d/ && cat /etc/motd

# Running processes
ps -eFH | grep -v "\["
```

Each mechanism reveals part of the flag or the attacker's technique.

---

## 📚 Lessons Learned

- Attackers use multiple persistence mechanisms simultaneously — check all of them
- Unknown services (like `cipher.service`) are immediate red flags on Linux
- SSH `authorized_keys` modification is silent and survives reboots
- MOTD scripts in `/etc/update-motd.d/` run as root on every login

---
*by OwlRC 🦉 | github.com/OwlRC*
