import json
import requests
import traceback
from anticaptchaofficial.hcaptchaproxyless import *
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock

proxies = {
    "http": "http://cuong.tran:4f77IpNRZYifgljF_country-Vietnam@proxy.packetstream.io:31112",
    "https": "https://cuong.tran:4f77IpNRZYifgljF_country-Vietnam@proxy.packetstream.io:31111",
}


def get_bearer():
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "Bearer null",
        "content-type": "application/json",
        "origin": "https://coin98.net",
        "os": "website",
        "osversion": "website",
        "referer": "https://coin98.net/",
        "signature": "2ddf5a5de97d2b348f2ee37fe5253fd16bda1a48d165fb11a5314fa5e44d7b96",
        "source": "C98ISSNKIMK",
        "user-agent": "Coin98/1657633523 CFNetwork/1333.0.4 Darwin/21.5.0",
        "version": "1.0",
    }
    data = {"id": "d520c7a8-421b-4563-b955-f5abc56b97ec", "lang": "vn"}
    url = "https://production.coin98.services/api/tempUser"

    r = requests.post(url=url, headers=headers, data=json.dumps(data),proxies=proxies)

    result = json.loads(r.text)
    return result["token"]


def hcaptcha_solve():
    solver = hCaptchaProxyless()
    solver.set_key("14d13757caa240bf729a6409378c5ef2")
    solver.set_website_url(
        "https://api.coin98.services/adapters/user/site/register")
    solver.set_website_key("1cb79159-1c87-4b0c-94f0-3dad1125eaba")
    solver.set_user_agent("Coin98/1657633523 CFNetwork/1333.0.4 Darwin/21.5.0")
    g_response = solver.solve_and_return_solution()
    return g_response


def input_email(email, bearer):
    headers = {
        "Host": "api.coin98.services",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "12.2.1",
        "Authorization": f"Bearer {bearer}",
        "Locale": "vi",
        "Os": "ios",
        "Source": "C98WLFININS",
        "Signature": "2f79a9255f0865d26ec8ea598aa01f168d9a574e2299fe2d8ea4a2414f45a758",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Captcha": "undefined",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Coin98/1657633523 CFNetwork/1333.0.4 Darwin/21.5.0",
    }
    data = {"id": email}
    url = "https://api.coin98.services/adapters/user/verify"

    r = requests.post(url=url, headers=headers, data=json.dumps(data),proxies=proxies)

    result = json.loads(r.text)
    return result["success"]


def input_password(email, password, bearer, captcha):
    headers = {
        "Host": "api.coin98.services",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "12.2.1",
        "Authorization": f"Bearer {bearer}",
        "Locale": "vi",
        "Os": "ios",
        "Source": "C98WLFININS",
        "Signature": "cf5c7c44c0eaf9ac31c0e7a2879bdb6676134ea9f80d1eeb85a8a72c027c4fbf",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Captcha": f"{captcha}",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Coin98/1657633523 CFNetwork/1333.0.4 Darwin/21.5.0",
    }
    data = {"id": email, "password": password}
    url = "https://api.coin98.services/adapters/user/login"

    r = requests.post(url=url, headers=headers, data=json.dumps(data),proxies=proxies)
    print(r.text)
    result = json.loads(r.text)
    print(f"result import password:", result)
    return result['data']['challenge']

def delete_line(file_name="success.txt", account=""):
    with open(f"{file_name}", "r") as f:
        lines = f.readlines()
    with open(f"{file_name}", "w") as f:
        for line in lines:
            if account not in line.strip("\n"):
                f.write(line)

def main(account):
    account = account.replace("\n", "")
    try:
        email = account.split("|")[0]
        print(email)
        pwd = account.split("|")[1].replace("\n", "")
        email_old = account.split("|")[2].replace("\n", "")
        bearer = get_bearer()
        print(bearer)
        if not bearer:
            raise Exception("Bearer:", bearer)
        input_email(account, bearer)
        challege = input_password(email, pwd, bearer, hcaptcha_solve())
        lock.acquire()
        with open("new.txt", "a") as f:
            f.write(f"{email}|{pwd}|{email_old}|{challege}\n")
        lock.release()
        lock.acquire()
        delete_line(account=account)
        lock.release()

    except Exception as e:
        print(f"line {traceback.format_exc()}|{e}|{email}")


if __name__ == "__main__":
    so_thread = int(input('Nhap so Thread muon chay: '))
    with open('success.txt', 'r') as f:
        accounts = f.readlines()
    lock = Lock()
    pool = ThreadPool(so_thread)
    pool.map(main, accounts)
