from hashlib import new
from gologin import GoLogin
from sys import platform
import requests
from selenium import webdriver
import json
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyotp
import time
from bs4 import BeautifulSoup
import imaplib
import email
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock

proxy = {
    "http": "socks5://wickedbot:asd123@msgn.foxproxy.net:20156",
    "https": "socks5://wickedbot:asd123@msgn.foxproxy.net:20157",
}


def get_gologin(profile_id):
    gl = GoLogin(
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2MjdkYzZmMjI3MWM0Nzg0MGJkOGE2NjAiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2MjdkYzcyMTI3MWM0NzdlZTlkOGE2ODEifQ.LvSzcsGvWTTyIFbG1UH6NceUNtxWiyWylZxANtsKi7A",
            "profile_id": f"{profile_id}",
        }
    )

    if platform == "linux" or platform == "linux2":
        chrome_driver_path = "./chromedriver"
    elif platform == "darwin":
        chrome_driver_path = "./mac/chromedriver"
    elif platform == "win32":
        chrome_driver_path = "chromedriver.exe"
    return gl


def create_profile(ip="proxy.packetstream.io", port="31112", name="profie"):
    url = "https://api.gologin.com/browser/"
    s = requests.Session()

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3RpZCI6IjYzNTc5MmNlOGJhNmQwYjFhODkxMTU4NiIsInR5cGUiOiJ1c2VyIiwic3ViIjoiNjI3ZGM2ZjIyNzFjNDc4NDBiZDhhNjYwIn0.L07DAk1I2HntpHu1uXoM7UozKkpKY8v-D2m-2IiTsss",
        "content-type": "application/json",
        "origin": "https://app.gologin.com",
    }
    data = {
        "name": name,
        "role": "owner",
        "notes": "",
        "browserType": "chrome",
        "lockEnabled": True,
        "timezone": {"enabled": True, "fillBasedOnIp": True, "timezone": ""},
        "navigator": {
            "hardwareConcurrency": 6,
            "doNotTrack": False,
            "deviceMemory": 8,
            "maxTouchPoints": 0,
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
            "resolution": "1920x1080",
            "language": "en-US,en;q=0.9",
            "platform": "Win32",
        },
        "geolocation": {
            "mode": "prompt",
            "enabled": True,
            "customize": True,
            "fillBasedOnIp": True,
            "latitude": 0,
            "longitude": 0,
            "accuracy": 10,
        },
        "debugMode": False,
        "os": "win",
        "fonts": {"enableMasking": False, "enableDomRect": True},
        "proxy": {
            "autoProxyRegion": "us",
            "host": ip,
            "mode": "http",
            "password": "4f77IpNRZYifgljF_country-UnitedStates",
            "port": port,
            "torProxyRegion": "us",
            "username": "cuong.tran",
        },
        "proxyEnabled": True,
    }

    r = s.post(url=url, headers=headers, data=json.dumps(data).encode("utf-8"))
    a = json.loads(r.text)
    id = a["id"]
    return id


def delete_profile(profile_id):
    url = f"https://api.gologin.com/browser/{profile_id}"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3RpZCI6IjYzNTc5MmNlOGJhNmQwYjFhODkxMTU4NiIsInR5cGUiOiJ1c2VyIiwic3ViIjoiNjI3ZGM2ZjIyNzFjNDc4NDBiZDhhNjYwIn0.L07DAk1I2HntpHu1uXoM7UozKkpKY8v-D2m-2IiTsss",
        "content-type": "application/json",
        "origin": "https://app.gologin.com",
    }
    data = {"profilesToDelete": f"{profile_id}"}
    requests.delete(url=url, headers=headers)


def create_browser(gologin):
    debugger_address = gologin.start()
    print(debugger_address)
    options = Options()
    options.add_extension('extension_0_11_3_0.crx')
    options.add_experimental_option("debuggerAddress", debugger_address)
    browser = webdriver.Chrome(options=options)
    # browser.set_window_position(x, y, windowHandle ='current')

    return {"browser": browser, "gologin": gologin}


