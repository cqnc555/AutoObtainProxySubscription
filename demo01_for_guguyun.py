from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def log_request_interceptor(request):
    """
    拦截器函数：当浏览器发起请求时触发
    在此处打印请求的 URL
    """
    print(f"[请求] {request.url}")

def main():
    # 1. 配置 selenium-wire 代理
    # 使用您要求的本地代理端口 10808
    wire_options = {
        'proxy': {
            'http': 'http://127.0.0.1:10808',
            'https': 'http://127.0.0.1:10808',
            'no_proxy': 'localhost,127.0.0.1'  # 排除本地地址不走代理
        },
        'verify_ssl': False  # 忽略 SSL 证书验证，防止代理抓包时报错
    }

    options = Options()
    options.add_argument("--incognito")  # 启用无痕模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # 解决共享内存问题
    options.add_argument('--start-maximized')

    # 3. 指定 ChromeDriver 路径
    # 参考自您提供的脚本 hz_register_selenium_xiaduola_ip.py 第 227 行
    driver_path = 'D:/Soft/Chrome140/chromedriver.exe'
    service = Service(driver_path)

    print(f"启动浏览器，使用代理: 127.0.0.1:10808，驱动路径: {driver_path}")

    # 4. 初始化浏览器
    driver = webdriver.Chrome(
        service=service,
        options=options,
        seleniumwire_options=wire_options
    )

    # 5. 绑定拦截器
    # 这一步是关键：每当有请求发生，都会调用 log_request_interceptor 打印地址
    driver.request_interceptor = log_request_interceptor

    try:
        # 6. 访问目标网站 (在此处替换为您要测试的网址)
        target_url = "https://cloud.guguyun.fun/#/register"
        print(f"正在访问页面: {target_url} ...")
        driver.get(target_url)

        # 保持页面打开一段时间，以便观察所有异步请求
        input("页面加载完毕。按回车键关闭浏览器...")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()