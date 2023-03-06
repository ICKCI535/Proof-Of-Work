import requests
import json
import re
import random
import logging
import os
import time
import capmonster
import solver
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock
import traceback
from imap_tools import MailBox, A

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

proxies = {
    "http": "http://cuong.tran:4f77IpNRZYifgljF_country-Vietnam@proxy.packetstream.io:31112",
    "https": "https://cuong.tran:4f77IpNRZYifgljF_country-Vietnam@proxy.packetstream.io:31111",
}


def hcaptcha_solve():
    return capmonster.main()


def get_bearer():
    headers = {
        "Host": "api.coin98.services",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Version": "12.2.1",
        "Locale": "en",
        "Os": "ios",
        "Source": "C98WLFININS",
        "Signature": "cdd8f5670049e59b17e670afa0039c9c661b7476f43d722e9c0495ba5823a090",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Length": "49",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Coin98/1657633523 CFNetwork/1325.0.1 Darwin/21.1.0"
    }
    data = {"device": "B741CDD9-2A4C-4DE7-BC3F-07A0E2DE70A6"}
    url = "https://api.coin98.services/adapters/user/device"
    try:
        r = requests.post(
            url=url, headers=headers, data=json.dumps(data), proxies=proxies
        )
    except:
        return "proxy_error"
    result = json.loads(r.text)
    return result


def request_otp(email):
    url = "https://api.coin98.services/adapters/user/verify"
    headers = {
        "Host": "api.coin98.services",
        "Accept": "application/json",
        "version": "12.1.1",
        "locale": "vi",
        "os": "ios",
        "source": "C98WLFININS",
        "signature": "795c537e29961bdf37a60f075dbc644bad3e019ea32456873db7fe99396e4740",
        "Accept-Language": "en-US,en;q=0.9",
        "captcha": "undefined",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Coin98/1657633523 CFNetwork/1325.0.1 Darwin/21.1.0",
        "Connection": "close",
        "Content-Type": "application/json",
    }
    data = {"id": email}
    try:
        r = requests.post(
            url=url, headers=headers, data=json.dumps(data), proxies=proxies
        )
    except:
        return "proxy_error"
    # print(r.text)
    return r.text


def get_otp_link(imap_host='imap-mail.outlook.com', imap_user="", imap_pass="", range_search="INBOX", imap_user_old=''):
    x = 0
    loop = True
    while True:
        time.sleep(2)
        with MailBox(imap_host).login(imap_user, imap_pass, range_search) as mailbox:
            mails = mailbox.fetch(
                A(new=True, from_="no-reply@coin98.com", to=imap_user))
            x += 1
            if x == 10:
                return 0
            for msg in mails:
                otp = re.findall(
                    '"https://information.coin98.services/api/otp.*alt="OTP CODE"', msg.html)
                otp = otp[0]
                otp = otp.replace('"https', 'https')
                otp = otp.replace('" alt="OTP CODE"', '')
                loop = False
                print(otp)
                break
            if loop == False:
                break
    return otp


def download_image(otp_link, email):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,vi;q=0.8",
        "cache-control": "max-age=0",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    r = requests.get(otp_link, headers=headers, proxies=proxies)
    print(r.status_code)
    if r.status_code == 200:
        with open(f"captcha/{email}.png", "wb") as f:
            f.write(r.content)
    print('download')


def otp_from_image(email):
    return solver.main(email)


def register(
    bearer, captcha, email, otp, refId, pwd
):  # catch nameAlready, 5-6 digits OTP
    url = "https://api.coin98.services/adapters/user/register"
    headers = {
        "Host": "api.coin98.services",
        "Accept": "application/json",
        "version": "12.1.1",
        "Authorization": f"Bearer {bearer}",
        "locale": "vi",
        "os": "ios",
        "source": "C98WLFININS",
        "signature": "0e66b61d91fab51aa14f5b26a2d77a6428373e295e83d3b493d676c40d3e87f3",
        "Accept-Language": "en-US,en;q=0.9",
        "captcha": captcha,
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Coin98/1657633523 CFNetwork/1325.0.1 Darwin/21.1.0",
        "Connection": "close",
        "Content-Type": "application/json",
    }
    username = email.split("@")[1] + str(random.randint(1000000, 9999999))
    data = {
        "id": email,
        "code": str(otp),
        "referral": f"{refId}",
        "userName": f"{username}",
        "password": f"{pwd}",
    }
    try:
        r = requests.post(
            url=url, headers=headers, data=json.dumps(data), proxies=proxies
        )
    except Exception as e:
        return e
    result = json.loads(r.text)
    return result


