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


def erth(address, email, username, discord_name):
    browser.get(
        'https://95d4zrtzeh4.typeform.com/DEallowlist?typeform-source=erth.xyz')
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//button[@data-qa="start-button"]'))
    time.sleep(2)
    next = browser.find_element(By.XPATH, '//button[@data-qa="start-button"]')
    next.click()
    WebDriverWait(browser, 15).until(
        lambda a: browser.find_element(By.XPATH, '//input[@name="name"]'))
    time.sleep(1)
    input_address = browser.find_element(By.XPATH, '//input[@name="name"]')
    input_address.click()
    input_address.send_keys(address)
    ok = browser.find_element(
        By.XPATH, '//*[@id="block-0b8ed7d5-2287-49c0-9a4e-7dc70c0ce16c"]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/button')
    ok.click()

    WebDriverWait(browser, 15).until(
        lambda a: browser.find_element(By.XPATH, '//input[@type="email"]'))
    time.sleep(1)
    input_email = browser.find_element(By.XPATH, '//input[@type="email"]')
    input_email.click()
    input_email.send_keys(email)
    ok = browser.find_element(
        By.XPATH, '//*[@id="block-6cfd4787-c36a-443d-b78a-221679978556"]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/button')
    ok.click()

    WebDriverWait(browser, 15).until(lambda a: browser.find_element(
        By.XPATH, '//*[@id="block-261d0775b1f029cb"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/input'))
    time.sleep(1)
    twitter = browser.find_element(
        By.XPATH, '//*[@id="block-261d0775b1f029cb"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/input')
    twitter.click()
    twitter.send_keys(username)
    ok = browser.find_element(
        By.XPATH, '//*[@id="block-261d0775b1f029cb"]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/button')
    ok.click()

    WebDriverWait(browser, 15).until(lambda a: browser.find_element(
        By.XPATH, '//*[@id="block-2abe6f3f-eed0-4e75-8a8c-5fb48f457fcd"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/input'))
    time.sleep(1)
    discord = browser.find_element(
        By.XPATH, '//*[@id="block-2abe6f3f-eed0-4e75-8a8c-5fb48f457fcd"]/div/div/div[2]/div/div/div/div/div[2]/div[1]/input')
    discord.click()
    discord.send_keys(discord_name)
    ok = browser.find_element(
        By.XPATH, '//*[@id="block-2abe6f3f-eed0-4e75-8a8c-5fb48f457fcd"]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div/div/button')
    ok.click()

    WebDriverWait(browser, 15).until(
        lambda a: browser.find_element(By.XPATH, '//div[text()="Yes"]'))
    time.sleep(1)
    yes = browser.find_element(By.XPATH, '//div[text()="Yes"]')
    yes.click()
    time.sleep(1)

    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//*[@id="block-c6d179ae9c4794e0"]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div/button'))
    time.sleep(1)
    submit = browser.find_element(
        By.XPATH, '//*[@id="block-c6d179ae9c4794e0"]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div/button')
    submit.click()
    time.sleep(5)


for i in range(0, 20):

    wallet = utils.get_wallet(i)
    account = utils.get_account(i)
    discord = utils.get_discord(i)
    print(account['id'])
    gologin = utils.get_gologin(account['id'])
    browser_info = utils.create_browser(gologin, 1600, 900)
    browser = browser_info['browser']
    gl = browser_info['gologin']
    erth(address=wallet['address'], email=account['email'],
         username=f"@{account['username']}", discord_name=discord['discord_name'])
    logging.info(f"-------------Done {account['username']}-------------")
    browser.close()
    gl.stop()
