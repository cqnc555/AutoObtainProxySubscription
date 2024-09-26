import sys
# 因为是绿色版python 设置当前目录添加到自定义环境变量
# 需要先配置环境变量，否则会提示导入同目录的包不存在
sys.path.append('')
import re
import base64
import urllib.parse
import requests
import json
import subprocess

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

def close_v2ray():
    try:
        # 替换成实际关闭V2RayN的命令，这里假设使用taskkill命令
        # taskkill是Windows上用于终止进程的命令
        # /IM参数指定要终止的进程名，这里假设V2RayN的进程名为v2rayN.exe
        subprocess.run(['taskkill', '/IM', 'v2rayN.exe', '/F'])
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
    f = open(path+"guiNConfig.json", 'w', encoding='UTF-8')
    # 字典转为字符串
    jsonobj = json.dumps(data)
    f.write(jsonobj)
    f.close()
    start_v2ray(path)
    pass


if __name__ == '__main__':
    # url = 'https://github.com/abshare/abshare.github.io'
    # url = 'https://github.com/mksshare/mksshare.github.io'
    # url = 'https://ablnk.absslk.xyz/zI3RCuq'
    # url = 'https://hub.gitmirror.com/https://raw.githubusercontent.com/abshare/abshare.github.io/main/README.md'
    # url = 'https://hub.gitmirror.com/https://raw.githubusercontent.com/mksshare/mksshare.github.io/main/README.md'
    # path = 'E:\\v2rayN-Core\\'
    # path = 'F:\\FQ\\v2rayN\\'
    config = read_config()
    url = config['url_direct']
    path = config['path']
    proxy_list = get_proxy(url)
    new_proxy_list = handle_proxy_list(proxy_list)
    write_config_file(path, new_proxy_list)