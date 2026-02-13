import urllib3
import requests


def register():

    url = "https://cloud.dingdangyun.top/api/v1/passport/auth/register"

    payload = {
        "email": "oBesTFgq4TeKvt@qq.com",
        "password": "oBesTFgq4TeKvt"
    }

    headers = {
        "Host": "cloud.dingdangyun.top",
        "Connection": "keep-alive",
        "sec-ch-ua-full-version-list": '"Chromium";v="134.0.6998.136", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.136"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-bitness": '"64"',
        "sec-ch-ua-model": '""',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-arch": '"x86"',
        "sec-ch-ua-full-version": "134.0.6998.136",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "sec-ch-ua-platform-version": '"10.0.0"',
        "Origin": "https://cloud.dingdangyun.top",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://cloud.dingdangyun.top/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "cf_clearance=38LoDmt0swkw_kmuTWcsw7NZ3dzHlJllNeE1r7ocxoc-1765302271-1.2.1.1-abD7G9kfHNc72jYY.n7uEQx.HBmruUJo08PRfo4cvYKXe7uqNVGhUc8nO5xHbaUA.S9TLfde_qtOnydqTc4GFqm1rYfJzUynBnIC7CXIewcMBF2KA.911iDl4wNGoV5UCj_Cy6Nl474YnJ0s5gsRBQd04IgXd8q5BJNtMWGtUUPKAFZepvTUXtWDOJUKMi3lfCkOWEZK0KJexiqCbIl5xDtcx..4hx89tsdVL2SQuuY"
    }

    # ---------------------------------------------------------
    # 设置代理 (请检查您的 V2Ray 软件底部显示的端口)
    # ---------------------------------------------------------

    # 【方案一】 使用 HTTP 协议 (最简单，无需额外安装库)
    # 默认端口通常是 10809，如果您的不同请修改
    proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }

    # 【方案二】 使用 SOCKS5 协议 (更稳定，但需安装依赖)
    # 前置要求：pip install requests[socks]  或  pip install pysocks
    # 默认端口通常是 10808
    # proxies = {
    #    'http': 'socks5://127.0.0.1:10808',
    #    'https': 'socks5://127.0.0.1:10808'
    # }

    try:
        # 在请求中加入 proxies 参数
        response = requests.post(url, data=payload, headers=headers, proxies=proxies,verify=False, timeout=10)

        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

    except requests.exceptions.ProxyError:
        print("连接失败：请检查 V2Ray 是否开启，以及端口号是否正确（常见为 10809 或 7890）。")
    except Exception as e:
        print(f"发生错误: {e}")

register()