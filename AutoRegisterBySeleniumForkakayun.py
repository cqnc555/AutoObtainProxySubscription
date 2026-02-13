import sys

from selenium.common import TimeoutException

sys.path.append('')

import random
import string
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def generate_random_string(length):
    letters = string.ascii_letters + string.digits  # 包含字母和数字
    return ''.join(random.choice(letters) for _ in range(length))

def runapp(url = 'https://www.douluoyun.lol/auth/register'):
    # 设置Chrome
    options = Options()
    options.add_argument("--incognito")  # 启用无痕模式
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # 解决共享内存问题
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options, service=Service('E:/Develop/Chrome89/App/chromedriver.exe'))
    driver.maximize_window()
    driver.implicitly_wait(1)
    driver.get(url)
    # element = driver.find_element_by_id('name')  # 根据元素ID查找元素
    element = driver.find_element(By.ID, value="name")
    random_string = generate_random_string(8)
    element.send_keys(random_string)

    element = driver.find_element(By.ID, value="email")
    element.send_keys(random_string)

    element = driver.find_element(By.ID, value="passwd")
    element.send_keys(random_string)

    element = driver.find_element(By.ID, value="repasswd")
    element.send_keys(random_string)

    button = driver.find_element(By.CLASS_NAME, value="geetest_radar_tip")  # 验证按钮
    button.click()

    while True:
        if "验证成功" in driver.page_source:
            print("验证成功，继续执行后续操作")
            break
        time.sleep(2)
    # driver.find_element(by="xpath",value='//*[@id="embed-captcha"]/div/div[2]/div[2]/div/div[2]/span[1]')

    # button = driver.find_element(by="class name",value="geetest_slider_button")  # 滑块按钮

    # time.sleep(20)

    wait = WebDriverWait(driver, 1)

    try:
        # 注册确认按钮
        register_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "register-confirm"))
        )
        register_btn.click()

        # 处理SweetAlert确认弹窗
        sweet_alert = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".swal2-confirm.swal2-styled"))
        )
        sweet_alert.click()

        # 处理可能出现的模态框
        try:
            modal_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary[data-dismiss='modal']"))
            )
            modal_btn.click()
        except TimeoutException:
            pass

        # 每日签到操作
        checkin_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@onclick='checkin()' and contains(., '每日签到')]"))
        )
        checkin_btn.click()

        # 签到确认弹窗
        try:
            confirm_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.swal2-confirm.swal2-styled"))
            )
            confirm_btn.click()
        except TimeoutException:
            pass

    except TimeoutException as e:
        print(f"自动化操作失败: {str(e)}")
        raise

    # 找到订阅地址
    element = driver.find_element(By.CSS_SELECTOR,
                                  "a.btn.btn-icon.icon-left.btn-primary.btn-v2ray.copy-text.btn-lg.btn-round")
    # 获取 V2Ray 链接 (例如: https://.../link/...?sub=3)
    v2ray_url = element.get_attribute("data-clipboard-text")

    # 生成 Clash 链接 (通过替换参数 sub=3 -> clash=1)
    clash_url = v2ray_url.replace("sub=3", "clash=1")

    # --- 打印结果 ---
    print("-" * 30)
    print("注册网站: " + url)
    print("账号: " + random_string + "@gmail.com")
    print("密码: " + random_string)
    print("-" * 30)
    print("【V2Ray 订阅地址】:")
    print(v2ray_url)
    print("-" * 30)
    print("【Clash 订阅地址】:")
    print(clash_url)
    print("-" * 30)
    driver.quit()
    input("按任意键继续...")




if __name__ == '__main__':
    # url = 'https://www.kakayun.art/auth/register'
    # url = 'http://a.reoen.top/auth/register'
    # url = 'https://www.recear.xyz/auth/register'
    runapp(sys.argv[1])