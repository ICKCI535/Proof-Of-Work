import logging
import time
import sys
import lib_utils as utils
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def claim_1(browser):
    browser.get(
        'https://twitter.com/intent/retweet?tweet_id=1628782936928702464')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Retweet"]'))
    retweet = browser.find_element(By.XPATH, '//span[text()="Retweet"]')
    retweet.click()
    time.sleep(1)
    browser.get('https://twitter.com/intent/follow?screen_name=XterioUpdates')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)
    browser.get('https://discord.com/invite/g6hmrdRdAA')
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//div[text()="Accept Invite"]'))
    accept = browser.find_element(By.XPATH, '//div[text()="Accept Invite"]')
    accept.click()
    time.sleep(2)
    pyautogui.press('esc')
    time.sleep(1)
    accept = browser.find_element(
        By.XPATH, '//div[text()="Continue to Discord"]')
    accept.click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//div[text()="Complete"]'))
    time.sleep(1)
    continue_button = browser.find_element(
        By.XPATH, '//div[text()="Complete"]')
    continue_button.click()
    time.sleep(1)
    browser.find_element(By.XPATH, '//input[@type="checkbox"]').click()
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(1)
    browser.get('https://twitter.com/intent/follow?screen_name=XterioGames')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)

    browser.get('https://galxe.com/Xterio/campaign/GCGQiU4qYJ')
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//input[@id="password"]'))
    password = browser.find_element(
        By.XPATH, '//input[@id="password"]')
    password.send_keys('123456789')
    password.send_keys(Keys.ENTER)
    browser.switch_to.window(browser.window_handles[0])
    verify_1 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[0].click()
    verify_2 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[1].click()
    verify_3 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[2].click()
    verify_4 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[3].click()
    time.sleep(5)
    claim = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Claim")]')[0].click()
    WebDriverWait(browser, 20).until(lambda a: browser.find_element(
        By.XPATH, '//div[text         ()="View on polygonscan.com"]'))


def claim_2(browser):
    browser.get(
        'https://twitter.com/intent/retweet?tweet_id=1626401438946705410')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Retweet"]'))
    retweet = browser.find_element(By.XPATH, '//span[text()="Retweet"]')
    retweet.click()
    time.sleep(1)
    browser.get('https://twitter.com/intent/follow?screen_name=link3to')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)
    browser.get('https://twitter.com/intent/follow?screen_name=CyberConnectHQ')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)
    browser.get('https://galxe.com/Xterio/campaign/GC3WiU4A2x')
    verify_1 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[0].click()
    verify_2 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[1].click()
    verify_3 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[2].click()
    time.sleep(5)
    claim = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Claim")]')[0].click()
    WebDriverWait(browser, 20).until(lambda a: browser.find_element(
        By.XPATH, '//div[text()="View on polygonscan.com"]'))


def claim_3(browser):
    browser.get(
        'https://twitter.com/intent/retweet?tweet_id=1626773370502279168')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Retweet"]'))
    retweet = browser.find_element(By.XPATH, '//span[text()="Retweet"]')
    retweet.click()
    time.sleep(1)
    browser.get('https://twitter.com/intent/follow?screen_name=link3to')
    action = ActionChains(browser)
    browser.get('https://discord.com/invite/g6hmrdRdAA')
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//div[text()="Accept Invite"]'))
    accept = browser.find_element(By.XPATH, '//div[text()="Accept Invite"]')
    accept.click()
    time.sleep(2)
    pyautogui.press('esc')
    time.sleep(1)
    accept = browser.find_element(
        By.XPATH, '//div[text()="Continue to Discord"]')
    accept.click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//div[text()="Complete"]'))
    time.sleep(1)
    continue_button = browser.find_element(
        By.XPATH, '//div[text()="Complete"]')
    continue_button.click()
    time.sleep(1)
    browser.find_element(By.XPATH, '//input[@type="checkbox"]').click()
    browser.find_element(By.XPATH, '//button[@type="submit"]').click()
    time.sleep(1)
