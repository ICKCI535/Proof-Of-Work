import requests
import traceback
from anticaptchaofficial.hcaptchaproxyless import *
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock

proxies = {
    "http": "http://cuong.tran:4f77IpNRZYifgljF_country-Vietnam@proxy.packetstream.io:31112",
    "https": "https://cuong.tran:4f77IpNRZYifgljF_country-Vietnam@proxy.packetstream.io:31111",
}

def daily_claim(account_token):
    headers = {
        "Host": "api.coin98.services",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "12.2.1",
        "Authorization": f"Bearer {account_token}",
        "Locale": "vi",
        "Os": "ios",
        "Source": "C98WLFININS",
        "Signature": "190e1f1ff70f978e0025030cebb9c1a877bc4e331c5495848ee0a31acad40248",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Coin98/1658070624 CFNetwork/1333.0.4 Darwin/21.5.0",
    }
    url = "https://api.coin98.services/api/carnival/free"
    r = requests.post(headers=headers, url=url, proxies=proxies)
    # result = json.loads(r.text)
    print(f"result daily claim: {r.text}")
    return

def main(account):
    account = account.replace("\n", "")
    try:
        email = account.split("|")[0]
        print(email)
        account_token = account.split("|")[3].replace("\n", "")
        daily_claim(account_token)
    except Exception as e:
        print(f"line {traceback.format_exc()}|{e}|{email}")

if __name__ == "__main__":
    so_thread = int(input('Nhap so Thread muon chay: '))
    with open('new.txt', 'r') as f:
        accounts = f.readlines()
    lock = Lock()
    pool = ThreadPool(so_thread)
    pool.map(main, accounts)