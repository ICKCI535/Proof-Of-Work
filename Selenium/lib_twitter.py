from concurrent.futures import BrokenExecutor
from multiprocessing.sharedctypes import Value
from re import I
from tkinter import BROWSE, W
from unittest import BaseTestSuite
from attr import attributes
from selenium import webdriver
from sys import platform
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import logging
import random
import sys
import lib_utils as utils
import os

sys.tracebacklimit = 0


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S]",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def log_in_twitter(browser, account):
    browser.get("https://twitter.com/i/flow/login")
    # time.sleep(5)
    # try:
    #     if_ban = check_ban_account(browser=browser)
    # except:
    #     if_ban = False
    #     pass
    # if if_ban == False:
    WebDriverWait(browser,10).until(lambda a :  browser.find_element(By.TAG_NAME,"input"))
    time.sleep(1)
    input_username = browser.find_element(By.TAG_NAME,"input").send_keys(
        account["username"]
    )
    time.sleep(1.5)
    submit = browser.find_element(By.XPATH,
        '//span[text()="Next"]'
    ).click()
    time.sleep(1)
    while True:
        try:
            password_input = browser.find_element(By.XPATH,
                '//input[@name="password"]'
            ).send_keys(account["password"])
            break
        except:
            continue

    browser.find_element(By.XPATH,
        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div'
    ).click()
    WebDriverWait(browser,10).until(lambda a : browser.find_element(By.XPATH,'//span[text()="Home"]'))
    time.sleep(2)

        # try:
    #         WebDriverWait(browser, 10).until(
    #             lambda a: browser.find_element_by_tag_name("input")
    #         )
    #     except:
    #         pass
    #     try:
    #         twofa_code = utils.get_twofa_code(account["twofa"])
    #         input_twofa_code = browser.find_element_by_tag_name("input").send_keys(
    #             twofa_code
    #         )
    #         submit = browser.find_element_by_xpath(
    #             '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div'
    #         ).click()
    #         WebDriverWait(browser, 5).until(
    #             lambda a: browser.find_element_by_xpath('//span[text()="Tweet"]')
    #         )
    #     except:
    #         pass
    #     return if_ban
    # else:
    #     return if_ban



def get_tweet(tweet_id, browser):
    browser.get(f"https://twitter.com/twitter/status/{tweet_id}")
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element_by_xpath('//div[@aria-label="Like"]')
    )
    time.sleep(1)


def like_tweet(browser):
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element_by_xpath('//div[@aria-label="Like"]')
    )
    browser.find_element_by_xpath('//div[@aria-label="Like"]').click()


def retweet(browser):
    time.sleep(1)
    browser.find_element_by_xpath('//div[@aria-label="Retweet"]').click()
    time.sleep(0.5)
    browser.find_element_by_xpath('//span[text()="Retweet"]').click()


def search_tweet(browser):
    browser.get("https://twitter.com/home")
    with open('get_word_search.txt','r') as r :
        words = r.readlines()
        words = str(words).split('|')
        word = words[random.randint(1,1601)]
    keyword_search = word
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(
            by=By.XPATH, value="//input[@placeholder='Search Twitter']"
        )
    )
    search_account = browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']"
    ).send_keys(keyword_search)
    a = browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']"
    ).send_keys(Keys.ENTER)


def search_user(browser,username):  
    browser.get('https://twitter.com/home')
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(
            by=By.XPATH, value="//input[@placeholder='Search Twitter']"
        )
    )
    search_account = browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']"
    ).send_keys(f'@{username}')
    a = browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']"
    ).send_keys(Keys.ENTER)
    WebDriverWait(browser,10).until( lambda a : browser.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/span'))
    people = browser.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/span').click()
    time.sleep(5)
    WebDriverWait(browser,10).until(lambda a : browser.find_elements(By.XPATH,'//div[@data-testid="UserCell"]')[0])
    choose_people = browser.find_elements(By.XPATH,'//div[@data-testid="UserCell"]')[0].click()
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Follow']")
    )
    time.sleep(1)
    follow = browser.find_element(By.XPATH, "//span[text()='Follow']").click()

def search_tweet_like_human(browser,tweet_id):
    WebDriverWait(browser,10).until(lambda a : browser.find_element(By.XPATH,'//article[@role="article"]'))
    while True:
        try:
            tweet = browser.find_element(By.XPATH,f'//a[contains(@href,"{tweet_id}")]/../../../../../div[2]/div').click()
            # time.sleep(2)
            # url = browser.current_url
            # if url == f'https://twitter.com/twitter/status/{tweet_id}':
            break
        except:
            scroll = 1
            for x in range(0, 10):
                browser.execute_script(f"window.scrollBy(0,{scroll})")
                scroll += 1
                time.sleep(0.1)


