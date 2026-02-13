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


domain = "www.布咕云.com"
# domain = "cloud.jiyuncloud.top"
# domain = "cloud.dingdangyun.top"
punycode_domain = domain.encode("idna").decode("utf-8")

def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # 包含字母和数字
    return ''.join(random.choice(letters) for _ in range(length))

def registeer():
    # 1. 目标 URL (Host + Path)
    # 注意：xn--9kq89l54i.com 是中文域名的 Punycode 编码
    url = f"https://{domain}/api/v1/passport/auth/register"

    # 2. 完整的请求头设置
    headers = {
        "Host": punycode_domain,
        "Connection": "keep-alive",
        "sec-ch-ua-platform": '"Windows"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
        "Content-Type": "application/x-www-form-urlencoded",
        "sec-ch-ua-mobile": "?0",
        "Origin": f"https://{punycode_domain}",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": f"https://{punycode_domain}/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        # "Accept-Encoding": "gzip, deflate", # 建议注释掉：requests 会自动处理压缩和解压，手动强制可能会导致返回乱码
        # "Content-Length": "44"              # 必须注释掉：requests 会根据 data 内容自动计算准确长度
    }

    # 3. 请求体数据 (Data)
    # requests 会自动将字典转换为 key=value&key=value 格式，并自动处理 URL 编码

    user_name = generate_random_string(10)

    payload = {
        "email": f"{user_name}@gmail.com",  # 这里填原始字符，不要填 %40
        "password": user_name
    }

    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    # 4. 发送 POST 请求
    try:
        # verify=False 用于忽略 SSL 证书验证（可选，防止报 SSLError）
        response = requests.post(url, headers=headers, data=payload,proxies=proxies, verify=False)

        # 打印状态码
        print(f"Status Code: {response.status_code}")

        # 打印响应内容 (通常是 JSON)
        # {
        #    "data" : {
        #       "auth_data" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgxMCwic2Vzc2lvbiI6IjFkZTIyNzRjNDUyZDA5NDRmY2FmMjVhN2I5MjQ1Yjc1In0.gx6GmTECMKxtVkuOMiH19ol64VX-4rxM02NfvrP6HOQ",
        #       "is_admin" : null,
        #       "token" : "9799d1b2c9e042018153dd08df417a84"
        #    }
        # }
        print(response.text)
        print("注册用户名:")
        print(f"{user_name}@gmail.com")
        print("注册密码:")
        print(user_name)
        print("token:")
        print(response.json()['data']['auth_data'])
        print("uid:")
        print(response.json()['data']['token'])
        return response.json()['data']['auth_data']
    except Exception as e:
        print(f"Request failed: {e}")


def getsub(token):
    # 1. 目标 URL
    # 域名 www.xn--9kq89l54i.com 是中文域名 (布咕.com) 的 Punycode
    url = f"https://{domain}/api/v1/user/getSubscribe"

    # 2. 请求头设置
    headers = {
        "Host": "www.xn--9kq89l54i.com",
        "Connection": "keep-alive",
        "sec-ch-ua-platform": '"Windows"',
        # 注意：这里的 Authorization 没有 "Bearer " 前缀，直接跟 Token，保持原样即可
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "sec-ch-ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": punycode_domain,
        "Accept-Language": "zh-CN,zh;q=0.9",
        # Cookie 直接作为 Header 传递最稳妥，防止自动编码导致格式不一致
        "Cookie": f"auth_data=%7B%22site%22%3A%22%E5%B8%83%E5%92%95%22%2C%22value%22%3A%22{token}%22%7D"
    }

    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    # 3. 发送 GET 请求
    try:
        # 忽略 SSL 警告 verify=False (抓包时常用)，如果是生产环境建议去掉 verify=False
        response = requests.get(url, headers=headers, proxies=proxies, verify=False)

        # 打印状态码
        print(f"Status Code: {response.status_code}")

        # 打印 JSON 结果
        # 如果返回的是乱码，可能是编码问题，requests.json() 通常能自动处理
        if response.status_code == 200:
            print(response.json())
            print(response.json()['data']['subscribe_url'])
        else:
            print(response.text)

    except Exception as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    token = registeer()
    # token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgxMCwic2Vzc2lvbiI6IjFkZTIyNzRjNDUyZDA5NDRmY2FmMjVhN2I5MjQ1Yjc1In0.gx6GmTECMKxtVkuOMiH19ol64VX-4rxM02NfvrP6HOQ'
    getsub(token)
    input(print("回车键关闭。"))