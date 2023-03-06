import logging
import time
import sys
import lib_utils as utils
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def connect_site(browser):
    input('Press enter to connect to the site')
    browser.get('https://guild.xyz/alongside')
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//span[text()="Connect to a wallet"]'))
    connect = browser.find_element(
        By.XPATH, '//span[text()="Connect to a wallet"]').click()
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="MetaMask"]'))
    time.sleep(1)
    metamask = browser.find_element(
        By.XPATH, '//span[text()="MetaMask"]').click()
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//input[@id="password"]'))
    password = browser.find_element(
        By.XPATH, '//input[@id="password"]')
    password.send_keys('123456789')
    password.send_keys(Keys.ENTER)
    try:
        WebDriverWait(browser, 3).until(
            lambda a: browser.find_element(By.XPATH, '//button[text()="Got it"]'))
        gotit = browser.find_element(
            By.XPATH, '//button[text()="Got it"]').click()
    except:
        pass
    connect = browser.find_element(By.XPATH, '//button[text()="Next"]').click()
    time.sleep(1)
    connect = browser.find_element(
        By.XPATH, '//button[text()="Connect"]').click()
    browser.switch_to.window(browser.window_handles[0])
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Verify account"]'))
    verify = browser.find_element(
        By.XPATH, '//span[text()="Verify account"]').click()
    time.sleep(2)
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//button[text()="Sign"]'))
    gotit = browser.find_element(By.XPATH, '//button[text()="Sign"]').click()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)
    while True:
        try:
            browser.find_element(
                By.XPATH, '//span[text()="Join Guild to get roles"]').click()
            break
        except:
            continue
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Connect"]'))
    time.sleep(2)
    connect = browser.find_elements(
        By.XPATH, '//span[text()="Connect"]')[0].click()
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[text()="Authorize"]'))
    authorize = browser.find_element(
        By.XPATH, '//div[text()="Authorize"]').click()
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(1)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//span[text()="Join guild"]'))
    browser.find_element(By.XPATH, '//span[text()="Join guild"]').click()
    input('Press Enter to continue...')


def claim_nft(browser):
    time.sleep(3)
    if len(browser.window_handles) != 1:
        browser.close()
    browser.switch_to.window(browser.window_handles[0])
    browser.get(
        f'https://twitter.com/intent/retweet?tweet_id=1628786835764785152')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Retweet"]'))
    retweet = browser.find_element(By.XPATH, '//span[text()="Retweet"]')
    retweet.click()
    time.sleep(1)
    browser.get('https://twitter.com/intent/like?tweet_id=1628786835764785152')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Like"]'))
    like = browser.find_element(By.XPATH, '//span[text()="Like"]')
    like.click()
    time.sleep(1)
    browser.get('https://twitter.com/intent/follow?screen_name=alongsidefi')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)

    browser.get('https://galxe.com/alongside/campaign/GCiXcU4dJR')
    # while len(browser.window_handles) != 2:
    #     continue
    # browser.switch_to.window(browser.window_handles[-1])
    # WebDriverWait(browser, 10).until(lambda a: browser.find_element(
    #     By.XPATH, '//input[@id="password"]'))
    # password = browser.find_element(
    #     By.XPATH, '//input[@id="password"]')
    # password.send_keys('123456789')
    # password.send_keys(Keys.ENTER)
    # browser.switch_to.window(browser.window_handles[0])
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//span[contains(text(),"Verify")]'))
    time.sleep(2)
    verify_1 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[0]
    verify_2 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[1]
    verify_3 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[2]
    verify_4 = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Verify")]')[3]
    verify_1.click()
    time.sleep(0.5)
    verify_2.click()
    time.sleep(0.5)
    verify_3.click()
    time.sleep(0.5)
    verify_4.click()
    time.sleep(5)
    claim = browser.find_elements(
        By.XPATH, '//span[contains(text(),"Claim")]')[0].click()
    WebDriverWait(browser, 20).until(lambda a: browser.find_element(
        By.XPATH, '//div[text         ()="View on polygonscan.com"]'))
    time.sleep(1)


def main():
    for i in range(16, 20):
        wallet = utils.get_wallet(i)
        account = utils.get_account(i)
        print(account['id'])
        gologin = utils.get_gologin(account['id'])
        browser_info = utils.create_browser(gologin)
        browser = browser_info['browser']
        gl = browser_info['gologin']
        # connect_site(browser)
        claim_nft(browser)
        logging.info(f"-------------Done {account['username']}-------------")
        browser.close()
        gl.stop()


main()