def delete_link(file_name="link_captcha.txt", account=""):
    with open(f"{file_name}", "r") as f:
        lines = f.readlines()
    with open(f"{file_name}", "w") as f:
        for line in lines:
            if account not in line.strip("\n"):
                f.write(line)


def delete_line(file_name="accounts.txt", account=""):
    with open(f"{file_name}", "r") as f:
        lines = f.readlines()
    with open(f"{file_name}", "w") as f:
        for line in lines:
            if line.strip("\n") != account:
                f.write(line)


def main(account):
    account = account.replace("\n", "")
    try:
        email = account.split("|")[0]
        print(email)
        pwd = account.split("|")[1].replace("\n", "")
        # email_old = account.split("|")[2].replace("\n", "")
        # bearer = get_bearer()
        # print(bearer)
        # if not bearer:
        #     raise Exception("Bearer:", bearer)
        bearer = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IkI3NDFDREQ5LTJBNEMtNERFNy1CQzNGLTA3QTBFMkRFNzBBNiIsInRva2VuIjoiIiwiaWF0IjoxNjU5NDA5MjI3LCJleHAiOjE2OTA5NDUyMjd9.ijkjioz1VNpFoAb3GsmDu2yzGRbvBmjpkM11-5ygFa4'
        request_otp_status = request_otp(email)
        print(request_otp_status)
        # if not request_otp_status:
        #     raise Exception("Request otp:", request_otp_status)
        otp_link = get_otp_link(
            imap_user=email, imap_pass=pwd, imap_user_old=email, range_search='JUNK')
        if not otp_link:
            otp_link = get_otp_link(
                imap_user=email, imap_pass=pwd, imap_user_old=email, range_search='INBOX')
        download_image(otp_link=otp_link, email=email)
        try:
            otp = otp_from_image(email=email)
        except:
            image_snapshot = f'{email}.png'  # xóa image otp captcha
            location = 'captcha/'
            path = os.path.join(location, image_snapshot)
            os.remove(path)
            raise Exception('No Image: ')
        print(otp)
        if len(str(otp)) != 4 or "x" in str(otp):
            raise Exception("Wrong OTP:", otp)
        captcha = hcaptcha_solve()
        if not captcha:
            raise Exception("Captcha:", captcha)
        result = register(bearer, captcha,
                          email, otp, pwd=pwd, refId="C986C915JP")

        print(result)
        print(result['success'])

        if result['success'] == True:
            logging.info(f"OK|{email}")
            lock.acquire()
            with open('success.txt', 'a') as f:
                f.write(
                    f"{email}|{pwd}|{result['data']['challenge']}\n")
            lock.release()
            lock.acquire()
            delete_line(account=account)
            lock.release()
        else:
            logging.info(f"Fail|{email}|{result}")
            image_snapshot = f'{email}.png'  # xóa image otp captcha
            location = 'captcha/'
            path = os.path.join(location, image_snapshot)
            os.remove(path)
        image_snapshot = f'{email}.png'  # xóa image otp captcha
        location = 'captcha/'
        path = os.path.join(location, image_snapshot)
        os.remove(path)
    except Exception as e:
        print(f"line {traceback.format_exc()}|{e}|{email}")


if __name__ == "__main__":
    so_thread = int(input('Nhap so Thread muon chay: '))

    with open('accounts.txt', 'r') as f:
        accounts = f.readlines()
    lock = Lock()
    pool = ThreadPool(so_thread)
    pool.map(main, accounts)
