import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- 1. 配置区域 ---
# [注意] 请确认此处路径是否正确，或者更新为新版本的 ChromeDriver
CHROME_DRIVER_PATH = 'E:/Develop/Chrome89/App/chromedriver.exe'
TARGET_URL = "https://joyo95.cc/auth/register"


# --- 2. 辅助函数 ---
def get_complex_password(length=12):
    """
    生成包含字母和数字的随机字符串
    (网页HTML中有密码强度检测，纯字母可能被判定为弱密码)
    """
    chars = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(chars) for i in range(length))
    return result_str


driver = None
subscription_url = None

try:
    # --- 3. 初始化浏览器 ---
    options = Options()
    # options.add_argument("--incognito") # 可选：是否无痕模式
    options.add_argument('--start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 禁用渲染器代码完整性检查，防止部分环境崩溃
    options.add_argument("--disable-features=RendererCodeIntegrity")

    service = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(options=options, service=service)

    wait_10s = WebDriverWait(driver, 10)
    wait_120s = WebDriverWait(driver, 120)  # 给足时间手动滑滑块

    # --- 4. 打开网页 ---
    print(f"正在打开网页: {TARGET_URL}")
    driver.get(TARGET_URL)

    # --- 5. 填写表单 ---
    print("正在定位并填写表单...")
    # HTML ID确认无误: name, email, passwd, repasswd
    username_field = wait_10s.until(EC.visibility_of_element_located((By.ID, "name")))
    email_field = wait_10s.until(EC.visibility_of_element_located((By.ID, "email")))
    pass1_field = wait_10s.until(EC.visibility_of_element_located((By.ID, "passwd")))
    pass2_field = wait_10s.until(EC.visibility_of_element_located((By.ID, "repasswd")))

    # 生成随机用户数据
    userid = get_complex_password(10)
    username_field.send_keys(userid)
    email_field.send_keys(userid + "@gmail.com")
    pass1_field.send_keys(userid)
    pass2_field.send_keys(userid)
    print(f"表单填充完成。用户: {userid}")

    # --- 6. 处理极验 (GeeTest) 滑块 ---
    # [核心修改] 新版网页是 Embed 模式，不需要点击按钮来呼出滑块，滑块直接显示。
    # 只需要等待用户手动滑动，并检测隐藏的 validation 输入框是否有值。

    print("-" * 30)
    print("【请注意】检测到嵌入式滑块。")
    print("请现在手动拖动滑块完成拼图...")
    print("脚本正在后台监测验证结果...")
    print("-" * 30)

    try:
        # 检测 name="geetest_validate" 的隐藏 input 标签。
        # 当滑块成功时，这个 input 的 value 会被填入一串乱码。
        wait_120s.until(
            lambda d: d.find_element(By.NAME, "geetest_validate").get_attribute("value") != ""
        )
        print("检测到验证码通过 (geetest_validate 已获取)！")
    except Exception as e:
        print("等待验证成功超时，请检查是否已手动完成滑块。")
        raise e

    # 稍微缓冲一下，防止JS动画未结束
    time.sleep(1)

    # --- 7. 点击“确认注册” ---
    # HTML ID确认无误: tos
    print("点击确认注册按钮...")
    register_btn = wait_10s.until(EC.element_to_be_clickable((By.ID, "tos")))
    register_btn.click()

    # --- 8. 处理 TOS 弹窗并确认 ---
    # HTML ID确认无误: tos_modal
    print("等待 TOS 弹窗...")
    wait_10s.until(EC.visibility_of_element_located((By.ID, "tos_modal")))

    # 缓冲，确保弹窗完全淡入
    time.sleep(0.5)

    print("点击'我同意'...")
    # HTML ID确认无误: reg
    agree_btn = wait_10s.until(EC.element_to_be_clickable((By.ID, "reg")))
    agree_btn.click()

    # --- 9. 等待跳转并获取“拷贝节点订阅链接” ---
    print("正在等待注册跳转 (跳转至 /user)...")
    try:
        wait_120s.until(EC.url_contains("/user"))
        print("跳转成功，当前位于用户中心。")
        print("正在寻找订阅链接...")

        # 注意：此处基于假设用户中心逻辑未变。
        # 寻找包含 'copy-text' 类名且包含 '拷贝节点订阅链接' 字样的元素
        target_link_xpath = "//a[contains(@class, 'copy-text') and contains(., '拷贝节点订阅链接')]"

        copy_element = wait_10s.until(
            EC.presence_of_element_located((By.XPATH, target_link_xpath))
        )

        # 优先获取 data-clipboard-text
        subscription_url = copy_element.get_attribute("data-clipboard-text")

        # 如果没有 data 属性，尝试 href
        if not subscription_url:
            subscription_url = copy_element.get_attribute("href")

        print("获取链接成功！")

    except Exception as e:
        print(f"提取链接时出错: {e}")
        print("说明: 注册可能已成功，但未能自动抓取链接(可能是页面加载慢或UI变动)。")
        print("建议: 登录浏览器手动查看。")

except Exception as e:
    print(f"自动化过程中发生错误: {e}")

finally:
    # --- 10. 结束 ---
    if driver:
        pass  # 保持开启

    os.system('cls' if os.name == 'nt' else 'clear')

    if subscription_url:
        print("\n" + "=" * 20)
        print("订阅链接:")
        print(subscription_url)
        print("=" * 20 + "\n")
    else:
        print("\n未能自动提取链接 (请在浏览器中手动查看)。")

    input("按任意键退出...")