def choose_like_or_not(browser, like_percent=False):
    if like_percent:
        d_random_like = random.randint(1, 100)
        if (d_random_like) >= 100 - int(like_percent):
            like_tweet(browser=browser)
            logging.info(f"Like tweet")
    else:
        like_tweet(browser=browser)
        logging.info(f"Like tweet")
    time.sleep(1)


def choose_retweet_or_not(browser, retweet_percent=False):
    if retweet_percent:
        d_random_retweet = random.randint(1, 100)
        if (d_random_retweet) >= 100 - int(retweet_percent):
            retweet(browser=browser)
            logging.info(f"Retweet this tweet")
    else:
        retweet(browser=browser)
        logging.info(f"Retweet this tweet")

    time.sleep(1)


def read_tweet(browser, time_read):

    time.sleep(int(time_read) // 3)
    logging.info(f"Finish reading!")


def read_replies(time_read, browser, replies_min, replies_max):
    try:
        browser.find_elements(by=By.XPATH, value='//article[@role="article"]')[6]
        replies_amount = random.randint(int(replies_min), int(replies_max))
        logging.info(f"Replies amount: {replies_amount+1}")
        for i in range(0, replies_amount + 1):
            logging.info(f"Reading reply number {i+1}")
            time.sleep(int(time_read) // 3)
            scroll = 1
            print(int(time_read) // 3)
            for x in range(0, 25):
                browser.execute_script(f"window.scrollBy(0,{scroll})")
                scroll += 1
                time.sleep(0.1)
        logging.info(f"Finish reading!")
    except:
        pass
        logging.info(f"No Reply!")


def faucet_rinkeby(browser, i):
    with open('wallet_short_finance.txt', 'r') as f:
        lines = f.readlines()
        line = lines[i]
        wallet_address = line.split("|")[0]
    browser.get('https://rinkebyfaucet.com/')
    print(wallet_address)
    input_address = browser.find_element(By.XPATH, "//input[@type='address']")
    input_address.send_keys(wallet_address)
    send_faucet = browser.find_element(By.XPATH, "//span[text()='Send Me ']").click()
    while True:
        try:
            WebDriverWait(browser, 20).until(lambda a: browser.find_element(By.XPATH, "//p[text()='Follow your transaction on']"))
            logging.info('Done Faucet')
            break
        except:
            logging.info('Fail Faucet')
            break

def change_avatar(browser,get_to = True):
    if get_to:
        browser.get("https://twitter.com/home")
        WebDriverWait(browser, 10).until(
            lambda a: browser.find_element(By.XPATH, "//a[@aria-label='Profile']")
        )
        time.sleep(1)
        my_profile = browser.find_element(By.XPATH, "//a[@aria-label='Profile']").click()
        WebDriverWait(browser, 10).until(
            lambda a: browser.find_element(By.XPATH, "//a[@aria-label='Profile']")
        )
        time.sleep(4)
    first_ava = check_change_avatar(browser=browser)
    edit_profile = browser.find_element(
        By.XPATH, "//span[text()='Edit profile']"
    ).click()

    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//input[@type='file']")
    )
    click_change_avar = browser.find_elements(By.XPATH, "//input[@type='file']")[1]

    # cai này là đường dẫn đến thư mục chưa avar của em, và thêm dấu "\" vào cho đủ 2 dấu nha
    a = os.getcwd() + f"\image_nft_opensea\{random.randint(1,816)}.jpg"
    print(a)
    s = click_change_avar
    time.sleep(2)
    s.send_keys(a)
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Apply']")
    )
    apply_avar = browser.find_element(By.XPATH, "//span[text()='Apply']").click()
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Save']")
    )
    save_avar = browser.find_element(By.XPATH, "//span[text()='Save']").click()
    time.sleep(2)
    return first_ava


def follow_user(browser, user):
    browser.get(f"https://twitter.com/{user}")
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Follow']")
    )
    time.sleep(1)
    follow = browser.find_element(By.XPATH, "//span[text()='Follow']").click()


def change_bio(browser):
    browser.get("https://twitter.com/home")
    time.sleep(1)
    my_profile = browser.find_element(By.XPATH, "//a[@aria-label='Profile']").click()
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//a[@aria-label='Profile']")
    )
    time.sleep(4)
    edit_profile = browser.find_element(
        By.XPATH, "//span[text()='Edit profile']"
    ).click()
    with open("get_bio_discord_twitter.txt", "r") as r:
        random_bio = r.readline()
        random_bio = random_bio.split("|")[random.randint(1, 385)]
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(
            By.XPATH, "//textarea[@autocapitalize='sentences']"
        )
    )
    input_bio = browser.find_element(
        By.XPATH, "//textarea[@autocapitalize='sentences']"
    )
    input_bio.clear()
    input_bio.send_keys(random_bio)
    time.sleep(0.5)
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Save']")
    )
    save_avar = browser.find_element(By.XPATH, "//span[text()='Save']").click()
    time.sleep(1)

