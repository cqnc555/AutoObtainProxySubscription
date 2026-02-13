from flask import Flask, Response
import requests
import base64

app = Flask(__name__)

# ================= 配置区域 =================

# 1. 这里填你的【真实】订阅地址（被墙的那个链接）
REAL_SUB_URL = "https://a.guguyundingyue.xyz/a2/b1/client/sub?token=e56019470108b397dfc59e312c392b15"
REAL_SUB_URL = "https://www.dingdangdingyue.top/c12/b33/client/sub?token=e0babc0fdad1835b08f1bcba0e34e6cd"

# 2. 这里填你的 V2Ray 代理地址
# V2RayN 默认通常是 10809，Clash 是 7890，请根据实际情况修改
PROXY_URL = "http://127.0.0.1:10809"


# ===========================================

@app.route('/')
def subscription():
    print(f"正在通过代理 {PROXY_URL} 获取远程订阅...")

    # 设置代理配置
    proxies = {
        "http": PROXY_URL,
        "https": PROXY_URL,
    }

    # 3. 【关键】伪装配置
    # 这里模仿了常见的 Clash 客户端
    HEADERS = {
        "User-Agent": "ClashforWindows/0.19.29",  # 伪装成 Clash for Windows
        # 如果上面这个不行，可以尝试换成下面这个更通用的：
        # "User-Agent": "Clash/1.16.0",
        "Accept": "*/*",
        "Connection": "keep-alive"
    }

    try:
        # 通过代理访问真实的订阅地址
        # timeout设置超时时间，防止卡死
        resp = resp = requests.get(
            REAL_SUB_URL,
            headers=HEADERS,  # 添加伪装头
            proxies=proxies,
            timeout=15,       # 增加一点超时时间
            verify=False      # 如果遇到 SSL 报错（如 self-signed cert），可以设为 False
        )
        print(resp.text)
        if resp.status_code == 200:
            print("获取成功！")
            # 直接返回获取到的内容（通常已经是 Base64 或者 YAML）
            # 我们原样转发给 FClash
            return Response(resp.text, mimetype='text/plain')
        else:
            return Response(f"Error: 远程服务器返回 {resp.status_code}", status=500)

    except Exception as e:
        print(f"获取失败: {e}")
        return Response(f"本地代理获取失败: {e}", status=500)


if __name__ == '__main__':
    print("本地转发服务器已启动！")
    print("请在 FClash 中设置订阅地址为: http://127.0.0.1:80/")
    app.run(host='0.0.0.0', port=80)