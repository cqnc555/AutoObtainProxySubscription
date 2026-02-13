import os
import subprocess
import time
import sys
import random

try:
    import pyautogui
    import pyperclip
except ImportError:
    print("缺少必要库，请运行: pip install pyautogui pyperclip")
    sys.exit(1)

# ================= 配置区域 =================

# Chrome 路径 (请确保正确)
CHROME_PATH = r"D:/Soft/Chrome109/chrome.exe"
USER_DATA_DIR = os.path.join(os.getcwd(), "browser_profile")
# 注册信息
REGISTER_DATA = {
    "email": "test_user_physical@gmail.com",
    "password": "Password123!",
    "verify_code": "",  # 留空则尝试点击发送
    "invite_code": ""
}

# 目标网址
TARGET_URL = "https://www.guguyun.fun/#/register"


# ===========================================

def random_sleep(min_t=0.5, max_t=1.5):
    time.sleep(random.uniform(min_t, max_t))


def type_text(text):
    """
    使用剪贴板粘贴文本，模拟物理输入，
    且不受输入法影响，速度快。
    """
    if not text:
        return
    pyperclip.copy(text)
    # 稍微等待剪贴板写入
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    random_sleep(0.3, 0.8)


def run_pure_automation():
    # 1. 彻底关闭旧 Chrome，保证环境纯净
    print(">>> 清理旧进程...")
    # os.system("taskkill /f /im chrome.exe >nul 2>&1")

    # 2. 以普通用户模式启动 Chrome (无调试端口，神仙也测不出)
    print(f">>> 正在以【纯净模式】启动 Chrome...")
    if not os.path.exists(CHROME_PATH):
        print("!!! 错误：找不到 Chrome，请修改代码中的路径。")
        return

    # 直接调用系统命令打开网址
    try:
        # subprocess.Popen([CHROME_PATH, TARGET_URL])
        cmd = f'"{CHROME_PATH}" --user-data-dir="{USER_DATA_DIR}" --no-first-run --no-default-browser-check'
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print(f"启动失败: {e}")
        return

    print("\n" + "=" * 50)
    print("【重要提示】浏览器已启动！")
    print("1. 请等待网页加载完成。")
    print("2. 如果有 Cloudflare 验证，请手动点击通过。")
    print("3. 请鼠标【单击一下】网页上的【邮箱输入框】，确保光标在里面闪烁。")
    print("=" * 50 + "\n")

    # 3. 关键交互：等待用户确认光标位置
    # 因为我们没有 Selenium 定位元素，必须靠人点第一下
    input(">>> 准备好后，请务必先点击邮箱框，然后【按回车键】开始自动填表...")

    print(">>> 3秒后开始输入，请不要移动鼠标...")
    time.sleep(3)

    # ================= 物理填表流程 =================

    # 1. 输入邮箱 (假设光标已经在邮箱框里)
    print(f">>> 正在输入邮箱: {REGISTER_DATA['email']}")
    type_text(REGISTER_DATA['email'])

    # 2. 处理验证码
    # 根据网页布局，通常是：邮箱 -> [Tab] -> 验证码框 -> [Tab] -> 发送按钮
    # 我们按 Tab 键切换焦点

    print(">>> 切换到验证码区域...")
    pyautogui.press('tab')  # 切换焦点到验证码输入框
    time.sleep(0.5)

    if not REGISTER_DATA['verify_code']:
        # 如果没有验证码，通常需要点发送按钮
        # 假设布局：验证码框 -> (Tab) -> 发送按钮
        pyautogui.press('tab')
        time.sleep(0.5)
        print(">>> 尝试按下回车触发发送验证码...")
        pyautogui.press('enter')  # 在按钮上按回车通常等于点击

        print(">>> (已尝试点击发送，请稍后去邮箱查看)")
        # 发送完后，光标可能在按钮上，我们需要回到验证码框或者继续往下
        # 这里假设用户可能需要手动填验证码，我们暂停一下
        print(">>> !!! 脚本暂停 15 秒，请手动填入验证码，并点击一下【密码框】!!!")
        time.sleep(15)
        print(">>> 继续执行...")
    else:
        # 如果有验证码，直接填
        print(f">>> 输入验证码: {REGISTER_DATA['verify_code']}")
        type_text(REGISTER_DATA['verify_code'])
        # 填完验证码，按 Tab 进入发送按钮，再按 Tab 进入密码框
        pyautogui.press('tab')
        time.sleep(0.2)
        pyautogui.press('tab')

        # 3. 输入密码
    # 此时假设焦点在密码框 (或者用户刚才手动点了密码框)
    # 为了保险，我们建议用户在上面的 15秒等待期 手动点一下密码框
    print(">>> 输入密码...")
    type_text(REGISTER_DATA['password'])

    # 4. 确认密码 (如果有第二个密码框)
    # V2board 通常有两个密码框，或者是 密码 -> 邀请码
    # 我们尝试按 Tab 填入下一个框，如果是确认密码就填密码，是邀请码就填邀请码
    print(">>> 尝试填入下一个框 (确认密码/邀请码)...")
    pyautogui.press('tab')
    time.sleep(0.5)

    # 这里比较玄学，我们把密码和邀请码都尝试填一下
    # 如果是确认密码框，填密码没问题
    type_text(REGISTER_DATA['password'])

    # 5. 邀请码
    if REGISTER_DATA['invite_code']:
        print(">>> 尝试填入邀请码...")
        pyautogui.press('tab')
        time.sleep(0.5)
        type_text(REGISTER_DATA['invite_code'])

    print("\n>>> 脚本操作结束！")
    print(">>> 这是一个纯物理外挂脚本，网站无法检测。")
    print(">>> 请检查填写内容，并手动点击【注册/创建账户】按钮。")


if __name__ == "__main__":
    run_pure_automation()