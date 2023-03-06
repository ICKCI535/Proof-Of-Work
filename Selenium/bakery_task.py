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


def like_retweet(browser, tweet_id):
    browser.get(f'https://twitter.com/intent/like?tweet_id={tweet_id}')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Like"]'))
    like = browser.find_element(By.XPATH, '//span[text()="Like"]')
    like.click()
    time.sleep(1)
    browser.get(f'https://twitter.com/intent/retweet?tweet_id={tweet_id}')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//span[text()="Retweet"]'))
    retweet = browser.find_element(By.XPATH, '//span[text()="Retweet"]')
    retweet.click()
    time.sleep(1)


def follow(browser, link):
    browser.get(link)
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]'))
    time.sleep(2)
    follow = browser.find_element(
        By.XPATH, '//div[@data-testid="confirmationSheetConfirm"]')
    follow.click()
    time.sleep(2)


def check_connect(browser):
    try:
        WebDriverWait(browser, 2).until(lambda a: browser.find_element(
            By.XPATH, '//div[text()="Connect Twitter"]'))
        connect = browser.find_element(
            By.XPATH, '//div[text()="Connect Twitter"]')
        connect.click()
        WebDriverWait(browser, 2).until(
            lambda a: browser.find_element(By.XPATH, '//button[@type="submit"]'))
        submit = browser.find_element(By.XPATH, '//button[@type="submit"]')
        submit.click()
        while len(browser.window_handles) != 2:
            continue
        browser.switch_to.window(browser.window_handles[-1])
        WebDriverWait(browser, 10).until(lambda a: browser.find_element(
            By.XPATH, '//input[@value="Authorize app"]'))
        authorize = browser.find_element(
            By.XPATH, '//input[@value="Authorize app"]')
        authorize.click()
        WebDriverWait(browser, 10).until(lambda a: browser.find_element(
            By.XPATH, '//div[text()="Congrats @"]'))
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except:
        pass


def delivery_func(browser, link):
    browser.get(link)
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@role="article"]'))
    article = browser.find_elements(By.XPATH, '//div[@role="article"]')[-1]
    action = ActionChains(browser)
    action.move_to_element(article).perform()
    delivery1 = browser.find_elements(
        By.XPATH, '//div[text()="Deliver my order"]')[-1]
    action.move_to_element(delivery1).perform()
    # delivery.click()
    check_connect(browser=browser)
    delivery = browser.find_elements(
        By.XPATH, '//div[text()="Deliver my order"]')[-1]
    # action.move_to_element(delivery).perform()
    delivery.click()
    time.sleep(1)
    # input('check')


def gm(browser):
    browser.get(
        'https://discord.com/channels/1042533136774479953/1042538425707942010')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, '//div[@role="textbox"]'))
    time.sleep(3)
    message = browser.find_element(By.XPATH, '//div[@role="textbox"]')
    message.send_keys('gm')
    message.send_keys(Keys.ENTER)
    time.sleep(1)


def main():
    for i in range(0, 20):
        wallet = utils.get_wallet(i)
        account = utils.get_account(i)
        print(account['id'])
        gologin = utils.get_gologin(account['id'])
        browser_info = utils.create_browser(gologin)
        browser = browser_info['browser']
        gl = browser_info['gologin']
        tweet_id = '1628768641897402369'
        like_retweet(browser, tweet_id)
        # gm(browser)
        # follow(browser, 'https://twitter.com/intent/follow?screen_name=homeety')
        delivery_func(
            browser, 'https://discord.com/channels/1042533136774479953/1063474557899526334')
        logging.info(f"-------------Done {account['username']}-------------")
        browser.close()
        gl.stop()


main()
