import logging
import time
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


def login(browser):
    browser.get('https://www.premint.xyz/freemint-cnp-makimono-red/')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//*[@id="register-form"]/div[1]/div[1]/a'))
    login = browser.find_element(
        By.XPATH, '//*[@id="register-form"]/div[1]/div[1]/a')
    login.click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//button[@title="Login with MetaMask"]'))
    time.sleep(1)
    input('Press enter to continue: ')
    metamask = browser.find_element(
        By.XPATH, '//button[@title="Login with MetaMask"]')
    metamask.click()
    time.sleep(1)
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//input[@id="password"]'))
    password = browser.find_element(
        By.XPATH, '//input[@id="password"]')
    password.send_keys('123456789')
    password.send_keys(Keys.ENTER)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//button[text()="Next"]'))
    next = browser.find_element(
        By.XPATH, '//button[text()="Next"]')
    next.click()
    time.sleep(1)
    connect = browser.find_element(
        By.XPATH, '//button[text()="Connect"]')
    connect.click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[0])
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//button[text()="Sign"]'))
    sign = browser.find_element(
        By.XPATH, '//button[text()="Sign"]')
    sign.click()
    browser.switch_to.window(browser.window_handles[0])


def twitter_tasks(browser):
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//*[@id="step-twitter"]/div/div/div[2]/a'))
    twitter = browser.find_element(
        By.XPATH, '//*[@id="step-twitter"]/div/div/div[2]/a')
    twitter.click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, '//input[@value="Authorize app"]'))
    authorize = browser.find_element(
        By.XPATH, '//input[@value="Authorize app"]')
    authorize.click()

    browser.get('https://twitter.com/intent/follow?screen_name=cnp_en')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)

    browser.get('https://twitter.com/intent/follow?screen_name=ihayato')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)

    browser.get(f'https://twitter.com/intent/like?tweet_id=1626702169872412679')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Like"]'))
    like = browser.find_element(By.XPATH, '//span[text()="Like"]')
    like.click()
    time.sleep(1)
    browser.get(
        f'https://twitter.com/intent/retweet?tweet_id=1626702169872412679')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Retweet"]'))
    retweet = browser.find_element(By.XPATH, '//span[text()="Retweet"]')
    retweet.click()
    time.sleep(1)

    browser.get('https://www.premint.xyz/freemint-cnp-makimono-red/')

    register = browser.find_element(
        By.XPATH, '//button[@id="register-submit"]')
    register.click()
    try:
        WebDriverWait(browser, 5).until(lambda a: browser.find_element(
            By.XPATH, '//div[text()="Stay tuned...🥷"]'))
    except:
        time.sleep(2)


def main():
    for i in range(13, 20):  # 14 un done
        wallet = utils.get_wallet(i)
        account = utils.get_account(i)
        print(account['id'])
        gologin = utils.get_gologin(account['id'])
        browser_info = utils.create_browser(gologin)
        browser = browser_info['browser']
        gl = browser_info['gologin']
        login(browser)
        twitter_tasks(browser)
        logging.info(f"-------------Done {account['username']}-------------")
        browser.close()
        gl.stop()


main()