def change_banner(browser,get_to=True):
    if get_to:
        browser.get('https://twitter.com/home')
        time.sleep(1)
        WebDriverWait(browser, 10).until(lambda a: browser.find_element(
            By.XPATH, "//a[@aria-label='Profile']"))   
        my_profile = browser.find_element(
            By.XPATH, "//a[@aria-label='Profile']").click()
        time.sleep(4)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//span[text()='Edit profile']"))  
    edit_profile = browser.find_element(
        By.XPATH, "//span[text()='Edit profile']").click()
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//input[@type='file']"))
    click_change_avar = browser.find_elements(
        By.XPATH, "//input[@type='file']")[0]

    # cai này là đường dẫn đến thư mục chưa avar của em, và thêm dấu "\" vào cho đủ 2 dấu nha
    a =os.getcwd() + f"\image_nft_opensea\{random.randint(1,816)}.jpg"
    s = click_change_avar
    s.send_keys(a)
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Apply']"))
    apply_avar = browser.find_element(
        By.XPATH, "//span[text()='Apply']").click()
    time.sleep(1)
    WebDriverWait(browser, 10).until(
        lambda a: browser.find_element(By.XPATH, "//span[text()='Save']"))
    save_avar = browser.find_element(By.XPATH, "//span[text()='Save']").click()
    time.sleep(3)

def get_random_emoji():
    with open('get_emoji-sequences.txt', 'r' ,encoding='utf8') as r:
        get_emoji = r.readlines()
        get_emoji = get_emoji[random.randint(1,478)]
        get_emoji = get_emoji.split(';')[2].replace(' ','_')
        code_emoji = emoji.emojize(f":{get_emoji}:")
    return code_emoji

def change_name(browser):
    browser.get('https://twitter.com/home')
    time.sleep(1)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//a[@aria-label='Profile']"))   
    my_profile = browser.find_element(
        By.XPATH, "//a[@aria-label='Profile']").click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//span[text()='Edit profile']"))
    time.sleep(4)  
    edit_profile = browser.find_element(
        By.XPATH, "//span[text()='Edit profile']").click()
    time.sleep(1)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(By.XPATH, "//input[@autocapitalize='sentences']")) 
    name_twitter = browser.find_element(By.XPATH, "//input[@autocapitalize='sentences']")
    old_name = name_twitter.get_attribute('value')
    choose_rename = random.randint(6,6)
    name_twitter.clear()
    time.sleep(1)
    if (choose_rename % 4) == 3:
        name_twitter.send_keys(f'{old_name}.eth')
    elif (choose_rename % 4) == 2:
        while True:
            try:
                name_twitter.send_keys(f'{old_name}{get_random_emoji()}')
                break
            except:
                continue
    elif (choose_rename % 4) == 1:
        name_twitter.send_keys(f'0x{old_name}')
    else:
        pass
    WebDriverWait(browser, 10).until(
    lambda a: browser.find_element(By.XPATH, "//span[text()='Save']"))
    save_avar = browser.find_element(By.XPATH, "//span[text()='Save']").click()
    time.sleep(3)

def check_change_avatar(browser):
    source = browser.find_element(By.XPATH,"//img[@alt='Opens profile photo']").get_attribute('src')
    return source

def check_change_banner(browser):
    try:
        source = browser.find_element(By.XPATH,"//a[contains(@href,'header_photo')]//img").get_attribute('src')
        return source
    except:
        source = 'xyz'
        return source

def check_ban_account(browser):
    try:
        WebDriverWait(browser, 15).until(
        lambda a: browser.find_element(By.XPATH,'//div[text()="What next?"]'))
        return True
    except:
        return False

def remove_phone(browser,password):
    browser.get('https://twitter.com/home')
    time.sleep(random.uniform(1, 2))
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//div[@aria-label='More menu items']"))   
    more_setting = browser.find_element(
        By.XPATH, "//div[@aria-label='More menu items']").click()
    time.sleep(random.uniform(1, 2))
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//span[text()='Settings and privacy']"))   
    setting_privacy = browser.find_element(
        By.XPATH, "//span[text()='Settings and privacy']").click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//span[text()='Account information']"))   
    account_information = browser.find_element(
        By.XPATH, "//span[text()='Account information']").click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//input[@type='password']"))   
    input_password = browser.find_element(
        By.XPATH, "//input[@type='password']").send_keys(password)
    time.sleep(random.uniform(1, 2))
    confirm_pass = browser.find_element(
        By.XPATH, "//span[text()='Confirm']").click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//span[text()='Phone']"))   
    button_phone = browser.find_element(
        By.XPATH, "//span[text()='Phone']").click()
    while True:
        try:
            WebDriverWait(browser, 10).until(lambda a: browser.find_element(
                By.XPATH, "//span[text()='Delete phone number']"))   
            delete_phone_number = browser.find_element(
                By.XPATH, "//span[text()='Delete phone number']").click()
            time.sleep(random.uniform(1, 2))
            confirm_delete_phone = browser.find_element(
                By.XPATH, "//span[text()='Delete']").click() # //span[text()='Delete']
            logging.info('Done Delete Phone')
            break
        except:
            logging.info('Pass Delete Phone')
            break


