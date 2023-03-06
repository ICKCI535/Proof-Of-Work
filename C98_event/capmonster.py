import requests
import json
import time

API_KEY = "53c07feb1b08e7ea84c07a162f0688fe"

def create_task():
    url = "https://api.capmonster.cloud/createTask"
    data = {
        "clientKey":API_KEY,
        "task":
        {
            "type":"HCaptchaTask",
            "websiteURL":"https://api.coin98.services/adapters/user/register",
            "websiteKey":"1cb79159-1c87-4b0c-94f0-3dad1125eaba",
            "proxyType":"https",
            "proxyAddress":"proxy.packetstream.io",
            "proxyPort":31111,
            "proxyLogin":"cuong.tran",
            "proxyPassword":"4f77IpNRZYifgljF_country-Vietnam",
            "userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
    }
    r = requests.post(url, json=data)
    return r.text

def get_task_result(task_id):
    url = "https://api.capmonster.cloud/getTaskResult"
    data = {"clientKey": API_KEY,"taskId": task_id}
    r = requests.post(url, json=data)
    return r.text

def main():
    task = create_task()
    if "taskId" not in task:
        print(task)
        return
    task_id = json.loads(task)["taskId"]
    # wait for task to complete
    while True:
        hcaptcha_response = get_task_result(task_id)
        if "gRecaptchaResponse" not in hcaptcha_response:
            if "processing" in hcaptcha_response:
                print("waiting")
                time.sleep(1)
                continue
            else:
                print(hcaptcha_response)
                return
        hcaptcha_response = json.loads(hcaptcha_response)["solution"]["gRecaptchaResponse"]
        print(hcaptcha_response)
        return hcaptcha_response

if __name__ == "__main__":
    main()