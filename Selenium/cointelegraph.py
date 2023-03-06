import requests
import time
import random
from imap_tools import MailBox, A
import re
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import os
from gologin import GoLogin
import zipfile
from sys import platform
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def get_chromedriver(use_proxy=False, user_agent=None, link='a'):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = Options()
    # if use_proxy:
    #     pluginfile = 'proxy_auth_plugin.zip'

    #     with zipfile.ZipFile(pluginfile, 'w') as zp:
    #         zp.writestr("manifest.json", manifest_json)
    #         zp.writestr("background.js", background_js)
    #     chrome_options.add_extension(pluginfile)
    # if user_agent:
    #     chrome_options.add_argument('--user-agent=%s' % user_agent)
    chrome_options.add_argument('start-maximized')
    driver = uc.Chrome(
        chrome_options=chrome_options)
    driver.get(link)
    try:
        WebDriverWait(driver, 50).until(lambda a: driver.find_element(
            By.XPATH, '//span[text()="Watch video"]'))
    except:
        pass
    driver.quit()

    return driver


def get_otp_link(imap_host="imap-mail.outlook.com", imap_user="", imap_pass="", imap_user_old=""):  # fix algorithm
    while True:
        try:
            with MailBox(imap_host).login(imap_user_old, imap_pass, "JUNK") as mailbox:
                find = False
                mails = mailbox.fetch(
                    A(from_='hello@viral-loops.com', seen=False))
                for msg in mails:
                    link = re.findall(
                        '"https://mandrillapp.com/track/click/30895797/app.viral-loops.*" ',
                        msg.html,
                    )
                    link = link[0]
                    link = link.replace('"https', 'https')
                    link = link.replace('" ', '')
                    # link = link.replace('viral-loops', 'app.viral-loops')
                    break
                return link
        except:
            try:
                with MailBox(imap_host).login(imap_user_old, imap_pass, "INBOX") as mailbox:
                    find = False
                    mails = mailbox.fetch(
                        A(from_='hello@viral-loops.com', seen=False))
                    for msg in mails:
                        link = re.findall(
                            '"https://mandrillapp.com/track/click/30895797/app.viral-loops.*" ',
                            msg.html,
                        )
                        link = link[0]
                        link = link.replace('"https', 'https')
                        link = link.replace('" ', '')
                        # link = link.replace('viral-loops', 'app.viral-loops')
                        break
                    return link
            except:
                continue


def convert_url(link):  # V0FSdFT6yYBNTTg8F2BLSnRRWBA4bKhyX7txXpg8o5mqptQe2iRlAuPA1SL7

    url = 'https://api.tinyurl.com/create?api_token=V0FSdFT6yYBNTTg8F2BLSnRRWBA4bKhyX7txXpg8o5mqptQe2iRlAuPA1SL7'
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    data = {
        "url": link,
        "domain": "tinyurl.com",
        "alias": "",
        "tags": [],
        "expires_at": ""
    }
    r = requests.post(url=url, headers=headers, json=data)

    url = json.loads(r.text)['data']['tiny_url']
    return url


def request_reg(account):
    url = 'https://app.viral-loops.com/api/v2/events'

    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://cointelegraph.com",
        "referer": "mail.google.com"
    }

    data = {"params": {"event": "registration", "captchaJWT": "null", "user": {"firstname": "a", "lastname": "Nguyen", "email": f"{account}", "extraData": {"xxi6GtgT": "0xcC2d7E93C2B2eE0d5273Ec91ff9AB814Ce85d577"},
                                                                               "consents": {}, "refSource": "copy"}, "referrer": {"referralCode": "gnmv841"}, "refSource": "copy", "acquiredFrom": "popup"}, "publicToken": "VSx8VFOsBXAmtdG2wyFoy380cp0"}

    s = requests.Session()
    r = s.post(url=url, headers=headers, json=data)

    time.sleep(5)
    link = get_otp_link(imap_user='webleychiyunj@hotmail.com',
                        imap_pass='xSybcu55', imap_user_old='webleychiyunj@hotmail.com')
    print(link)
    return link


if __name__ == '__main__':
    with open('mail.txt', 'r') as r:
        data = r.readlines()
    for account in data:
        account = account.split('|')[0]
        link = request_reg(account)
        while True:
            try:
                browser = get_chromedriver(use_proxy=False, link=link)
                logging.info(f'DONE {account}')
                break
            except:
                continue
