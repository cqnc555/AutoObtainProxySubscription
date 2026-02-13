import requests
import string
import random
import os
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.path.append('')
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)


domain = "hongm.ilailian.com"
# domain = "cloud.jiyuncloud.top"
# domain = "cloud.dingdangyun.top"
punycode_domain = domain.encode("idna").decode("utf-8")

def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # 包含字母和数字
    return ''.join(random.choice(letters) for _ in range(length))

def registeer():
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-language": "zh-CN",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://hongm.ilailian.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://hongm.ilailian.com/",
        "sec-ch-ua": "\"Chromium\";v=\"133\", \"Not(A:Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    url = "https://hongm.ilailian.com/api/v1/passport/auth/register"
    data = {
        "email": "sdfsxc123@qq.com",
        "password": "sdfsxc123",
        "invite_code": "",
        "email_code": ""
    }
    response = requests.post(url, headers=headers, data=data)

    print(response.text)
    print(response)

    # {
    #     "status": "success",
    #     "message": "\u64cd\u4f5c\u6210\u529f",
    #     "data": {
    #         "token": "3fff05abda39804bc5a22b9a4b27d961",
    #         "auth_data": "Bearer 63NTiu0FxgVoZ1BuJJFXWkPidGo9FUvnLZQDMBIl03209320",
    #         "is_admin": null
    #     },
    #     "error": null
    # }


def getsub(token):
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer 63NTiu0FxgVoZ1BuJJFXWkPidGo9FUvnLZQDMBIl03209320",
        "cache-control": "no-cache",
        "content-language": "zh-CN",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://hongm.ilailian.com/",
        "sec-ch-ua": "\"Chromium\";v=\"133\", \"Not(A:Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    url = "https://hongm.ilailian.com/api/v1/user/getSubscribe"
    params = {
        "t": "1768839280909"
    }
    response = requests.get(url, headers=headers, params=params)

    print(response.text)
    print(response)

    # {
    #     "status": "success",
    #     "message": "\u64cd\u4f5c\u6210\u529f",
    #     "data": {
    #         "plan_id": 8,
    #         "token": "3fff05abda39804bc5a22b9a4b27d961",
    #         "expired_at": 1768925680,
    #         "u": 0,
    #         "d": 0,
    #         "transfer_enable": 5368709120,
    #         "email": "sdfsxc123@qq.com",
    #         "uuid": "5703f023-7b82-47b4-ac78-83c1046cca30",
    #         "device_limit": null,
    #         "speed_limit": null,
    #         "next_reset_at": null,
    #         "plan": {
    #             "id": 8,
    #             "group_id": 2,
    #             "transfer_enable": 5,
    #             "name": "\u6ce8\u518c\u8bd5\u7528",
    #             "prices": {
    #                 "yearly": null,
    #                 "monthly": null,
    #                 "onetime": null,
    #                 "quarterly": null,
    #                 "two_yearly": null,
    #                 "half_yearly": null,
    #                 "three_yearly": null,
    #                 "reset_traffic": null
    #             },
    #             "sell": 0,
    #             "speed_limit": null,
    #             "device_limit": 1,
    #             "show": false,
    #             "sort": null,
    #             "renew": false,
    #             "content": null,
    #             "tags": [],
    #             "reset_traffic_method": null,
    #             "capacity_limit": 1,
    #             "created_at": 1767865871,
    #             "updated_at": 1767951498
    #         },
    #         "subscribe_url": "https:\/\/hongm.ilailian.com\/s\/3fff05abda39804bc5a22b9a4b27d961",
    #         "reset_day": 1
    #     },
    #     "error": null
    # }

if __name__ == "__main__":
    token = registeer()
    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgxMCwic2Vzc2lvbiI6IjFkZTIyNzRjNDUyZDA5NDRmY2FmMjVhN2I5MjQ1Yjc1In0.gx6GmTECMKxtVkuOMiH19ol64VX-4rxM02NfvrP6HOQ'
    getsub(token)
    input(print("回车键关闭。"))