import requests
import string
import random
import asyncio
import os
import sys
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
sys.path.append('')
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(current_dir)
sys.path.append(project_root)
sys.path.append("E:/PythonCode/CF-Clearance-Scraper")
# 禁用不安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 导入模块 ---
# 尝试直接导入，如果失败则添加当前路径
try:
    from get_cf_ref import get_cf_cookie
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from get_cf_ref import get_cf_cookie

import util_generate_user

# --- 配置区域 ---
CONFIG = {
    "HOST": "cloud.dingdangyun.top",
    "PROXY": "http://127.0.0.1:7890",
    "CHROME_PATH": r"D:\Soft\Chrome140\chrome.exe", # 如果环境变量里没有，请取消注释并填入路径
    "HEADLESS": True,  # 调试时设为 False，正式运行设为 True
}

BASE_URL = f"https://{CONFIG['HOST']}"


# --- 自定义 SSL 适配器 (解决 Key too weak 问题) ---
class WeakCipherAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers='DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super(WeakCipherAdapter, self).init_poolmanager(*args, **kwargs)


# 全局 Session
session = requests.Session()
session.mount('https://', WeakCipherAdapter())


def generate_random_string(length=8):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def get_common_headers(user_agent: str, cf_clearance: str) -> dict:
    """生成通用的请求头，确保 UA 与 Selenium 浏览器一致"""
    return {
        "Host": CONFIG['HOST'],
        "Connection": "keep-alive",
        # 这里的 sec-ch-ua 尽量模糊化，因为 Requests 很难完美模拟。
        # 如果服务端校验非常严格，这里可能需要根据 user_agent 解析版本号动态生成
        "sec-ch-ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": user_agent,  # [重要] 必须与浏览器一致
        "Origin": BASE_URL,
        "Referer": BASE_URL,
        "Cookie": f"cf_clearance={cf_clearance}"
    }


def register(cf_data: dict):
    """
    注册函数
    :param cf_data: 包含 cf_clearance 和 user_agent 的字典
    """
    url = f"{BASE_URL}/api/v1/passport/auth/register"

    cf_clearance = cf_data['cf_clearance']
    user_agent = cf_data['user_agent']

    headers = get_common_headers(user_agent, cf_clearance)

    user_name = util_generate_user.get_complex_username()
    email = util_generate_user.get_random_email()
    payload = {
        "email": email,
        "password": user_name
    }

    proxies = {
        'http': CONFIG['PROXY'],
        'https': CONFIG['PROXY']
    }

    try:
        logging.info(f"正在注册: {email}")
        response = session.post(url, headers=headers, data=payload, proxies=proxies, verify=False)

        if response.status_code == 200:
            resp_json = response.json()
            if 'data' in resp_json:
                auth_data = resp_json['data']['auth_data']
                token = resp_json['data']['token']
                logging.info("注册成功!")
                logging.info(f"Token: {token}")
                return auth_data
            else:
                logging.error(f"注册响应数据异常: {resp_json}")
                return None
        else:
            logging.error(f"注册失败 (状态码 {response.status_code}): {response.text}")
            return None

    except Exception as e:
        logging.error(f"注册请求异常: {e}")
        return None


def get_subscribe(auth_data: str, cf_data: dict):
    """
    获取订阅
    """
    if not auth_data:
        return

    url = f"{BASE_URL}/api/v1/user/getSubscribe"

    cf_clearance = cf_data['cf_clearance']
    user_agent = cf_data['user_agent']

    headers = get_common_headers(user_agent, cf_clearance)

    # 覆盖或追加特定的 Header
    headers["Authorization"] = auth_data
    # 更新 Cookie，追加 auth_data
    headers[
        "Cookie"] = f"auth_data=%7B%22site%22%3A%22%E5%B8%83%E5%92%95%22%2C%22value%22%3A%22{auth_data}%22%7D; cf_clearance={cf_clearance}"

    proxies = {
        'http': CONFIG['PROXY'],
        'https': CONFIG['PROXY']
    }

    try:
        logging.info("正在获取订阅信息...")
        response = session.get(url, headers=headers, proxies=proxies, verify=False)

        if response.status_code == 200:
            try:
                data = response.json()
                if 'data' in data and 'subscribe_url' in data['data']:
                    sub_url = data['data']['subscribe_url']
                    logging.info(f"✅ 订阅地址获取成功: ")
                    logging.info(sub_url)
                else:
                    logging.warning(f"未找到订阅地址: {data}")
            except ValueError:
                logging.error("解析响应 JSON 失败")
        else:
            logging.error(f"获取订阅失败 (状态码 {response.status_code}): {response.text}")

    except Exception as e:
        logging.error(f"获取订阅请求异常: {e}")


async def main():
    target_url = BASE_URL
    logging.info(f"开始任务，目标: {target_url}")

    # 1. 获取 CF 验证信息 (异步)
    cf_result = await get_cf_cookie(
        url=target_url,
        proxy=CONFIG['PROXY'],
        chrome_path=CONFIG['CHROME_PATH'],
        headless=CONFIG['HEADLESS']
    )

    if cf_result:
        logging.info("Cloudflare 验证通过，开始执行业务逻辑...")

        # 2. 注册 (同步)
        auth_data = register(cf_result)

        # 3. 获取订阅 (同步)
        if auth_data:
            get_subscribe(auth_data, cf_result)
    else:
        logging.critical("无法通过 Cloudflare 验证，程序终止。")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("用户中断程序")
    finally:
        input("\n按回车键退出...")