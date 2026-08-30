import os
import requests
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
THM_USERNAME = "OwlRC"

CATEGORIES = {
    "easy":   {"label": "Easy",   "icon": "🟢"},
    "medium": {"label": "Medium", "icon": "🟡"},
    "hard":   {"label": "Hard",   "icon": "🔴"},
    "info":   {"label": "Info",   "icon": "ℹ️"},
}

def get_thm_total_rooms():
    for url in [
        "https://tryhackme.com/api/v2/search?kind=room&difficulty=all&limit=1",
        "https://tryhackme.com/api/hacktivities?type=room&difficulty=all&page=1&limit=1",
    ]:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "OwlRC/readme-bot"})
            if r.status_code == 200:
                d = r.json()
                t = d.get("data", {}).get("total") or d.get("total")
                if t: return int(t)
        except Exception:
            pass
    return 800

def count_writeups():
    counts, rooms = {}, {}
    for cat in CATEGORIES:
        folder = REPO_ROOT / cat
        if folder.exists():
            files = sorted([f for f in folder.glob("*.md") if f.name != "README.md"])
            counts[cat] = len(files)
            rooms[cat] = [f.stem.replace("-", " ").title() for f in files]
        else:
            counts[cat] = 0
            rooms[cat] = []
    return counts, rooms

def room_table(room_list, cat):
    if not room_list:
        return "_No writeups yet_\n"
    rows = []
    for i in range(0, len(room_list), 3):
        chunk = room_list[i:i+3]
        cells = [f"[{r}]({cat}/{r.lower().replace(' ', '-')}.md)" for r in chunk]
        while len(cells) < 3:
            cells.append("")
        rows.append("| " + " | ".join(cells) + " |")
    return "| Room | Room | Room |\n|---|---|---|\n" + "\n".join(rows) + "\n"

def build_readme(counts, rooms, thm_total):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = sum(counts.values())
    pct = round(total / thm_total * 100, 1) if thm_total else 0

    # Simple clean progress bar — no box drawing, no emoji widths
    filled = int((total / thm_total) * 50) if thm_total else 0
    bar = "█" * filled + "░" * (50 - filled)

    readme = f"""<div align="center">

# 🧠 OwlRC — TryHackMe Writeups

[![TryHackMe](https://img.shields.io/badge/TryHackMe-OwlRC-red?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/{THM_USERNAME})
[![Rooms](https://img.shields.io/badge/Rooms_Completed-{total}-39d353?style=for-the-badge)](https://github.com/OwlRC/thm-writeups)
[![THM Total](https://img.shields.io/badge/THM_Total-{thm_total}_Rooms-58a6ff?style=for-the-badge)](https://tryhackme.com)
[![Auto](https://img.shields.io/badge/Auto_Updated-Daily-c9a84c?style=for-the-badge)](https://github.com/OwlRC/thm-writeups/actions)

---

### Progress — {total} / {thm_total} rooms &nbsp;·&nbsp; {pct}%

`{bar}`

| 🟢 Easy | 🟡 Medium | 🔴 Hard | ℹ️ Info |
|:---:|:---:|:---:|:---:|
| **{counts['easy']}** | **{counts['medium']}** | **{counts['hard']}** | **{counts['info']}** |

*Last updated: {now}*

</div>

---

## 📋 Methodology

Every writeup follows this structure:

```
Recon → Enumeration → Exploitation → Post-Exploitation → Lessons Learned
```

---

## 🟢 Easy — {counts['easy']} writeups

{room_table(rooms['easy'], 'easy')}

---

## 🟡 Medium — {counts['medium']} writeups

{room_table(rooms['medium'], 'medium')}

---

## 🔴 Hard — {counts['hard']} writeups

{room_table(rooms['hard'], 'hard')}

---

## ℹ️ Info / CTF Events — {counts['info']} writeups

{room_table(rooms['info'], 'info')}

---

## 🛠️ Tools

![Kali](https://img.shields.io/badge/Kali_Linux-557C94?style=flat-square&logo=kali-linux&logoColor=white)
![Nmap](https://img.shields.io/badge/nmap-0E83CD?style=flat-square)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat-square)
![Metasploit](https://img.shields.io/badge/Metasploit-2596CD?style=flat-square)
![Hashcat](https://img.shields.io/badge/Hashcat-121011?style=flat-square)
![BloodHound](https://img.shields.io/badge/BloodHound-FF0000?style=flat-square)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat-square)

---

> ⚠️ All writeups are based on authorized TryHackMe lab environments.
> Never use these techniques on systems you do not own or have written permission to test.

*🤖 README auto-generated daily — push a new writeup and this updates itself.*

**by OwlRC 🦉**
"""
    return readme

def main():
    print("[*] Counting writeups...")
    counts, rooms = count_writeups()
    print(f"    easy={counts['easy']} medium={counts['medium']} hard={counts['hard']} info={counts['info']}")
    print("[*] Fetching THM total...")
    thm_total = get_thm_total_rooms()
    print(f"    THM total: {thm_total}")
    print("[*] Generating README...")
    readme = build_readme(counts, rooms, thm_total)
    (REPO_ROOT / "README.md").write_text(readme, encoding="utf-8")
    print("[+] Done")

if __name__ == "__main__":
    main()
