import sys
# 因为是绿色版python 设置当前目录添加到自定义环境变量
# 需要先配置环境变量，否则会提示导入同目录的包不存在
import time

sys.path.append('')
import re
import base64
import urllib.parse
import requests
import json
import subprocess
import yaml
from bs4 import BeautifulSoup

# 禁用安全请求警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置Chrome的环境变量（也可以直接指定路径）
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
}

def get_proxy(url):
    resp = requests.get(url,headers=headers)
    data_dict = yaml.safe_load(resp.text)
    return data_dict['proxies']


def handle_proxy_list(proxy_list):
    new_proxy_list = []
    for proxy_str in proxy_list:
        proxy_dict = {}
        proxy_dict['d_pass_word'] = proxy_str['password']
        proxy_dict['d_url'] = proxy_str['server']
        proxy_dict['d_prot'] = proxy_str['port']
        proxy_dict['d_note'] = proxy_str['name']
        new_proxy_list.append(proxy_dict)
    return new_proxy_list

def close_v2ray():
    try:
        # 替换成实际关闭V2RayN的命令，这里假设使用taskkill命令
        # taskkill是Windows上用于终止进程的命令
        # /IM参数指定要终止的进程名，这里假设V2RayN的进程名为v2rayN.exe
        subprocess.run(['taskkill', '/IM', 'v2rayN.exe', '/F'])
        time.sleep(5)
        print("V2RayN 已成功关闭")
    except Exception as e:
        print(f"关闭V2RayN时出现错误: {e}")

def start_v2ray(path):
    try:
        # 替换成实际启动V2Ray的命令，这里只是一个示例
        # 假设V2Ray的可执行文件位于 /path/to/v2ray
        # 你可能需要根据实际情况修改启动命令  popen代替run方法，可以后台运行软件与当前py线程无关
        subprocess.Popen([path+'v2rayN.exe'])
        print("V2Ray 已成功启动")
    except Exception as e:
        print(f"启动V2Ray时出现错误: {e}")

def write_config_file(path, new_proxy_list):
    # 关闭v2rayN
    close_v2ray()
    # 读取JSON文件
    f = open(path+"guiNConfig.json", "r", encoding="UTF-8")
    data = json.loads(f.read())
    new_proxy_list2 = []
    for index,new_proxy in enumerate(new_proxy_list):
        new_proxy_dict = {}
        new_proxy_dict['indexId'] = index
        new_proxy_dict['configVersion'] = 2
        new_proxy_dict['address'] = new_proxy['d_url']
        new_proxy_dict['port'] = new_proxy['d_prot']
        new_proxy_dict['id'] = new_proxy['d_pass_word']
        new_proxy_dict['alterId'] = 0
        new_proxy_dict['security'] = "chacha20-ietf-poly1305"
        new_proxy_dict['network'] = ''
        new_proxy_dict['remarks'] = new_proxy['d_note']
        new_proxy_dict['headerType'] = ''
        new_proxy_dict['requestHost'] = ''
        new_proxy_dict['path'] = ''
        new_proxy_dict['streamSecurity'] = ''
        new_proxy_dict['allowInsecure'] = "False"
        new_proxy_dict['configType'] = 3
        new_proxy_dict['testResult'] = ''
        new_proxy_dict['subid'] = ''
        new_proxy_dict['flow'] = ''
        new_proxy_dict['sni'] = ''
        new_proxy_dict['alpn'] = ''
        new_proxy_list2.append(new_proxy_dict)
    data['vmess'] = new_proxy_list2
    print(new_proxy_list2)
    f = open(path+"guiNConfig.json", 'w', encoding='UTF-8')
    # 字典转为字符串
    jsonobj = json.dumps(data)
    f.write(jsonobj)
    f.close()
    start_v2ray(path)
    pass


if __name__ == '__main__':
    # url = 'https://github.com/abshare/abshare.github.io'
    url = 'https://freemc.mcsslk.xyz/SVpFKXE'
    # url = 'https://freemc.mcsslk.xyz/Jjk3lTM'
    # url = 'https://abshare.github.io/'
    # path = 'E:\\v2rayN-Core\\'
    path = 'F:\\FQ\\v2rayN\\'
    proxy_list = get_proxy(url)
    new_proxy_list = handle_proxy_list(proxy_list)
    # print(new_proxy_list)

    # ran_str = register_web(url,validate)
    # cookies = login_web(url, ran_str)
    # checkin_web(url, cookies)
    # v2ray_url = get_v2ray_url(url, cookies)
    write_config_file(path, new_proxy_list)
    # get_v2ray_suburl(v2ray_url)
    # print('程序执行完毕，15S后自动结束本程序。')
    # time.sleep(15)