# 🔍 OSINT Rooms

> Writeups for TryHackMe OSINT challenge rooms — by OwlRC 🦉

---

# 🐇 White Rabbit

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [White Rabbit](https://tryhackme.com/room/whiterabbit) |
| **Difficulty** | 🟡 Medium |
| **Category** | OSINT, Cryptography, Steganography |

## 💥 Approach
Chain multiple OSINT and cryptography techniques — follow the rabbit hole from one clue to the next.

**Common techniques needed:**
- Base64/ROT13/Caesar cipher decoding
- Image steganography (`steghide`, `zsteg`, `exiftool`)
- Social media username searches
- Reverse image search
- Metadata extraction from files

```bash
# Steganography
steghide extract -sf image.jpg
zsteg image.png
exiftool image.jpg

# Cipher decoding
echo "BASE64" | base64 -d
python3 -c "import codecs; print(codecs.decode('ROT13STRING', 'rot_13'))"
```

## 📚 Lessons Learned
- OSINT investigations chain clues — solve one to get to the next
- Steganography hides data in images, audio, and other media files
- Always check file metadata — GPS, author, creation date, software used

---

# 👤 Missing Person

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Missing Person](https://tryhackme.com/room/missingperson) |
| **Difficulty** | 🟡 Medium |
| **Category** | OSINT |

## 💥 Approach
Use social media OSINT, image analysis, and geolocation to track a missing person across digital footprints.

```bash
# Username enumeration across platforms
sherlock username

# Reverse image search
# Upload to: images.google.com, yandex.com/images, tineye.com

# Geolocation from image metadata
exiftool image.jpg | grep -i "GPS\|Location"

# Social media search
# Twitter/X: site:twitter.com "username"
# Instagram: site:instagram.com "username"
```

## 📚 Lessons Learned
- Digital footprints are extensive — usernames, photos, and posts reveal location and habits
- Reverse image search reveals where images were posted and can identify locations
- GPS metadata in photos is frequently overlooked — people geo-tag images without realising

---

# 🎣 Phishing Pond

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Phishing Pond](https://tryhackme.com/room/phishingpond) |
| **Difficulty** | 🟡 Medium |
| **Category** | Phishing Analysis, Threat Intelligence |

## 💥 Approach
Analyse phishing emails to identify indicators of compromise, spoofing techniques, and malicious URLs.

```bash
# Extract email headers
# Check: Return-Path, Received, DKIM-Signature, SPF

# Analyse URLs without visiting
curl -I -L "SUSPICIOUS_URL"  # check redirects
urlscan.io  # sandbox analysis
virustotal.com  # URL/file reputation

# Analyse attachments safely
# Upload to: any.run, hybrid-analysis.com
file attachment.docx
strings attachment.docx | grep -i "http\|powershell\|cmd"
```

**Red flags in phishing emails:**
- Mismatched From and Reply-To addresses
- Urgent language and pressure tactics
- Suspicious links with URL shorteners
- Attachments with macros
- Poor grammar and generic greetings

## 📚 Lessons Learned
- Email header analysis reveals the true origin of messages
- Always analyse suspicious URLs and attachments in a sandbox environment
- SPF, DKIM, and DMARC records help identify email spoofing
- Threat intelligence platforms (VirusTotal, URLScan) speed up analysis significantly

---

# 🔎 OSINT Challenge IV

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [OSINT Challenge IV](https://tryhackme.com/room/osintchallengeiv) |
| **Difficulty** | 🟡 Medium |
| **Category** | OSINT |

## 💥 Approach
Multi-source OSINT investigation combining social media, public records, and digital forensics.

**Tools and techniques:**
```bash
# Google dorking
site:target.com filetype:pdf
"target name" site:linkedin.com
intitle:"index of" "target"

# Shodan for infrastructure
shodan search "target.com"

# Certificate transparency
crt.sh — search for domain certificates

# WHOIS and DNS history
whois domain.com
dig any domain.com
viewdns.info — IP history, reverse IP

# Wayback Machine
web.archive.org — find old versions of sites
```

## 📚 Lessons Learned
- Google dorks expose sensitive files, directories, and information not meant to be public
- Certificate transparency logs reveal all issued SSL certs — useful for subdomain discovery
- WHOIS history and DNS records can reveal infrastructure changes and old IP addresses

---
*by OwlRC 🦉 | github.com/OwlRC*
