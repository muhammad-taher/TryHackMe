TryHackMe: Vulnversity Write-up
Challenge Overview
Platform: TryHackMe
Room: Vulnversity
Category: Web Exploitation, Privilege Escalation
Objective: Compromise a web server by exploiting a file upload vulnerability, then escalate privileges to root by abusing an SUID binary.

1. Reconnaissance
Port Scanning
We start by running an nmap scan to discover open ports and running services.

Bash
nmap -sC -sV -p- -oN nmap/initial <TARGET_IP>
Results:
The scan revealed 6 open ports:

Port 21: FTP (vsftpd 3.0.3)

Port 22: SSH (OpenSSH)

Port 139 & 445: SMB/NetBIOS

Port 3128: Squid Proxy (Version 3.5.12)

Port 3333: HTTP (Apache web server)

The machine appears to be running Ubuntu based on the service versions.

Web Enumeration
Since there is a web server running on an unconventional port (3333), I navigated to http://<TARGET_IP>:3333. It presented a static university page.

To find hidden directories, I ran gobuster:

Bash
gobuster dir -u http://<TARGET_IP>:3333 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
The scan uncovered a highly interesting directory: /internal/.

2. Initial Access
Exploiting File Upload
Navigating to http://<TARGET_IP>:3333/internal/ revealed a file upload form. My immediate goal was to upload a PHP reverse shell. However, attempting to upload a standard .php file resulted in an "Extension not allowed" error.

Instead of using Burp Suite to fuzz the allowed extensions, I wrote a quick custom Python script using the requests library to automate the process and test various extensions (.php3, .php4, .php5, .phtml).

The script iterated through the extensions and revealed that .phtml files were allowed by the server's filter.

Gaining the Shell
Grabbed the standard PHP reverse shell script from pentestmonkey.

Modified the IP and Port variables to point to my local machine.

Renamed the payload to revshell.phtml and uploaded it.

Set up a netcat listener:

Bash
nc -lvnp 9001
Navigated to http://<TARGET_IP>:3333/internal/uploads/revshell.phtml to trigger the execution.

This successfully popped a shell as the www-data user. I stabilized the shell using Python:

Bash
python -c 'import pty; pty.spawn("/bin/bash")'
From here, navigating to /home/bill/ allowed me to read the user.txt flag.

3. Privilege Escalation
The next step was to escalate privileges to root. I started by searching the system for binaries with the SUID bit set, which allow files to be executed with the permissions of the file owner (root).

Bash
find / -type f -perm -4000 2>/dev/null
Reviewing the output, /bin/systemctl stood out as highly unusual for an SUID binary.

Abusing systemctl
To figure out how to exploit systemctl, I consulted GTFOBins. Since systemctl was running with SUID privileges, I could create a malicious system service to execute commands as root.

Instead of grabbing a reverse shell, I created a service unit file that changes the permissions of /bin/bash to make it an SUID binary itself:

Bash
TF=$(mktemp).service
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash"
[Install]
WantedBy=multi-user.target' > $TF
/bin/systemctl link $TF
/bin/systemctl enable --now $TF
After executing the service, I checked the permissions of /bin/bash and confirmed the SUID bit (s) was now active.

I simply ran bash with the -p flag to retain the privileges:

Bash
/bin/bash -p
This dropped me into an effective root shell! I navigated to /root/ and grabbed the final root.txt flag.