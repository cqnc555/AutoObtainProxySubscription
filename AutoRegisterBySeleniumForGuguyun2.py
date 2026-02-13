import os
import subprocess
import time
import random
import sys

# 第三方库导入
try:
    import pyautogui
    import pyperclip
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(f"缺少必要库: {e}")
    print("请运行: pip install selenium pyautogui pyperclip webdriver-manager")
    sys.exit(1)

# ================= 核心配置区域 =================

# 1. Chrome 浏览器主程序路径 (必须修改为您电脑上的真实路径)
# 常见路径：
# C:\Program Files\Google\Chrome\Application\chrome.exe
# C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
CHROME_PATH = r"D:/Soft/Chrome109/chrome.exe"

# 2. 用户数据目录 (脚本会自动创建，用于保存登录状态，避免重复验证 CF)
USER_DATA_DIR = os.path.join(os.getcwd(), "browser_profile")

# 3. 调试端口 (保持 9222 即可)
DEBUG_PORT = "9222"

# 4. 注册信息配置
REGISTER_DATA = {
    "email": "test_user_final_v3@gmail.com",  # 您的邮箱
    "password": "Password123!",  # 您的密码
    "verify_code": "",  # 验证码 (留空则脚本点击发送按钮)
    "invite_code": ""  # 邀请码 (可选)
}


# ===============================================

def kill_chrome():
    """强制关闭所有 Chrome 进程，防止端口占用"""
    print(">>> 清理旧的 Chrome 进程...")
    if os.name == 'nt':  # Windows
        os.system("taskkill /f /im chrome.exe >nul 2>&1")
        os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
    else:  # Mac/Linux
        os.system("pkill -9 chrome")


def launch_chrome():
    """通过命令行启动开启了调试端口的 Chrome"""
    if not os.path.exists(CHROME_PATH):
        print(f"!!! 错误: 找不到 Chrome，请检查 CHROME_PATH 路径是否正确: {CHROME_PATH}")
        return False

    if not os.path.exists(USER_DATA_DIR):
        os.makedirs(USER_DATA_DIR)

    # 构造启动命令
    # --remote-debugging-port: 开启调试端口
    # --user-data-dir: 指定独立配置，实现数据隔离和持久化
    # --no-first-run --no-default-browser-check: 禁止弹窗
    cmd = f'"{CHROME_PATH}" --remote-debugging-port={DEBUG_PORT} --user-data-dir="{USER_DATA_DIR}" --no-first-run --no-default-browser-check'

    print(f">>> 正在启动 Chrome (端口 {DEBUG_PORT})...")
    try:
        subprocess.Popen(cmd, shell=True)
        time.sleep(3)  # 等待浏览器完全启动
        return True
    except Exception as e:
        print(f"!!! 启动 Chrome 失败: {e}")
        return False


def random_sleep(min_t=0.5, max_t=1.5):
    """模拟人类操作的随机延迟"""
    time.sleep(random.uniform(min_t, max_t))


def human_input_gui(driver, element, text):
    """
    【核心函数】物理级模拟输入
    绕过 event.isTrusted 检测，防止网页自动后退
    """
    if not text:
        return

    try:
        # 1. 激活浏览器窗口 (确保 PyAutoGUI 打字打在浏览器里)
        # 这一步非常重要，必须让 Chrome 处于前台
        driver.switch_to.window(driver.current_window_handle)

        # 2. 使用 Selenium 点击元素，确保获得光标焦点
        # 使用 ActionChains 移动并点击，比直接 element.click() 更稳定
        actions = ActionChains(driver)
        actions.move_to_element(element).click().perform()

        # 3. 清除已有内容 (模拟 Ctrl+A -> Delete)
        # 不能用 element.clear()，因为那也是 Selenium 信号
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('delete')

        # 4. 使用剪贴板粘贴 (最快、最准、不干扰输入法)
        # 这种方式被浏览器视为用户的 "粘贴" 操作，isTrusted = true
        pyperclip.copy(text)
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')

        print(f"    -> [物理输入] 已填入: {text}")
        random_sleep(0.5, 1.0)

    except Exception as e:
        print(f"!!! 物理输入失败: {e}")


