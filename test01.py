import time

import requests

# 从历史附件信息中提取的URL列表
url_list = [
    "http://www.hotmail.com/",
    "http://mail.qq.com/",
    "http://mail.163.com/",
    "http://24mail.chacuo.net/"
]



headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Chromium\";v=\"118\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "Referer": "https://www.limestart.cn/",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44'
}

def saveweb(payload):
    import requests
    import json

    url = "https://api.limestart.cn/backend/bookmark-v3"

    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer 429d34fcd7b921798a50f577b71dc6c7",  # 注意：请确保这是有效的token
        "content-type": "application/json",
        "sec-ch-ua": "\"Not=A?Brand\";v=\"99\", \"Chromium\";v=\"118\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://www.limestart.cn/",
        "Origin": "https://www.limestart.cn",
        "Cookie": "tmpuid=26c114be.53c6.4667.a07c.330b48fb8ef7; luckynum=21; luckyid=421; token=dy+zOuC5xj1JcG3v4BwIG6bcJqa7kHViykVEPYvXXSb5VcTFL7P0l5YHbSAl41BP0gOoRGynZy97W5TgW7++ckTrYKrZwt2RG93Jgafik9Edv58RtGHmg1R+ZeEFB3ZuWJITeor0+5dtUUIOZrET6LOZ074s346IQxt2RiNifc8=; acw_tc=79593ab517545787934885140ecb5ca1836093f6d1439d1571d84e5daa; cdn_sec_tc=79593ab517545787934885140ecb5ca1836093f6d1439d1571d84e5daa",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44'
    }

    # 构造请求体数据
    try:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),  # 将字典转换为JSON字符串
            timeout=10
        )

        print(f"状态码: {response.status_code}")
        print("响应内容:")
        print(response.json())  # 假设响应是JSON格式

    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    except json.JSONDecodeError:
        print(f"非JSON响应: {response.text}")

def check_site_info(url):
    api_url = f"https://api.limestart.cn/backend/site-info-v2?url={url}"
    try:
        response = requests.get(
            api_url,
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            print(f"成功获取 {url} 的信息")
            print("响应内容:", response.json())
        else:
            print(f"获取 {url} 信息失败，状态码: {response.status_code}")
            return False

        payload = {
            "folderId": "6894c12fe61637e6411d2cde",
            "icon": response.json()['icon'],
            "title": response.json()['title'],
            "url": url,
            "username": "771959111rv5p6i"
        }
        saveweb(payload)
        return True

    except requests.exceptions.RequestException as e:
        print(f"请求 {url} 时出现异常: {e}")
        return False


# 主循环处理所有URL
for url in url_list:
    print(f"\n正在处理: {url}")
    success = check_site_info(url)
    if not success:
        print(f"警告: {url} 处理失败")

    # 添加适当延迟以避免请求过于频繁
    time.sleep(1)


print("\n所有URL处理完成")
