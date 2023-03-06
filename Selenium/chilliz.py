from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import logging
import pyperclip

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
    options.add_argument("window-size=1600,900")
    options.add_experimental_option(
        "excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)
    # current_path = os.path.dirname(os.path.realpath(__file__))

    # exts
    options.add_extension("metamask.crx")
    browser = webdriver.Chrome("chromedriver.exe", options=options)
    return browser


def import_wallet(i):
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(2)
    browser.refresh()
    # browser.get("chrome-extension://kphmfijcplmcmnkmdfmmllhinoenacbc/home.html/")
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element_by_xpath("//button[text()='Get Started']"))
    get_started = browser.find_element_by_xpath(
        "//button[text()='Get Started']").click()
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element_by_xpath("//button[text()='Import wallet']"))
    import_wallet = browser.find_element_by_xpath(
        "//button[text()='Import wallet']").click()
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element_by_xpath("//button[text()='I Agree']"))
    i_agree = browser.find_element_by_xpath(
        "//button[text()='I Agree']").click()
    WebDriverWait(browser, 20).until(lambda a: browser.find_element_by_xpath(
        "//input[@placeholder='Paste Secret Recovery Phrase from clipboard']"))
    secret_recovery_phrase = browser.find_element_by_xpath(
        "//input[@placeholder='Paste Secret Recovery Phrase from clipboard']")
    secret_recovery_phrase.click()
    secret_recovery_phrase.send_keys(
        "wool damp fetch hundred funny clerk tiger child soap alien cruise other")
    time.sleep(1)
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element_by_xpath("//input[@id='password']"))
    new_password = browser.find_element_by_xpath("//input[@id='password']")
    new_password.send_keys("123456789")
    WebDriverWait(browser, 20).until(
        lambda a: browser.find_element_by_xpath("//input[@id='confirm-password']"))
    confirm_password = browser.find_element_by_xpath(
        "//input[@id='confirm-password']")
    confirm_password.send_keys("123456789")
    tick_read_agree = browser.find_elements_by_xpath(
        "//div[@role='checkbox']")[1].click()
    agree_import = browser.find_element_by_xpath(
        "//button[text()='Import']").click()
    while True:  # header not found
        try:
            WebDriverWait(browser, 15).until(
                lambda a: browser.find_element_by_xpath("//button[text()='All Done']"))
            break
        except:
            browser.execute_script(
                'document.getElementsByTagName("input")[0].value = "" ')
            browser.execute_script(
                f'document.getElementsByTagName("input")[0].value = "wool damp fetch hundred funny clerk tiger child soap alien cruise other" ')
            browser.find_element_by_xpath("//button[text()='Import']").click()

    browser.find_element_by_xpath("//button[text()='All Done']").click()
    time.sleep(1)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element_by_xpath(
        "//button[@class='fas fa-times popover-header__button']"))
    browser.find_element_by_xpath(
        "//button[@class='fas fa-times popover-header__button']").click()
    with open("wallets_chilliz.txt", 'r') as f:
        lines = f.readlines()
        line = lines[i]
        wallet_address = line.split("|")[0]
        private_key = line.split("|")[1]
        private_key = private_key.replace("\n", "")
        WebDriverWait(browser, 20).until(lambda a: browser.find_element_by_xpath(
            "//div[@class='identicon__address-wrapper']"))
        browser.find_element_by_xpath(
            "//div[@class='identicon__address-wrapper']").click()
        WebDriverWait(browser, 20).until(
            lambda a: browser.find_element_by_xpath("//div[text()='Import Account']"))
        browser.find_element_by_xpath("//div[text()='Import Account']").click()
        WebDriverWait(browser, 20).until(
            lambda a: browser.find_element_by_xpath("//input[@id='private-key-box']"))
        send_private_key = browser.find_element_by_xpath(
            "//input[@id='private-key-box']")
        send_private_key.send_keys(private_key)
        WebDriverWait(browser, 20).until(
            lambda a: browser.find_element_by_xpath("//button[text()='Import']"))
        browser.find_element_by_xpath("//button[text()='Import']").click()
        logging.info(f"Wallet: {wallet_address}")
        return wallet_address


def switch_network():
    time.sleep(1)
    menu = browser.find_element_by_xpath(
        '//*[@id="app-content"]/div/div[1]/div/div[2]/div[1]/div').click()
    custom = browser.find_element_by_xpath(
        '//span[text()="Custom RPC"]').click()
    time.sleep(0.5)
    network_name = browser.find_elements_by_xpath(
        '//input')[0].send_keys('Chiliz Scoville Testnet')
    rpc_url = browser.find_elements_by_xpath(
        '//input')[1].send_keys('https://scoville-rpc.chiliz.com')
    chain_id = browser.find_elements_by_xpath('//input')[2].send_keys('88880')
    currency = browser.find_elements_by_xpath('//input')[3].send_keys('CHZ')
    time.sleep(2)
    add_network = browser.find_element_by_xpath(
        '//button[text()="Save"]').click()
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element_by_xpath('//span[contains(text(),"Chiliz")]'))
    logging.info(f'Switch Network!')


def faucet_chilliz(address):
    browser.get('https://scoville-faucet.chiliz.com/')
    address_input = browser.find_element_by_xpath(
        '//input[@id="url"]').send_keys(address)
    give_me_chz = browser.find_element_by_xpath(
        '//button[text()="Give me CHZ	"]').click()
    time.sleep(0.5)
    amount_faucet = browser.find_element_by_xpath(
        '//a[text()="6.25 CHZs"]').click()


def get_chilliz():
    browser.get('https://scoville-nft.chiliz.com/')
    while len(browser.window_handles) != 2:
        continue
    browser.switch_to.window(browser.window_handles[1])
    while True:
        try:
            confirm = browser.find_element_by_xpath(
                '//button[text()="Next"]').click()
            time.sleep(0.5)
            connect = browser.find_element_by_xpath(
                '//button[text()="Connect"]').click()
            break
        except:
            continue
    browser.switch_to.window(browser.window_handles[0])


def mint_nft():
    for i in range(0, 5):
        WebDriverWait(browser, 30).until(
            lambda a: browser.find_element_by_xpath('//div[@aria-haspopup="listbox"]'))
        nfts = browser.find_element_by_xpath(
            '//div[@aria-haspopup="listbox"]').click()
        time.sleep(0.5)
        nft = browser.find_elements_by_xpath('//li[@role="option"]')[i].click()
        time.sleep(0.5)
        mint = browser.find_element_by_xpath('//button[text()="MINT"]').click()
        while len(browser.window_handles) != 2:
            continue
        browser.switch_to.window(browser.window_handles[1])
        while True:
            try:
                confirm = browser.find_element_by_xpath(
                    '//button[text()="Confirm"]').click()
                time.sleep(0.5)
                break
            except:
                continue
        browser.switch_to.window(browser.window_handles[0])
        WebDriverWait(browser, 60).until(lambda a: browser.find_element_by_xpath(
            '//div[text()="Transaction is successful!"]'))
        logging.info(f"Minted {i+1}/5")
        time.sleep(2)


for i in range(0, 1001):
    browser = create_browser()
    wallet = import_wallet(i)
    switch_network()
    faucet_chilliz(wallet)
    get_chilliz()
    mint_nft()
    logging.info(f'Done wallet {i+1}/1000')
    browser.quit()