def get_wallet(i):
    with open("wallets.txt", "r") as r:
        wallets = r.readlines()
        wallet = wallets[i]
        wallet = wallet.split('|')
        return {"address": wallet[0], "pk": wallet[1]}


def get_account(i):
    with open("twitter.txt", "r") as r:
        accounts = r.readlines()
        account_detail = accounts[i]
        account_detail = account_detail.split("|")
        username = account_detail[0]
        password = account_detail[1]
        twofa = account_detail[2]
        email = account_detail[3]
        email_pass = account_detail[4]
        id = account_detail[5].replace("\n", "")

    return {
        "username": username,
        "password": password,
        "twofa": twofa,
        "email": email,
        "email_pass": email_pass,
        "id": id,
    }


def get_discord(i):
    with open("discord.txt", "r") as r:
        accounts = r.readlines()
        account_detail = accounts[i]
        account_detail = account_detail.split("|")
        email = account_detail[0]
        phone = account_detail[1]
        discord_name = account_detail[2]
        twofa = account_detail[3]
        token = account_detail[4]
        pass_mail = account_detail[5].replace("\n", "")
        pass_discord = account_detail[6].replace("\n", "")

    return {
        "phone": phone,
        "discord_name": discord_name,
        "twofa": twofa,
        "email": email,
        "token": token,
        "pass_mail": pass_mail,
        "pass_discord": pass_discord,
    }


def get_twofa_code(twofa):
    totp = pyotp.TOTP(twofa)
    twofa_code = totp.now()
    return twofa_code


def is_ip_changed(old_ip):
    while True:
        try:
            time.sleep(2)
            new_ip = requests.get(
                "http://ipv4.icanhazip.com/", proxies=proxy).text
            print(new_ip)
            if new_ip != old_ip:
                print("changed")
                print(new_ip)
                return True
        except:
            continue


def is_ip_changed_2(old_ip):
    i = 0
    # get verification token
    while i < 8:
        time.sleep(5)
        s = requests.Session()
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "foxproxy.net",
            "Origin": "https://foxproxy.net",
            "Referer": "https://foxproxy.net/dang-nhap",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
        }
        url = "https://foxproxy.net/dang-nhap"
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        token = soup.find("input", {"name": "__RequestVerificationToken"})[
            "value"]
        data = f"__RequestVerificationToken={token}&url=&U_UserName=wickedbot&U_Password=asd123456"
        # login
        r = s.post(url, headers=headers, data=data)
        # get ip
        url = "https://foxproxy.net/myproxy/getjson"
        headers = {"Content-Type": "application/json"}
        data = {"page": 1, "pageSize": 10}
        r = s.post(url, headers=headers, data=json.dumps(data))
        # print(r.text)
        ip = json.loads(r.text)
        new_ip = str(ip["Data"][0]["proxys"][1]["ip"]).split(":")[0]
        if len(str(new_ip)) >= 2 and new_ip != old_ip:
            print(new_ip)
            print("changed")
            return {"change_status": True, "new_ip": new_ip}
        i += 1


def change_ip_2():
    s = requests.Session()
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "foxproxy.net",
        "Origin": "https://foxproxy.net",
        "Referer": "https://foxproxy.net/dang-nhap",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    }
    url = "https://foxproxy.net/dang-nhap"
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]
    data = f"__RequestVerificationToken={token}&url=&U_UserName=wickedbot&U_Password=asd123456"
    # login
    r = s.post(url, headers=headers, data=data)
    # get ip
    url = "https://foxproxy.net/myproxy/getjson"
    headers = {"Content-Type": "application/json"}
    data = {"page": 1, "pageSize": 10}
    r = s.post(url, headers=headers, data=json.dumps(data))
    # print(r.text)
    ip = json.loads(r.text)
    old_ip = str(ip["Data"][0]["proxys"][1]["ip"]).split(":")[0]
    print(f"old ip: {old_ip}")
    while True:
        time.sleep(5)
        r = requests.post(
            "https://foxproxy.net/apiv1/reset/40a15c36-a371-4a92-8851-8360bd88f6d5"
        )
        info = json.loads(r.text)
        print(info)

        if info["status"]:
            status = is_ip_changed_2(old_ip)
            if status["change_status"]:
                break
        try:
            if info["message"]:
                sleep_time = info["message"].split(" ")[1].strip("s")
                time.sleep(int(sleep_time) + 2)
        except Exception as e:
            pass
        time.sleep(1)
    return status["new_ip"]


