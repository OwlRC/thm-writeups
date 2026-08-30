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
    try:
        r = requests.get(
            "https://tryhackme.com/api/v2/search?kind=room&difficulty=all&limit=1",
            timeout=10, headers={"User-Agent": "OwlRC/readme-bot"}
        )
        if r.status_code == 200:
            total = r.json().get("data", {}).get("total")
            if total: return int(total)
    except Exception:
        pass
    try:
        r = requests.get(
            "https://tryhackme.com/api/hacktivities?type=room&difficulty=all&page=1&limit=1",
            timeout=10, headers={"User-Agent": "OwlRC/readme-bot"}
        )
        if r.status_code == 200:
            total = r.json().get("total")
            if total: return int(total)
    except Exception:
        pass
    return 800

def count_writeups():
    counts = {}
    rooms = {}
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

def make_progress_bar(done, total, width=40):
    if total == 0:
        return "░" * width
    pct = min(done / total, 1.0)
    filled = int(pct * width)
    return "█" * filled + "░" * (width - filled)

def room_table(room_list, cat):
    if not room_list:
        return "_No writeups yet_\n"
    rows = []
    for i in range(0, len(room_list), 3):
        chunk = room_list[i:i+3]
        cells = [f"[{r}]({cat}/{r.lower().replace(' ', '-')}.md)" for r in chunk]
        while len(cells) < 3:
            cells.append("")
        rows.append(f"| {' | '.join(cells)} |")
    return "| Room | Room | Room |\n|---|---|---|\n" + "\n".join(rows) + "\n"

def build_readme(counts, rooms, thm_total):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_done = sum(counts.values())
    pct = (total_done / thm_total * 100) if thm_total > 0 else 0
    bar = make_progress_bar(total_done, thm_total)

    readme = f"""<div align="center">

```
  ╔══════════════════════════════════════════════════════════╗
  ║         OwlRC // TryHackMe Writeups          🦉          ║
  ║  Updated : {now:<46}║
  ╠══════════════════════════════════════════════════════════╣
  ║  Completed : {total_done:<3}   🟢 {counts['easy']:<3}  🟡 {counts['medium']:<3}  🔴 {counts['hard']:<3}  ℹ️  {counts['info']:<3}       ║
  ║  THM Total : {thm_total:<3} rooms tracked live from TryHackMe       ║
  ╠══════════════════════════════════════════════════════════╣
  ║  {bar}  ║
  ║  Progress  : {pct:.1f}% ({total_done}/{thm_total}){'':>34}║
  ╚══════════════════════════════════════════════════════════╝
```

[![TryHackMe](https://img.shields.io/badge/TryHackMe-{THM_USERNAME}-red?style=flat-square&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/{THM_USERNAME})
![Completed](https://img.shields.io/badge/Rooms_Completed-{total_done}-39d353?style=flat-square)
![THM Total](https://img.shields.io/badge/THM_Total_Rooms-{thm_total}-58a6ff?style=flat-square)
![Auto Updated](https://img.shields.io/badge/Auto_Updated-Daily-c9a84c?style=flat-square)

</div>

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

## 🛠️ Tools Used

![Kali Linux](https://img.shields.io/badge/Kali_Linux-557C94?style=flat-square&logo=kali-linux&logoColor=white)
![Nmap](https://img.shields.io/badge/nmap-0E83CD?style=flat-square)
![Burp Suite](https://img.shields.io/badge/Burp_Suite-FF6633?style=flat-square)
![Metasploit](https://img.shields.io/badge/Metasploit-2596CD?style=flat-square)
![Hashcat](https://img.shields.io/badge/Hashcat-121011?style=flat-square)
![BloodHound](https://img.shields.io/badge/BloodHound-FF0000?style=flat-square)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat-square)

---

> ⚠️ All writeups are based on TryHackMe lab environments — authorized, legal practice only.
> Never use these techniques on systems you do not own or have written permission to test.

---

_🤖 README auto-generated daily — add a writeup, push, README updates itself._

**by OwlRC 🦉 · [github.com/OwlRC](https://github.com/OwlRC)**
"""
    return readme

def main():
    print("[*] Counting writeups...")
    counts, rooms = count_writeups()
    print(f"    easy={counts['easy']} medium={counts['medium']} hard={counts['hard']} info={counts['info']}")
    print("[*] Fetching THM total room count...")
    thm_total = get_thm_total_rooms()
    print(f"    THM total: {thm_total}")
    print("[*] Generating README...")
    readme = build_readme(counts, rooms, thm_total)
    readme_path = REPO_ROOT / "README.md"
    readme_path.write_text(readme, encoding="utf-8")
    print(f"[+] Done → {readme_path}")

if __name__ == "__main__":
    main()
