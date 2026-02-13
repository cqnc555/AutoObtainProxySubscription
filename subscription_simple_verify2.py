import sys
import time

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

# 获取临时邮箱
def get_tempemail():
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44'
    }
    # 设置请求参数
    # data = {
    #     'mailbox': ''
    # }
    # 发起get请求
    response = requests.post("https://temp-mail.org/mailbox", headers=headers, verify=False)
    # 获取响应的内容,解析json
    resp = json.loads(response.text)
    # print(resp["token"])
    print("获取的临时邮箱地址："+resp["mailbox"])
    return resp["token"],resp["mailbox"]

# 获取邮件内容
def get_email_content(token):
    # 等待5秒
    time.sleep(5)
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
        "authorization" : "Bearer "+token
        # "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiMjYzNDFkNjViMDQwNDEyNWIzZmYxMzQ2NDkyMjU1NDAiLCJtYWlsYm94Ijoic29oZXlpZjMzMEBlbGl4aXJzZC5jb20iLCJpYXQiOjE2OTcyOTU4Mjl9.YlTsqR5nFsiQLhQUZzydABU0IvgiGLpyv96hA7MtVAE"
    }
    # 发起get请求
    response = requests.get("https://web2.temp-mail.org/messages", headers=headers, verify=False)
    # 获取响应的内容,解析json
    resp = json.loads(response.text)
    id = resp['messages'][0]['_id']
    response = requests.get("https://web2.temp-mail.org/messages/"+id, headers=headers, verify=False)
    body = json.loads(response.text)['bodyHtml']
    # 获取body之后解析成HTML对象
    obj_html = BeautifulSoup(body, 'html.parser')
    # 获取验证码
    body = obj_html.find('span', style="font-family: 'Nunito', Arial, Verdana, Tahoma, Geneva, sans-serif; color: #ffffff; font-size: 20px; line-height: 30px; text-decoration: none; white-space: nowrap; font-weight: 600;").text
    print("获取的验证码为：" + body)
    return body


# 发送邮件验证码
def send_email(url,email):
    # 随机获取8位数的字符串
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # 参数放在一个字典中
    data = {
        'email': email
    }
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44'
    }
    # 发起post请求
    response = requests.post(url+"/api/v1/passport/comm/sendEmailVerify", data=data, headers=headers, verify=False)
    # response = requests.post(url+"/auth/send", data=data, headers=headers, verify=False)
    # 获取响应的内容
    resp = json.loads(response.text)
    # 判断是否发送成功
    if resp['ret'] == 1:
        print('发送邮件成功')
    else:
        # 抛出异常结束程序
        raise Exception('发送邮件失败，原因：' + resp['msg'])

# 添加返回值
def register_web(url,email,code):
    # 截取邮箱前缀
    mail_str = email.split("@")[0]
    # 参数放在一个字典中
    data = {
        'email': email,
        'name': mail_str,
        'passwd': mail_str,
        'repasswd': mail_str,
        'code': 0,
        'emailcode': code
    }
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
    }
    # 发起post请求
    response = requests.post(url+"/auth/register", data=data, headers=headers, verify=False)
    # 获取响应的内容
    resp = json.loads(response.text)
    if resp['ret'] == 1:
        print('注册成功，账户为：', email)
        return email
    else:
        # 抛出异常结束程序
        raise Exception('注册失败，原因：' + resp['msg'])


# 添加返回值
def login_web(url, email):
    # 参数放在一个字典中
    data = {
        'email': email,
        'passwd': email.split("@")[0]
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
    return v2ray_url

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
    url = 'https://portal.taronet.uk'
    # url = 'https://www.paofu.cloud'
    # url = 'https://vpiv.me' 不支持v2ray 但是支持ssr
    # token,email = get_tempemail()
    email = 'dinak83310@finfave.com'
    send_email(url,email)
    # code = get_email_content(token)
    # email = register_web(url,email,code)
    # cookies = login_web(url,email)
    # checkin_web(url,cookies)
    # v2ray_url = get_v2ray_url(url,cookies)
    # print(v2ray_url)
    # write_config_file('E:\\v2rayN-Core\\',v2ray_url)
    print('程序执行完毕')

