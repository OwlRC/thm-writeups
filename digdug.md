# 🪱 DigDug

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [DigDug](https://tryhackme.com/room/digdug) |
| **Difficulty** | 🟢 Easy |
| **Category** | DNS, Networking |
| **Tools** | dig, nslookup, host |

---

## 🎯 Objective

Practice DNS enumeration techniques to extract information from a misconfigured DNS server allowing zone transfers.

---

## 🔍 Enumeration

Basic DNS lookup:
```bash
nslookup TARGET_IP
dig TARGET_IP

# Reverse lookup
dig -x TARGET_IP
```

Trying a DNS zone transfer (AXFR):
```bash
dig axfr @TARGET_IP givemetheflag.com
```

A successful zone transfer dumps all DNS records for the domain — revealing hostnames, IP addresses, mail servers, and hidden subdomains.

**Flag found in a TXT record within the zone transfer output.**

---

## 📚 Lessons Learned

- DNS zone transfers (AXFR) should be restricted to authorized secondary DNS servers only
- A misconfigured DNS server leaks the entire domain's record set to any requester
- Always test `dig axfr @nameserver domain.com` during external recon
- TXT records often contain sensitive info — API keys, verification tokens, flags

---
*by OwlRC 🦉 | github.com/OwlRC*
