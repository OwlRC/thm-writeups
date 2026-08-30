# 👤 Missing Person

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Missing Person](https://tryhackme.com/room/missingperson) |
| **Difficulty** | 🟡 Medium |
| **Category** | OSINT |
| **Tools** | browser, sherlock, exiftool, reverse image search, Google dorking |

---

## 🎯 Objective

Track a missing person across their digital footprint using OSINT — social media, image analysis, geolocation, and public records.

---

## 🔍 Methodology

### Step 1 — Username Enumeration
```bash
sherlock TARGET_USERNAME
```

Find all platforms — Twitter, Instagram, LinkedIn, Reddit, GitHub.

### Step 2 — Social Media Analysis

Look for:
- Location tags and check-ins
- Photos with identifiable backgrounds
- Bio — employer, hometown, interests
- Tagged friends and connections

### Step 3 — Image Geolocation
```bash
exiftool image.jpg | grep -i "GPS\|Latitude\|Longitude"
```

Reverse image search at: `images.google.com`, `yandex.com/images`, `tineye.com`

Cross-reference visible landmarks with Google Maps / Street View.

### Step 4 — Google Dorking
```
"target name" site:twitter.com
"target name" site:instagram.com
"target name" filetype:pdf
```

Follow each clue to the next until the flag is revealed in the OSINT trail.

---

## 📚 Lessons Learned

- Digital footprints are extensive — usernames, photos, and posts reveal location and habits
- GPS metadata in photos reveals exact coordinates — always disable geotagging
- Cross-referencing multiple OSINT sources builds a complete picture
- OSINT is legal and critical for both red team recon and blue team threat intelligence

---
*by OwlRC 🦉 | github.com/OwlRC*
