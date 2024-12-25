import sys
# 因为是绿色版python 设置当前目录添加到自定义环境变量
# 需要先配置环境变量，否则会提示导入同目录的包不存在
sys.path.append('')
import re
import base64
import urllib.parse
import requests
import json
import handle_v2ray

# 禁用安全请求警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_proxy(url):
    resp = requests.get(url, verify=False)
    resp_text = resp.text
    pattern = r"ss://[^\s]+"
    ss_links = re.findall(pattern, resp_text)

    return ss_links

def handle_proxy_list(proxy_list):
    pattern = r"ss://(.*?)@(.*?)#(.*)"
    new_proxy_list = []
    for proxy_str in proxy_list:
        if (len(proxy_str) == 0):
            continue
        match = re.search(pattern, proxy_str)
        if match:
            pass_word = match.group(1)  # ss:// 和 @ 之间的内容
            url_prot = match.group(2)  # @ 和 # 之间的内容
            note = match.group(3)  # # 之后的内容
            pass_word2 = base64.b64decode(pass_word+'=')
            d_screar_way,d_pass_word = pass_word2.decode('utf-8').split(':')
            d_url,d_prot = url_prot.split(':')
            d_note = urllib.parse.unquote(note)
            proxy_dict = {}
            proxy_dict['d_pass_word'] = d_pass_word
            # print(d_pass_word)
            proxy_dict['d_url'] = d_url
            proxy_dict['d_prot'] = d_prot
            proxy_dict['d_note'] = d_note
            new_proxy_list.append(proxy_dict)
        else:
            print("匹配失败")
    return new_proxy_list

def read_config():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config


if __name__ == '__main__':
    # url = 'https://github.com/abshare/abshare.github.io'
    # url = 'https://hub.gitmirror.com/https://raw.githubusercontent.com/mksshare/mksshare.github.io/main/README.md'
    # path = 'E:\\v2rayN-Core\\'
    # path = 'F:\\FQ\\v2rayN\\'
    config = read_config()
    url = config['url_direct']
    path = config['path']
    proxy_list = get_proxy(url)
    new_proxy_list = handle_proxy_list(proxy_list)
    handle_v2ray.write_config_file(path, new_proxy_list)