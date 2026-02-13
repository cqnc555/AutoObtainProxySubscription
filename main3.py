# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import re
import sys
import requests
import random
import base64
import json
import subprocess
from bs4 import BeautifulSoup
sys.path.append('')
from urllib.parse import unquote


def print_hi(path,lastword):
    # 读取JSON文件
    f = open(path + "guiNConfig.json", "r", encoding="UTF-8")
    data = json.loads(f.read())
    data['vmess'][0]["id"] = lastword
    data['vmess'][1]["id"] = lastword
    data['vmess'][2]["id"] = lastword
    f = open(path + "guiNConfig.json", 'w', encoding='UTF-8')
    # 字典转为字符串
    jsonobj = json.dumps(data)
    f.write(jsonobj)
    f.close()

def start_v2ray(path):
    try:
        # 替换成实际启动V2Ray的命令，这里只是一个示例
        # 假设V2Ray的可执行文件位于 /path/to/v2ray
        # 你可能需要根据实际情况修改启动命令  popen代替run方法，可以后台运行软件与当前py线程无关
        subprocess.Popen([path+'v2rayN.exe'])
        print("V2Ray 已成功启动")
    except Exception as e:
        print(f"启动V2Ray时出现错误: {e}")


def close_v2ray():
    try:
        # 替换成实际关闭V2RayN的命令，这里假设使用taskkill命令
        # taskkill是Windows上用于终止进程的命令
        # /IM参数指定要终止的进程名，这里假设V2RayN的进程名为v2rayN.exe

        subprocess.run(['taskkill', '/IM', 'v2rayN.exe', '/F'])
        print("V2RayN 已成功关闭")
    except Exception as e:
        print(f"关闭V2RayN时出现错误: {e}")


def extract_username(email):
    match = re.search(r'@(.*?):', email)
    return match.group(1) if match else None


def extract_between_colon_and_pound(input_str):
    # 正则表达式匹配冒号和#号之间的内容
    pattern = r":(.*?)#"
    match = re.search(pattern, input_str)
    if match:
        return match.group(1)
    else:
        return None


def get_hashtag_content(text):
    # 使用split()分割字符串，然后取第一个元素
    hashtag = text.split('#')[1] if '#' in text else None
    return hashtag

def get_last_lastword(url):
    requests_get = requests.get(url)
    # 将响应转为html对象
    obj_html = BeautifulSoup(requests_get.text, 'html.parser')
    # 解析网页对象获得 class = language-plaintext highlighter-rouge 的标签
    lastword = obj_html.find('div', class_='language-plaintext highlighter-rouge').text
    # 拿到第一行的内容
    lastword = lastword.split('\n')[0]
    print(lastword)
    # 从ss://开始截取，到第一个@结束，不包含ss://和@，即为订阅地址
    # lastword = lastword[lastword.find('ss://') + 5:lastword.find('@')]
    # if (len(lastword) % 3 == 1):
    #     lastword += "=="
    # elif (len(lastword) % 3 == 2):
    #     lastword += "="
    #
    #     # 是同base64解码
    # lastword = base64.urlsafe_b64decode(lastword)
    # # 取b'chacha20-ietf-poly1305:b889207f-aa08-4a9c-ace9-6e1335d9eb69' 中的b889207f-aa08-4a9c-ace9-6e1335d9eb69
    # lastword = lastword.decode('utf-8').split(':')[1]
    # return lastword
def get_v2ray_proxy(url):
    requests_get = requests.get(url)
    # 将响应转为html对象
    obj_html = BeautifulSoup(requests_get.text, 'html.parser')
    # 解析网页对象获得 class = language-plaintext highlighter-rouge 的标签
    lastword = obj_html.find('div', class_='language-plaintext highlighter-rouge').text
    # 拿到第一行的内容
    lastword = lastword.split('\n')[0]
    print('获取代理链接成功')
    return lastword

def flash_proxy(path,v2ray_proxy_url):
    # 读取JSON文件
    guiNConfig = open(path + "guiNConfig.json", "r", encoding="UTF-8")
    data = json.loads(guiNConfig.read())

    new_id = v2ray_proxy_url[v2ray_proxy_url.find('ss://') + 5:v2ray_proxy_url.find('@')]
    if (len(new_id) % 3 == 1):
        new_id += "=="
    elif (len(new_id) % 3 == 2):
        new_id += "="
    new_id = base64.urlsafe_b64decode(new_id)
    # 取b'chacha20-ietf-poly1305:b889207f-aa08-4a9c-ace9-6e1335d9eb69' 中的b889207f-aa08-4a9c-ace9-6e1335d9eb69
    new_id = new_id.decode('utf-8').split(':')[1]
    new_address = extract_username(v2ray_proxy_url)
    new_port = extract_between_colon_and_pound(v2ray_proxy_url)
    remarks = get_hashtag_content(v2ray_proxy_url)
    new_remarks = unquote(remarks)

    data['vmess'][0]["id"] = new_id
    data['vmess'][0]["address"] = new_address
    data['vmess'][0]["port"] = new_port
    data['vmess'][0]["remarks"] = new_remarks

    f = open(path + "guiNConfig.json", 'w', encoding='UTF-8')
    # 字典转为字符串
    jsonobj = json.dumps(data)
    f.write(jsonobj)
    f.close()


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # lastword = get_last_lastword(url="https://abshare.github.io/")
    v2ray_proxy_url = get_v2ray_proxy(url="https://abshare.github.io/")
