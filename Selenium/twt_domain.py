import requests
import lib_twitter as tw
import logging
import time
import sys
import lib_utils as utils
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import random

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
def claim_domain(address):
    browser.get('https://twit.domains/')
    WebDriverWait(browser,10).until(lambda a : browser.find_element(By.XPATH,'//div[text()=" Continue with Twitter"]'))
    twitter = browser.find_element(By.XPATH,'//div[text()=" Continue with Twitter"]')
    twitter.click()
    WebDriverWait(browser,15).until(lambda a : browser.find_element(By.XPATH,'//span[text()="Authorize app"]'))
    time.sleep(1)
    authorize = browser.find_element(By.XPATH,'//span[text()="Authorize app"]')
    authorize.click()
    WebDriverWait(browser,10).until(lambda a : browser.find_element(By.TAG_NAME,"input"))
    input_address = browser.find_element(By.TAG_NAME,"input")
    input_address.send_keys(address)
    confirm = browser.find_element(By.XPATH,'//div[text()="confirm"]')
    confirm.click()
    time.sleep(3)

for i in range(1,20):
    try:
        wallet = utils.get_wallet(i)
        account = utils.get_account(i)
        print(account['id'])
        gologin = utils.get_gologin(account['id'])
        browser_info = utils.create_browser(gologin)
        browser = browser_info['browser']
        gl = browser_info['gologin']
        claim_domain(wallet['address'])
        logging.info(f"-------------Done {account['username']}-------------")
        browser.close()
        gl.stop()
    except Exception as e:
        print(e)