import os
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

# ── Config ─────────────────────────────────────────────────
REPO_ROOT = Path(__file__).parent.parent
THM_USERNAME = "OwlRC"

CATEGORIES = {
    "easy":   {"label": "Easy",   "icon": "🟢", "color": "39d353"},
    "medium": {"label": "Medium", "icon": "🟡", "color": "e3b341"},
    "hard":   {"label": "Hard",   "icon": "🔴", "color": "f85149"},
    "info":   {"label": "Info",   "icon": "ℹ️",  "color": "58a6ff"},
}

# ── Fetch THM total room count ──────────────────────────────
def get_thm_total_rooms():
    try:
        # THM public API for room count
        r = requests.get(
            "https://tryhackme.com/api/v2/search?kind=room&difficulty=all&limit=1",
            timeout=10,
            headers={"User-Agent": "OwlRC/readme-bot"}
        )
        if r.status_code == 200:
            data = r.json()
            total = data.get("data", {}).get("total", None)
            if total:
                return int(total)
    except Exception:
        pass

    try:
        # Fallback — alternate endpoint
        r = requests.get(
            "https://tryhackme.com/api/hacktivities?type=room&difficulty=all&page=1&limit=1",
            timeout=10,
            headers={"User-Agent": "OwlRC/readme-bot"}
        )
        if r.status_code == 200:
            data = r.json()
            total = data.get("total", None)
            if total:
                return int(total)
    except Exception:
        pass

    # Static fallback if API unreachable — updated periodically by the script
    return 800

# ── Fetch THM user stats ────────────────────────────────────
def get_thm_user_stats():
    try:
        r = requests.get(
            f"https://tryhackme.com/api/user/rank/{THM_USERNAME}",
            timeout=10,
            headers={"User-Agent": "OwlRC/readme-bot"}
        )
        if r.status_code == 200:
            data = r.json()
            return {
                "rank": data.get("userRank", "N/A"),
                "points": data.get("points", "N/A"),
            }
    except Exception:
        pass
    return {"rank": "N/A", "points": "N/A"}

# ── Count writeups in repo ──────────────────────────────────
def count_writeups():
    counts = {}
    rooms = {}
    for cat in CATEGORIES:
        folder = REPO_ROOT / cat
        if folder.exists():
            files = [f for f in folder.glob("*.md") if f.name != "README.md"]
            counts[cat] = len(files)
            rooms[cat] = sorted([f.stem.replace("-", " ").title() for f in files])
        else:
            counts[cat] = 0
            rooms[cat] = []
    return counts, rooms

# ── Progress bar ────────────────────────────────────────────
def make_bar(done, total, width=30):
    if total == 0:
        return "░" * width + " 0%"
    pct = min(done / total, 1.0)
    filled = int(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"{bar}  {pct*100:.1f}%  ({done}/{total})"

# ── Build README ────────────────────────────────────────────
def build_readme(counts, rooms, thm_total, thm_stats):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_done = sum(counts.values())
    bar = make_bar(total_done, thm_total)

    # Room list columns — 3 per row
    def room_table(room_list, cat):
        if not room_list:
            return "_No writeups yet_\n"
        icon = CATEGORIES[cat]["icon"]
        rows = []
        for i in range(0, len(room_list), 3):
            chunk = room_list[i:i+3]
            row = " | ".join(f"[{r}]({cat}/{r.lower().replace(' ','-')}.md)" for r in chunk)
            rows.append(f"| {row} |" if len(chunk)==3 else f"| {row} |")
        header = "| Room | Room | Room |"
        sep    = "|---|---|---|"
        return header + "\n" + sep + "\n" + "\n".join(rows) + "\n"

    readme = f"""```
┌─────────────────────────────────────────────────────────────┐
│  OwlRC // TryHackMe Writeups                 by OwlRC 🦉   │
│  Last updated: {now:<44}│
├─────────────────────────────────────────────────────────────┤
│  Completed : {total_done:<3}   🟢 Easy: {counts['easy']:<3}  🟡 Medium: {counts['medium']:<3}  🔴 Hard: {counts['hard']:<3}  │
│  THM Total : {thm_total:<3} rooms (live count from TryHackMe)           │
├─────────────────────────────────────────────────────────────┤
│  Progress  : {bar:<47}│
└─────────────────────────────────────────────────────────────┘
```

[![TryHackMe](https://img.shields.io/badge/TryHackMe-{THM_USERNAME}-red?style=flat-square&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/{THM_USERNAME})
![Rooms Completed](https://img.shields.io/badge/Rooms_Completed-{total_done}-39d353?style=flat-square)
![THM Total](https://img.shields.io/badge/THM_Total_Rooms-{thm_total}-58a6ff?style=flat-square)
![Auto Updated](https://img.shields.io/badge/Auto_Updated-Daily-c9a84c?style=flat-square)

---

## 📋 Methodology

Every writeup follows this structure:

```
1. Room Info      → platform, difficulty, category, tools
2. Reconnaissance → nmap, service fingerprinting, web enum
3. Enumeration    → deeper scanning, attack surface
4. Exploitation   → gaining foothold
5. Post-Exploit   → privilege escalation where applicable
6. Lessons Learned → key takeaways
```

---

## 🟢 Easy  —  {counts['easy']} writeups

{room_table(rooms['easy'], 'easy')}

---

## 🟡 Medium  —  {counts['medium']} writeups

{room_table(rooms['medium'], 'medium')}

---

## 🔴 Hard  —  {counts['hard']} writeups

{room_table(rooms['hard'], 'hard')}

---

## ℹ️ Info / CTF Events  —  {counts['info']} writeups

{room_table(rooms['info'], 'info')}

---

## 🛠️ Tools

![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=flat-square&logo=kali-linux&logoColor=white)
![Nmap](https://img.shields.io/badge/nmap-0E83CD?style=flat-square)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat-square)
![Metasploit](https://img.shields.io/badge/Metasploit-2596CD?style=flat-square)
![Hashcat](https://img.shields.io/badge/Hashcat-121011?style=flat-square)
![BloodHound](https://img.shields.io/badge/BloodHound-FF0000?style=flat-square)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat-square)

---

> ⚠️ All writeups are based on TryHackMe lab environments — authorized, legal practice.
> Never use these techniques on systems you do not own or have written permission to test.

---

_🤖 This README is auto-generated daily by a GitHub Action — no manual updates needed._
_Add a writeup → push → README updates itself._

**by OwlRC 🦉 · github.com/OwlRC**
"""
    return readme

# ── Main ────────────────────────────────────────────────────
def main():
    print("[*] Counting writeups...")
    counts, rooms = count_writeups()
    print(f"    easy={counts['easy']} medium={counts['medium']} hard={counts['hard']} info={counts['info']}")

    print("[*] Fetching THM total room count...")
    thm_total = get_thm_total_rooms()
    print(f"    THM total rooms: {thm_total}")

    print("[*] Fetching THM user stats...")
    thm_stats = get_thm_user_stats()
    print(f"    rank={thm_stats['rank']} points={thm_stats['points']}")

    print("[*] Generating README...")
    readme = build_readme(counts, rooms, thm_total, thm_stats)

    readme_path = REPO_ROOT / "README.md"
    readme_path.write_text(readme, encoding="utf-8")
    print(f"[+] README written to {readme_path}")

if __name__ == "__main__":
    main()
