from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s", datefmt='[%Y-%m-%d %H:%M:%S]',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def create_browser():
    options = Options()
    options.add_argument("window-size=1300,900")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    current_path = os.path.dirname(os.path.realpath(__file__))

    # exts
    options.add_extension("metamask.crx")
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    return browser


def import_wallet(i):
    browser.switch_to.window(browser.window_handles[0])
    # time.sleep(2)
    # browser.get("chrome-extension://kphmfijcplmcmnkmdfmmllhinoenacbc/home.html#initialize/welcome")
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, "//button[text()='Get Started']"))
    get_started = browser.find_element(By.XPATH,
                                       "//button[text()='Get Started']").click()
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, "//button[text()='Import wallet']"))
    import_wallet = browser.find_element(By.XPATH,
                                         "//button[text()='Import wallet']").click()
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, "//button[text()='I Agree']"))
    i_agree = browser.find_element(By.XPATH,
                                   "//button[text()='I Agree']").click()
    WebDriverWait(browser, 20).until(lambda a: browser.find_element(By.XPATH,
                                                                    "//input[@placeholder='Paste Secret Recovery Phrase from clipboard']"))
    secret_recovery_phrase = browser.find_element(By.XPATH,
                                                  "//input[@placeholder='Paste Secret Recovery Phrase from clipboard']")
    secret_recovery_phrase.click()
    secret_recovery_phrase.send_keys(
        "wool damp fetch hundred funny clerk tiger child soap alien cruise other")
    time.sleep(1)
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, "//input[@id='password']"))
    new_password = browser.find_element(By.XPATH, "//input[@id='password']")
    new_password.send_keys("123456789")
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, "//input[@id='confirm-password']"))
    confirm_password = browser.find_element(By.XPATH,
                                            "//input[@id='confirm-password']")
    confirm_password.send_keys("123456789")
    tick_read_agree = browser.find_elements(By.XPATH,
                                            "//div[@role='checkbox']")[1].click()
    agree_import = browser.find_element(By.XPATH,
                                        "//button[text()='Import']").click()
    while True:  # header not found
        try:
            WebDriverWait(browser, 15).until(
                lambda a: browser.find_element(By.XPATH, "//button[text()='All Done']"))
            break
        except:
            browser.execute_script(
                'document.getElementsByTagName("input")[0].value = "" ')
            browser.execute_script(
                f'document.getElementsByTagName("input")[0].value = "wool damp fetch hundred funny clerk tiger child soap alien cruise other" ')
            browser.find_element(By.XPATH, "//button[text()='Import']").click()
    browser.find_element(By.XPATH, "//button[text()='All Done']").click()
    time.sleep(1)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(By.XPATH,
                                                                    "//button[@class='fas fa-times popover-header__button']"))
    browser.find_element(By.XPATH,
                         "//button[@class='fas fa-times popover-header__button']").click()
    with open("wallets_rainbow.txt", 'r') as f:
        lines = f.readlines()
        line = lines[i]
        wallet_address = line.split("|")[0]
        private_key = line.split("|")[1]
        private_key = private_key.replace("\n", "")

        WebDriverWait(browser, 20).until(lambda a: browser.find_element(By.XPATH,
                                                                        "//div[@class='identicon__address-wrapper']"))
        browser.find_element(By.XPATH,
                             "//div[@class='identicon__address-wrapper']").click()
        WebDriverWait(browser, 20).until(
            lambda a: browser.find_element(By.XPATH, "//div[text()='Import Account']"))
        browser.find_element(
            By.XPATH, "//div[text()='Import Account']").click()
        WebDriverWait(browser, 20).until(
            lambda a: browser.find_element(By.XPATH, "//input[@id='private-key-box']"))
        send_private_key = browser.find_element(By.XPATH,
                                                "//input[@id='private-key-box']")
        send_private_key.send_keys(private_key)
        WebDriverWait(browser, 20).until(
            lambda a: browser.find_element(By.XPATH, "//button[text()='Import']"))
        browser.find_element(By.XPATH, "//button[text()='Import']").click()
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        return wallet_address


def mint_nft(wallet_address):
    while True:
        try:
            browser.get('https://rainbow.me/drop/zorb')
            WebDriverWait(browser, 5).until(
                lambda a: browser.find_element(By.XPATH, '//button[text()="Connect wallet"]'))
            break
        except:
            continue
    connect = browser.find_element(
        By.XPATH, '//button[text()="Connect wallet"]').click()
    time.sleep(1)
    browser.find_element(By.XPATH, '//div[text()="MetaMask"]').click()
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[1])
    while True:
        try:
            confirm = browser.find_element(By.XPATH,
                                           '//button[text()="Next"]').click()
            break
        except:
            continue
    time.sleep(0.5)
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[-1])
    while True:
        try:
            confirm = browser.find_element(By.XPATH,
                                           '//button[text()="Connect"]').click()
            break
        except:
            continue
    time.sleep(1)
    while len(browser.window_handles) != 1:
        continue
    browser.switch_to.window(browser.window_handles[0])
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, '//button[text()="Mint"]'))
    mint = browser.find_element(
        By.XPATH, '//button[text()="Mint"]').click()
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[1])
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element(By.XPATH, '//button[text()="Confirm"]'))
    time.sleep(1)
    while True:
        try:
            confirm = browser.find_element(By.XPATH,
                                           '//button[text()="Confirm"]').click()
            break
        except:
            continue
    while len(browser.window_handles) != 1:
        continue
    time.sleep(1)
    logging.info(f'done {wallet_address}')
    browser.quit()


for i in range(36, 100):
    browser = create_browser()
    a = import_wallet(i)
    mint_nft(a)
