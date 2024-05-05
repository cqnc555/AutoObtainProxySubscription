import sys
sys.path.append('')
import time
import geetest_slide
import requests
import random
import string
import json
import subprocess
from bs4 import BeautifulSoup

# 禁用安全请求警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置Chrome的环境变量（也可以直接指定路径）
# 因为是绿色版python 设置当前目录添加到自定义环境变量
# 需要先配置环境变量，否则会提示导入同目录的包不存在
sys.path.append('')

# 添加返回值
def register_web(url,validate):
    # 随机获取8位数的字符串
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # 参数放在一个字典中
    data = {
        'email': ran_str + '@163.com',
        'name': ran_str,
        'passwd': ran_str,
        'repasswd': ran_str,
        'code': 0,
        'geetest_challenge': validate['geetest_challenge'],
        'geetest_validate': validate['geetest_validate'],
        'geetest_seccode': validate['geetest_seccode']

    }
    # 设置请求头 新版新增cookie，以防失败
    headers = {
        'cookie': validate['set-cookie'],
        # 'cookie': 'Cookie: GeeTestUser=0b273d6d8c36d658f33b8b35fb3b93c2',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    }
    # 发起post请求
    response = requests.post(url+"/auth/register", data=data, headers=headers, verify=False)
    # 获取响应的内容
    resp = json.loads(response.text)
    if resp['ret'] == 1:
        print('注册成功，账户为：', ran_str)
        return ran_str
    else:
        # 抛出异常结束程序
        raise Exception('注册失败，原因：' + resp['msg'])


# 添加返回值
def login_web(url, ran_str):
    # 参数放在一个字典中
    data = {
        'email': ran_str + '@163.com',
        'passwd': ran_str
    }
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    }
    # 发起post请求
    response = requests.post(url+"/auth/login", data=data, headers=headers, verify=False)
    if json.loads(response.text)['ret'] == 1:
        print('登陆成功，正在获取Cooike')
        setCookie = response.headers['Set-Cookie']
        # 获取响应的内容,获取cookie
        # 遍历cookie,拼接成一个字符串
        cookies = ''
        for cookie in response.cookies:
            cookies += cookie.name + '=' + cookie.value + ';'
        # 返回cookie
        return cookies
    else:
        # 抛出异常结束程序
        raise Exception('登陆失败，原因：' + response.text['msg'])

# 发送签到请求
def checkin_web(url, cookies):
    # 设置请求头,并携带cookie
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        'Cookie': cookies
    }
    # 发起post请求
    resp = requests.post(url+"/user/checkin", headers=headers, verify=False)
    if json.loads(resp.text)['ret'] == 1:
        print('签到成功')
    else:
        # 抛出异常结束程序
        raise Exception('签到失败，原因：' + resp['msg'])

# 获取订阅地址
def get_v2ray_url(url, cookies):
    # 设置请求头,并携带cookie
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        'Cookie': cookies
    }
    # 发起get请求
    resp = requests.get(url+"/user", headers=headers, verify=False)
    # 判断是否请求成功
    if resp.status_code != 200:
        # 抛出异常结束程序
        raise Exception('获取订阅地址失败，请手动复制账号+@163.com邮箱，密码同账号手动登录获取订阅地址！')
    else:
        print('获取订阅地址成功')
    # 转为html对象
    obj_html = BeautifulSoup(resp.text, 'html.parser')
    # 获取订阅地址
    v2ray_url = obj_html.find('a', class_='btn btn-icon icon-left btn-primary btn-v2ray copy-text btn-lg btn-round')['data-clipboard-text']
    print('订阅地址：', v2ray_url)
    return v2ray_url

def read_config():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config

# 写入配置文件
def write_config_file(path,v2ray_url):
    # 关闭v2rayN
    close_v2ray()
    # 读取JSON文件
    f = open(path+"guiNConfig.json", "r", encoding="UTF-8")
    data = json.loads(f.read())
    data['subItem'][0]['url'] = v2ray_url
    f = open(path+"guiNConfig.json", 'w', encoding='UTF-8')
    # 字典转为字符串
    jsonobj = json.dumps(data)
    f.write(jsonobj)
    f.close()
    start_v2ray(path)

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

if __name__ == '__main__':
    # url = 'https://www.ytdy666.buzz' # 不支持v2ray 但是支持ssr
    # url = 'https://www.douluoyun.lol'
    # url = 'https://www.kakayun.homes'
    # url = 'https://www.paofu.cloud'
    # path = 'E:\\v2rayN-Core\\'
    # path = 'F:\\FQ\\v2rayN\\'

    config = read_config()
    url = config['url']
    path = config['path']
    validate = geetest_slide.get_validate(url)
    ran_str = register_web(url,validate)
    cookies = login_web(url, ran_str)
    checkin_web(url, cookies)
    v2ray_url = get_v2ray_url(url, cookies)
    write_config_file(path, v2ray_url)
    print('程序执行完毕')
    time.sleep(15)