def change_ip():
    old_ip = requests.get("https://ipv4.icanhazip.com/", proxies=proxy).text
    print(f"old ip: {old_ip}")
    while True:
        time.sleep(3)
        r = requests.post(
            "https://foxproxy.net/apiv1/reset/d74ec0d6-271d-46ea-ad41-aa6e5faedf99"
        )
        info = json.loads(r.text)
        print(info)
        # print(info["status"])
        if info["status"]:
            # if is_ip_changed(old_ip):
            break
        try:
            if info["message"]:
                sleep_time = info["message"].split(" ")[1].strip("s")
                time.sleep(int(sleep_time) + 2)
        except Exception as e:
            pass


def edit_proxy(profile_id, name, host, port, username, password):
    url = f"https://api.gologin.com/browser/{profile_id}?updateNoises=False"
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqd3RpZCI6IjYyODc2MmZhNzlmN2YyZGU1YmNlMGY5OSIsInR5cGUiOiJ1c2VyIiwic3ViIjoiNjI3ZGM2ZjIyNzFjNDc4NDBiZDhhNjYwIn0.l5F4dcxlJjXxbEHTtJjmRV1HDYyP2Lhp9Alc1WCFN20",
        "content-type": "application/json",
        "origin": "https://app.gologin.com",
    }

    data = {
        "name": name,
        "browserType": "chrome",
        "os": "win",
        "proxyEnabled": True,
        "proxy": {
            "mode": "socks5",
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "autoProxyRegion": "us",
            "torProxyRegion": "us",
        },
    }
    r = requests.put(url=url, headers=headers, data=json.dumps(data))


def get_email(i):
    with open("email.txt", "r") as r:
        emails = r.readlines()
        email = emails[i]
        email = email.split("|")
    return {"email": email[0], "password": email[1].replace("\n", "")}


def get_message(imap_host, imap_user, imap_pass):
    imap = imaplib.IMAP4_SSL(imap_host)

    # login to server
    imap.login(imap_user, imap_pass)

    imap.select("Inbox")

    status, data = imap.search(None, "ALL")
    mail_ids = []

    for block in data:
        mail_ids += block.split()

    for i in mail_ids:
        status, data = imap.fetch(i, "(RFC822)")

        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])

                mail_from = message["from"]
                mail_subject = message["subject"]

                if message.is_multipart():
                    mail_content = ""
                    for part in message.get_payload():
                        if part.get_content_type() == "text/plain":
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()

                # print(f'From: {mail_from}')
                print(f'{str(mail_subject).split(" ")[0]}')
                # print(f'Content: {mail_content}')
    return str(mail_subject).split(" ")[0]


def create_phone(
    apikey="802831ff-d877-4265-a73e-7420cd1b97ec", dichvu_id="35", so_sms_nhan="1"
):
    s = requests.session()
    r = s.get(
        f"http://api.codesim.net/api/CodeSim/DangKy_GiaoDich?apikey={apikey}&dichvu_id={dichvu_id}&so_sms_nhan={so_sms_nhan}"
    )
    r = json.loads(r.text)
    giaodich_id = r["data"]["id_giaodich"]
    phone_number = r["data"]["phoneNumber"]
    return {"giaodich_id": giaodich_id, "phone_number": phone_number}


def get_sms(apikey="802831ff-d877-4265-a73e-7420cd1b97ec", giaodich_id=""):
    s = requests.session()
    r = s.get(
        f" http://api.codesim.net/api/CodeSim/KiemTraGiaoDich?apikey={apikey}&giaodich_id={giaodich_id}"
    )
    r = json.loads(r.text)
    sms_code = r["data"]["number"]
    return sms_code
