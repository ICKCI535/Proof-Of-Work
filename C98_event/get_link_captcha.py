from imap_tools import MailBox, A
import random
import time
import re


def get_otp_link(imap_host="imap.gmail.com", imap_user="", imap_pass="", imap_user_old=""):  # fix algorithm
    while True:
        time.sleep(random.randint(1, 4))
        try:
            with MailBox(imap_host).login(imap_user_old, imap_pass, "INBOX") as mailbox:
                find = False
                mails = mailbox.fetch(
                    A(from_='no-reply@coin98.com', seen=False))
                for msg in mails:
                    captcha_img = re.findall(
                        '"https://information.coin98.services/api/otp.*alt="OTP CODE"',
                        msg.html,
                    )
                    captcha_img = captcha_img[0]
                    captcha_img = captcha_img.replace('"https', 'https')
                    captcha_img = captcha_img.replace('" alt="OTP CODE"', '')
                    print(captcha_img)
                    print(msg.to)
                    with open('link_captcha.txt', 'a') as a:
                        a.write(f'{captcha_img}|{msg.to[0]}\n')
        except Exception as e:
            print(e)
            continue


link = get_otp_link(imap_user='',
                    imap_pass='trczpdakbgbbkfjq', imap_user_old='vuquyem4567av@gmail.com')
