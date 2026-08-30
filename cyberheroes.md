# 🦸 CyberHeroes

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [CyberHeroes](https://tryhackme.com/room/cyberheroes) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | Browser DevTools |

---

## 🎯 Objective

Find credentials hidden in the JavaScript source code to log in and capture the flag.

---

## 💥 Exploitation

Navigating to `http://TARGET_IP` shows a login page. Opening browser DevTools (`F12`) → **Sources** tab reveals the JavaScript handling authentication:

```javascript
function authenticate() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    if (username === 'h3ck3rBoi' && password === 'superS3cur3Passw0rd!') {
        window.location.href = '/flag.html';
    }
}
```

**Credentials found:** `h3ck3rBoi:superS3cur3Passw0rd!`

Logging in redirects to `/flag.html` which contains the flag.

---

## 📚 Lessons Learned

- Never perform authentication logic client-side — it can always be viewed and bypassed
- JavaScript source code is fully visible to users — never store credentials there
- Always view page source and JavaScript files when testing web applications
- Client-side validation is for UX only — never rely on it for security

---
*by OwlRC 🦉 | github.com/OwlRC*
