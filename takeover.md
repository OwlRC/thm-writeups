# 🌐 Takeover

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Takeover](https://tryhackme.com/room/takeover) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | nmap, subfinder, dig, curl |

---

## 🎯 Objective

Identify and exploit a subdomain takeover vulnerability.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
```

Enumerate subdomains:
```bash
# Add target to /etc/hosts first
echo "TARGET_IP futurevera.thm" >> /etc/hosts

# Subfinder
subfinder -d futurevera.thm

# Gobuster DNS
gobuster dns -d futurevera.thm -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

**Found subdomains:**
- `blog.futurevera.thm`
- `support.futurevera.thm`

---

## 💥 Exploitation — Subdomain Takeover

Checking the SSL certificate of `support.futurevera.thm`:
```bash
curl -v https://support.futurevera.thm 2>&1 | grep -i "subject\|issuer"
```

The certificate reveals an additional subdomain. Navigating to it shows a provider error page indicating the CNAME points to an unclaimed resource — this is a subdomain takeover opportunity.

The flag is embedded in the SSL certificate's Subject Alternative Names (SAN) field.

---

## 📚 Lessons Learned

- Subdomain takeover occurs when a CNAME points to an unclaimed external resource
- SSL certificates can reveal additional subdomains via SAN fields
- Always enumerate subdomains — they are frequently forgotten and left misconfigured
- Tools: subfinder, amass, gobuster dns, crt.sh for certificate transparency logs

---
*by OwlRC 🦉 | github.com/OwlRC*
