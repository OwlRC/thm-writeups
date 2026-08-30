import os
import re
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

# Badge colors per tool
TOOL_COLORS = {
    "nmap":           "0E83CD",
    "burp suite":     "FF6633",
    "metasploit":     "2596CD",
    "hashcat":        "121011",
    "bloodhound":     "FF0000",
    "wireshark":      "1679A7",
    "kali linux":     "557C94",
    "kali":           "557C94",
    "gobuster":       "00ADD8",
    "ffuf":           "F5A623",
    "hydra":          "2E86AB",
    "john":           "8B0000",
    "sqlmap":         "CC2927",
    "nikto":          "6A0572",
    "netcat":         "444444",
    "nc":             "444444",
    "evil-winrm":     "5C2D91",
    "impacket":       "003366",
    "crackmapexec":   "1A1A2E",
    "powerview":      "0078D4",
    "mimikatz":       "B22222",
    "linpeas":        "FF4500",
    "winpeas":        "FF6347",
    "dirsearch":      "20B2AA",
    "git-dumper":     "F05032",
    "ghidra":         "009A44",
    "strings":        "708090",
    "exiftool":       "6B8E23",
    "sherlock":       "483D8B",
    "curl":           "073551",
    "python":         "3776AB",
    "bash":           "121011",
    "ssh":            "2E8B57",
    "nessus":         "00B388",
    "openvas":        "558B2F",
    "aircrack-ng":    "E65100",
    "jwt_tool":       "7B1FA2",
    "feroxbuster":    "FF5722",
    "wpscan":         "21759B",
    "ldapsearch":     "0052CC",
    "kerbrute":       "C62828",
    "rubeus":         "AD1457",
    "msfvenom":       "37474F",
    "stealthon":      "39d353",
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

def extract_tools_from_file(filepath):
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        # Match the Tools row in the markdown table
        match = re.search(r'\|\s*\*\*Tools\*\*\s*\|\s*([^|\n]+)', content)
        if match:
            tools_raw = match.group(1).strip()
            # Split by comma, pipe, or bullet
            tools = re.split(r'[,·|•\n]+', tools_raw)
            cleaned = []
            for t in tools:
                t = t.strip().strip('*').strip()
                # Remove markdown links
                t = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', t)
                if t and len(t) > 1:
                    cleaned.append(t)
            return cleaned
    except Exception:
        pass
    return []

def count_writeups():
    counts, rooms, all_tools = {}, {}, set()
    for cat in CATEGORIES:
        folder = REPO_ROOT / cat
        if folder.exists():
            files = sorted([f for f in folder.glob("*.md") if f.name != "README.md"])
            counts[cat] = len(files)
            rooms[cat] = [f.stem.replace("-", " ").title() for f in files]
            for f in files:
                for tool in extract_tools_from_file(f):
                    all_tools.add(tool.lower().strip())
        else:
            counts[cat] = 0
            rooms[cat] = []
    return counts, rooms, all_tools

def make_tool_badge(tool):
    color = TOOL_COLORS.get(tool.lower(), "555555")
    label = tool.replace("-", "_").replace(" ", "_")
    display = tool.replace(" ", "%20").replace("-", "--")
    return f"![{tool}](https://img.shields.io/badge/{display}-{color}?style=flat-square)"

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

def build_readme(counts, rooms, thm_total, all_tools):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = sum(counts.values())
    pct = round(total / thm_total * 100, 1) if thm_total else 0
    filled = int((total / thm_total) * 50) if thm_total else 0
    bar = "█" * filled + "░" * (50 - filled)

    # Build tool badges — sorted alphabetically, skip very generic ones
    skip = {"browser", "n/a", "browser devtools", "terminal", "linux", "windows"}
    tool_badges = []
    for tool in sorted(all_tools):
        if tool not in skip and len(tool) > 1:
            tool_badges.append(make_tool_badge(tool))
    tools_section = "\n".join(tool_badges) if tool_badges else "_(tools auto-detected from writeups)_"

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

## 🛠️ Tools — auto-detected from writeups

{tools_section}

---

> ⚠️ All writeups are based on authorized TryHackMe lab environments.
> Never use these techniques on systems you do not own or have written permission to test.

*🤖 README auto-generated daily — push a new writeup and this updates itself.*

**by OwlRC 🦉**
"""
    return readme

def main():
    print("[*] Counting writeups and scanning tools...")
    counts, rooms, all_tools = count_writeups()
    print(f"    easy={counts['easy']} medium={counts['medium']} hard={counts['hard']} info={counts['info']}")
    print(f"    Tools found: {sorted(all_tools)}")
    print("[*] Fetching THM total...")
    thm_total = get_thm_total_rooms()
    print(f"    THM total: {thm_total}")
    print("[*] Generating README...")
    readme = build_readme(counts, rooms, thm_total, all_tools)
    (REPO_ROOT / "README.md").write_text(readme, encoding="utf-8")
    print("[+] Done")

if __name__ == "__main__":
    main()
