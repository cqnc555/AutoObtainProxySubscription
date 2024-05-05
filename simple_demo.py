from pprint import pprint

import requests
import json

import random
import string


def register_web(url):
    # 随机获取8位数的字符串
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # 参数放在一个字典中
    data = {
        # 'email': ran_str + '@163.com',
        # 'name': ran_str,
        # 'passwd': ran_str,
        # 'repasswd': ran_str,
        # 'code': 0,
        # 'geetest_challenge': 'efb0b951cd3d1ac85cb302621ab0d4f5io',
        # 'geetest_validate': 'bb43d4655b42a564611da09934e2aec4',
        # 'geetest_seccode': 'bb43d4655b42a564611da09934e2aec4|jordan',

        'email': 'QDT42aH9ta465s'+'@gmail.com',
        'name': 'QDT42aH9ta465s',
        'passwd': 'QDT42aH9ta465s',
        'repasswd': 'QDT42aH9ta465s',
        'code': 0,
        'geetest_challenge': '14e9e9a9ad1264eca11fb4df31c77ceacx',
        'geetest_validate': '87c97836450a3484c1af0a26390780de',
        'geetest_seccode': '87c97836450a3484c1af0a26390780de|jordan'

    }
    # 设置请求头
    headers = {
        # 'accept': 'application/json, text/javascript, */*; q=0.01',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'zh-CN,zh;q=0.9',
        # 'content-length': str(len(str(data))),
        # 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'PHPSESSID=bp8279pj88sup3uum8b5q3tmde; lang=zh-cn',
        # 'origin': 'https://www.kakayun.homes',
        # 'referer': 'https://www.kakayun.homes/auth/register',
        # 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': "Windows",
        # 'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        # 'x-requested-with': 'XMLHttpRequest'
    }
    # 发起post请求
    response = requests.post(url+"/auth/register", data=data, headers=headers)
    pprint(response.text)
    # 获取响应的内容
    resp = json.loads(response.text)
    if resp['ret'] == 1:
        print('注册成功，账户为：', ran_str)
        return ran_str
    else:
        # 抛出异常结束程序
        raise Exception('注册失败，原因：' + resp['msg'])


if __name__ == '__main__':
    url = 'https://www.kakayun.homes'
    register_web(url)