def reply(browser,message,image,reply_percent=False):
    WebDriverWait(browser,20).until(lambda a : browser.find_element(By.XPATH,'//div[@aria-label="Tweet text"]'))
    if reply_percent:
        random_reply = random.randint(1,100)
        if random_reply > 100 - int(reply_percent):
            comment = browser.find_element(By.XPATH,'//div[@aria-label="Tweet text"]')
            comment.click()
            comment.send_keys(f'{message}')
            time.sleep(1)
            image = os.getcwd() + f"\image_reply\{image}.jpg"
            send_image = browser.find_element(By.XPATH, "//input[@type='file']").send_keys(image)
            time.sleep(1)
            enter = browser.find_element(By.XPATH,'//div[@data-testid="tweetButtonInline"]')
            enter.click()
            time.sleep(2)
    else:
        comment = browser.find_element(By.XPATH,'//div[@aria-label="Tweet text"]')
        comment.click()
        comment.send_keys(message)
        time.sleep(1)
        image = os.getcwd() + f"\image_spam\{image}.jpg"
        send_image = browser.find_element(By.XPATH, "//input[@type='file']").send_keys(image)
        time.sleep(1)
        enter = browser.find_element(By.XPATH,'//div[@data-testid="tweetButtonInline"]')
        enter.click()
        time.sleep(2)
        
        

def spam_tweet(browser, keyword_spam, text_spam, image_name_spam):
    browser.get('https://twitter.com/home')
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']"))
    search_account = browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']").send_keys(keyword_spam)
    a = browser.find_element(
        by=By.XPATH, value="//input[@placeholder='Search Twitter']").send_keys(Keys.ENTER)
    WebDriverWait(browser, 20).until(lambda a: browser.find_elements(By.XPATH, "//div[@data-testid='reply']"))
    spams_tweet = browser.find_elements(By.XPATH, "//div[@data-testid='reply']")
    a = os.getcwd() + f"\image_spam\{image_name_spam}.jpg"
    t = random.randint(0, 5) #random tweet trong list tìm kiếm để spam
    spams_tweet[t].click()
    time.sleep(0.5)
    tweet_reply_spam = browser.find_element(By.XPATH, "//div[@class='public-DraftStyleDefault-block public-DraftStyleDefault-ltr']").send_keys(text_spam)
    time.sleep(0.5)
    spam_media = browser.find_element(By.XPATH, "//input[@type='file']").send_keys(a)
    time.sleep(1)
    cf_reply = browser.find_element(By.XPATH, "//span[text()='Reply']").click()


def create_tweet(browser,text,image):
    browser.get('https://twitter.com/home')
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        by=By.XPATH, value='//div[@aria-label="Tweet text"]'))
    tweet = browser.find_element(
        by=By.XPATH, value='//div[@aria-label="Tweet text"]').send_keys(text)
    picture = os.getcwd() + f"\image_nft_opensea\{image}.jpg"
    time.sleep(1)
    add_picture = browser.find_element(By.XPATH, "//input[@type='file']").send_keys(picture)
    time.sleep(2)
    submit = browser.find_element(By.XPATH,'//div[@data-testid="tweetButtonInline"]').click()
    time.sleep(3)
    
def follow_topic(browser):
    browser.refresh()
    time.sleep(5)
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//div[@aria-label='More menu items']"))   
    more_setting = browser.find_element(
        By.XPATH, "//div[@aria-label='More menu items']").click()
    WebDriverWait(browser, 10).until(lambda a: browser.find_element(
        By.XPATH, "//span[text()='Topics']"))   
    topics = browser.find_element(
        By.XPATH, "//span[text()='Topics']").click()   
    time.sleep(random.randint(1,4))
    WebDriverWait(browser, 10).until(lambda a:browser.find_elements(
        By.XPATH, "//div[@class='css-1dbjc4n r-4amgru r-1p6iasa']/div/div[1]")) 
    suggetsted_topics = browser.find_elements(
        By.XPATH, "//div[@class='css-1dbjc4n r-4amgru r-1p6iasa']/div/div[1]")
    suggetsted_topics[random.randint(1,4)].click()
    time.sleep(random.randint(1,4))
    suggetsted_topics[random.randint(5,9)].click()
    time.sleep(random.randint(1,4))
    suggetsted_topics[random.randint(10,14)].click()
    time.sleep(random.randint(1,4))




