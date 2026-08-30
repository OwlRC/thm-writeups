# 🔏 Confidential

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Confidential](https://tryhackme.com/room/confidential) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web, OSINT |
| **Tools** | browser, zbar-tools, pdfinfo, strings |

---

## 🎯 Objective

Extract hidden information from a PDF document containing embedded QR codes and metadata.

---

## 💥 Exploitation

**Step 1 — Download and inspect the PDF:**
```bash
# Check metadata
pdfinfo document.pdf
exiftool document.pdf

# Extract strings
strings document.pdf | grep -i "flag\|THM"
```

**Step 2 — Extract and scan the QR code:**
```bash
# Extract images from PDF
pdfimages document.pdf images/

# Scan QR code
zbarimg images/image.png
# or
python3 -c "
import cv2
img = cv2.imread('image.png')
detector = cv2.QRCodeDetector()
data, _, _ = detector.detectAndDecode(img)
print(data)
"
```

**Flag found in the QR code data.**

---

## 📚 Lessons Learned

- PDFs can embed QR codes, hidden text, metadata, and even executable code
- Always check metadata — author names, creation tools, GPS coordinates can be revealing
- `strings` on binary files often reveals plaintext information
- QR codes in documents are a common way to embed hidden data in CTFs and in the wild

---
*by OwlRC 🦉 | github.com/OwlRC*