def run_automation():
    print(">>> 正在连接 Chrome 调试端口...")

    chrome_options = Options()
    # 核心：接管已启动的浏览器
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{DEBUG_PORT}")

    try:
        # 使用 webdriver_manager 自动下载匹配的驱动，解决 Unable to obtain driver 问题
        CHROMEDRIVER_PATH = "D:/Soft/Chrome109/chromedriver.exe"
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f">>> 连接成功！")
    except Exception as e:
        print(f"!!! 连接失败: {e}")
        return

    try:
        # 1. 注入防跳转补丁 (双重保险)
        driver.execute_script("""
            window.onbeforeunload = function() { return "脚本拦截了跳转"; };
        """)

        # 2. 导航到注册页
        target_url = "https://www.guguyun.fun/#/register"
        if "register" not in driver.current_url:
            print(f">>> 打开网址: {target_url}")
            driver.get(target_url)

        print(">>> [重要] 请确保 Chrome 窗口在前台，且不要移动鼠标！")
        print(">>> 等待页面加载 (如果遇到 Cloudflare，请手动点击)...")

        wait = WebDriverWait(driver, 60)

        # 使用 input-with-icon 定位，确保是加载出的表单
        email_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".input-with-icon input[type='text']")))
        print(">>> 页面加载完成，开始填表...")

        random_sleep(1, 2)

        # 3. 填写邮箱 (使用物理模拟)
        print(">>> 填写邮箱...")
        human_input_gui(driver, email_input, REGISTER_DATA['email'])

        # 4. 验证码流程
        if not REGISTER_DATA['verify_code']:
            print(">>> 尝试点击发送验证码...")
            try:
                # 定位发送按钮
                send_btn = driver.find_element(By.CLASS_NAME, "send-code-btn")

                # 高亮按钮
                driver.execute_script("arguments[0].style.border='3px solid red'", send_btn)

                # 点击按钮 (点击通常不会触发 isTrusted 校验，Selenium 点击即可)
                send_btn.click()

                print(">>> 点击成功！请去邮箱查看验证码。")
                print(">>> 脚本暂停 20 秒，等待您手动填入验证码，或者等脚本恢复后手动填写...")
                time.sleep(20)
            except:
                print("!!! 未找到发送按钮，跳过...")
        else:
            # 如果预设了验证码，直接填入
            try:
                code_input = driver.find_element(By.XPATH, "//input[@placeholder='验证码']")
                human_input_gui(driver, code_input, REGISTER_DATA['verify_code'])
            except:
                pass

        # 5. 填写密码 (使用物理模拟)
        print(">>> 填写密码...")
        # 找到所有密码框 (通常有两个: 密码 + 确认密码)
        pwd_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        for p_in in pwd_inputs:
            human_input_gui(driver, p_in, REGISTER_DATA['password'])

        # 6. 邀请码
        if REGISTER_DATA['invite_code']:
            print(">>> 填写邀请码...")
            try:
                inv_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, '邀请')]")
                human_input_gui(driver, inv_input, REGISTER_DATA['invite_code'])
            except:
                pass

        # 7. 提交注册
        print(">>> 准备提交...")
        try:
            # 根据您提供的HTML，定位包含"创建账户"文字的按钮
            submit_btn = driver.find_element(By.XPATH, "//button[contains(., '创建账户')]")

            # 高亮
            driver.execute_script("arguments[0].style.border='3px solid red'", submit_btn)

            print(">>> ✅ 流程结束！")
            print(">>> 请检查页面信息，并手动点击红框内的【创建账户】按钮。")

        except:
            print("!!! 未找到提交按钮")

        # 保持脚本不退出，维持浏览器连接
        input("\n>>> 按回车键结束脚本并关闭连接...")

    except Exception as e:
        print(f"!!! 运行出错: {e}")


if __name__ == "__main__":
    # 步骤 1: 清理环境
    kill_chrome()

    # 步骤 2: 启动浏览器
    if launch_chrome():
        # 步骤 3: 运行自动化
        run_automation()