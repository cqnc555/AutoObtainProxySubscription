import sys
# 因为是绿色版python 设置当前目录添加到自定义环境变量
# 需要先配置环境变量，否则会提示导入同目录的包不存在
import time

import markdown

sys.path.append('')
import re
import base64
import urllib.parse
import requests
import json
import subprocess
import markdown
import yaml
from bs4 import BeautifulSoup

# 禁用安全请求警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置Chrome的环境变量（也可以直接指定路径）
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
}

def get_proxy_url(url):
    resp = requests.get(url,headers=headers)
    resp = resp.text
    resp = markdown.markdown(resp)
    soup = BeautifulSoup(resp, 'html.parser')
    # 3. 查找目标 div
    snippet_div = soup.find('div', class_='snippet-clipboard-content')
    if snippet_div:
        # 4. 获取 data-snippet-clipboard-copy-content 属性的值
        # clipboard_content = snippet_div.get('data-snippet-clipboard-copy-content')

        # 5. 获取 <code> 中的文本
        code_content = snippet_div.find('code').text.strip()

        # print("Data-snippet-clipboard-copy-content:", clipboard_content)
        print("Code content:", code_content)

        resp = requests.get(code_content, headers=headers)
        return resp.text
    else:
        print("未找到指定的 div.")

def handle_proxy_base64url(base64_str = 'dm1lc3M6Ly9leUp5WlcxaGNtc2lPaUxsaWFua3Zabm10WUhwaDQvdnZKb3hMalE0UjBJaUxDSjBlWEJsSWpwdWRXeHNMQ0poWkdRaU9pSjNkM2N1YTJGcllYbDFiaTVzYjJ3aUxDSndiM0owSWpveE1EQTROaXdpYVdRaU9pSXdPVFF5T0dFNFpTMHdNemM1TFRNME1HTXRZVEEyWXkxbU5XRXpNemcyTlRNME1UQWlMQ0p1WlhRaU9pSjBZM0FpTENKaGFXUWlPakFzSW5Ceklqb2k1WW1wNUwyWjVyV0I2WWVQNzd5YU1TNDBPRWRDSW4wPQp2bWVzczovL2V5SnlaVzFoY21zaU9pTG92NGZtbkovbWw3YnBsN1R2dkpveU1ESTBMVEE1TFRJd0lpd2lkSGx3WlNJNmJuVnNiQ3dpWVdSa0lqb2lkM2QzTG10aGEyRjVkVzR1Ykc5c0lpd2ljRzl5ZENJNk1UQXdPRFlzSW1sa0lqb2lNRGswTWpoaE9HVXRNRE0zT1Mwek5EQmpMV0V3Tm1NdFpqVmhNek00TmpVek5ERXdJaXdpYm1WMElqb2lkR053SWl3aVlXbGtJam93TENKd2N5STZJdWkvaCthY24rYVh0dW1YdE8rOG1qSXdNalF0TURrdE1qQWlmUT09CnZtZXNzOi8vZXlKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlJc0luWmxjbWxtZVY5alpYSjBJanAwY25WbExDSmhaR1FpT2lJekxtdGhhMkY1ZFc0dWFHOXRaWE1pTENKd2IzSjBJam96TURBd015d2lZV2xrSWpveUxDSnVaWFFpT2lKMFkzQWlMQ0pvWldGa1pYSlVlWEJsSWpvaWJtOXVaU0lzSW5ZaU9pSXlJaXdpZEhsd1pTSTZJbTV2Ym1VaUxDSndjeUk2SWx0MmFYQXhYU0Rpa2FBZzU3Nk81WnU5SURFd01EQk43NzJjdzVjeDVZQ041NDZINzcyYzZabVE2WUNmTVRBd1RTSXNJbkpsYldGeWF5STZJbHQyYVhBeFhTRGlrYUFnNTc2TzVadTlJREV3TURCTjc3MmN3NWN4NVlDTjU0Nkg3NzJjNlptUTZZQ2ZNVEF3VFNJc0ltbGtJam9pTURrME1qaGhPR1V0TURNM09TMHpOREJqTFdFd05tTXRaalZoTXpNNE5qVXpOREV3SWl3aVkyeGhjM01pT2pGOQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSTBMbXRoYTJGNWRXNHVhRzl0WlhNaUxDSndiM0owSWpvek1EQXdOQ3dpWVdsa0lqb3lMQ0p1WlhRaU9pSjBZM0FpTENKb1pXRmtaWEpVZVhCbElqb2libTl1WlNJc0luWWlPaUl5SWl3aWRIbHdaU0k2SW01dmJtVWlMQ0p3Y3lJNklsdDJhWEF4WFNEaWthRWc1cGVsNXB5c0lERXdNREJONzcyY3c1Y3g1WUNONTQ2SDc3MmM2Wm1RNllDZk1UQXdUU0lzSW5KbGJXRnlheUk2SWx0MmFYQXhYU0Rpa2FFZzVwZWw1cHlzSURFd01EQk43NzJjdzVjeDVZQ041NDZINzcyYzZabVE2WUNmTVRBd1RTSXNJbWxrSWpvaU1EazBNamhoT0dVdE1ETTNPUzB6TkRCakxXRXdObU10WmpWaE16TTROalV6TkRFd0lpd2lZMnhoYzNNaU9qRjkKdm1lc3M6Ly9leUpvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUlzSW5abGNtbG1lVjlqWlhKMElqcDBjblZsTENKaFpHUWlPaUkxTG10aGEyRjVkVzR1YUc5dFpYTWlMQ0p3YjNKMElqb3pNREF3TlN3aVlXbGtJam95TENKdVpYUWlPaUowWTNBaUxDSm9aV0ZrWlhKVWVYQmxJam9pYm05dVpTSXNJbllpT2lJeUlpd2lkSGx3WlNJNkltNXZibVVpTENKd2N5STZJbHQyYVhBeFhTRGlrYUlnNXBlbDVweXNJREV3TURCTjc3MmN3NWN4NVlDTjU0Nkg3NzJjNlptUTZZQ2ZNVEF3VFNJc0luSmxiV0Z5YXlJNklsdDJhWEF4WFNEaWthSWc1cGVsNXB5c0lERXdNREJONzcyY3c1Y3g1WUNONTQ2SDc3MmM2Wm1RNllDZk1UQXdUU0lzSW1sa0lqb2lNRGswTWpoaE9HVXRNRE0zT1Mwek5EQmpMV0V3Tm1NdFpqVmhNek00TmpVek5ERXdJaXdpWTJ4aGMzTWlPakY5CnZtZXNzOi8vZXlKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlJc0luWmxjbWxtZVY5alpYSjBJanAwY25WbExDSmhaR1FpT2lJMkxtdGhhMkY1ZFc0dWFHOXRaWE1pTENKd2IzSjBJam96TURBd05pd2lZV2xrSWpveUxDSnVaWFFpT2lKMFkzQWlMQ0pvWldGa1pYSlVlWEJsSWpvaWJtOXVaU0lzSW5ZaU9pSXlJaXdpZEhsd1pTSTZJbTV2Ym1VaUxDSndjeUk2SWx0MmFYQXhYU0Rpa2FNZzVwZWw1cHlzSURFd01EQk43NzJjdzVjeDVZQ041NDZINzcyYzZabVE2WUNmTVRBd1RTSXNJbkpsYldGeWF5STZJbHQyYVhBeFhTRGlrYU1nNXBlbDVweXNJREV3TURCTjc3MmN3NWN4NVlDTjU0Nkg3NzJjNlptUTZZQ2ZNVEF3VFNJc0ltbGtJam9pTURrME1qaGhPR1V0TURNM09TMHpOREJqTFdFd05tTXRaalZoTXpNNE5qVXpOREV3SWl3aVkyeGhjM01pT2pGOQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSTNMbXRoYTJGNWRXNHVhRzl0WlhNaUxDSndiM0owSWpvek1EQXdOeXdpWVdsa0lqb3lMQ0p1WlhRaU9pSjBZM0FpTENKb1pXRmtaWEpVZVhCbElqb2libTl1WlNJc0luWWlPaUl5SWl3aWRIbHdaU0k2SW01dmJtVWlMQ0p3Y3lJNklsdDJhWEF4WFNEaWthUWc1cGVsNXB5c0lERXdNREJONzcyY3c1Y3g1WUNONTQ2SDc3MmM2Wm1RNllDZk1UQXdUU0lzSW5KbGJXRnlheUk2SWx0MmFYQXhYU0Rpa2FRZzVwZWw1cHlzSURFd01EQk43NzJjdzVjeDVZQ041NDZINzcyYzZabVE2WUNmTVRBd1RTSXNJbWxrSWpvaU1EazBNamhoT0dVdE1ETTNPUzB6TkRCakxXRXdObU10WmpWaE16TTROalV6TkRFd0lpd2lZMnhoYzNNaU9qRjkKdm1lc3M6Ly9leUpvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUlzSW5abGNtbG1lVjlqWlhKMElqcDBjblZsTENKaFpHUWlPaUk0TG10aGEyRjVkVzR1YUc5dFpYTWlMQ0p3YjNKMElqb3pNREF3T0N3aVlXbGtJam95TENKdVpYUWlPaUowWTNBaUxDSm9aV0ZrWlhKVWVYQmxJam9pYm05dVpTSXNJbllpT2lJeUlpd2lkSGx3WlNJNkltNXZibVVpTENKd2N5STZJbHQyYVhBeFhTRGlrYVVnNXBlbDVweXNJREV3TURCTjc3MmN3NWN4NVlDTjU0Nkg3NzJjNlptUTZZQ2ZNVEF3VFNJc0luSmxiV0Z5YXlJNklsdDJhWEF4WFNEaWthVWc1cGVsNXB5c0lERXdNREJONzcyY3c1Y3g1WUNONTQ2SDc3MmM2Wm1RNllDZk1UQXdUU0lzSW1sa0lqb2lNRGswTWpoaE9HVXRNRE0zT1Mwek5EQmpMV0V3Tm1NdFpqVmhNek00TmpVek5ERXdJaXdpWTJ4aGMzTWlPakY5CnZtZXNzOi8vZXlKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlJc0luWmxjbWxtZVY5alpYSjBJanAwY25WbExDSmhaR1FpT2lJNUxtdGhhMkY1ZFc0dWFHOXRaWE1pTENKd2IzSjBJam96TURBd09Td2lZV2xrSWpveUxDSnVaWFFpT2lKMFkzQWlMQ0pvWldGa1pYSlVlWEJsSWpvaWJtOXVaU0lzSW5ZaU9pSXlJaXdpZEhsd1pTSTZJbTV2Ym1VaUxDSndjeUk2SWx0MmFYQXhYU0Rpa2FZZzVwZWw1cHlzSURFd01EQk43NzJjdzVjeDVZQ041NDZINzcyYzZabVE2WUNmTVRBd1RTSXNJbkpsYldGeWF5STZJbHQyYVhBeFhTRGlrYVlnNXBlbDVweXNJREV3TURCTjc3MmN3NWN4NVlDTjU0Nkg3NzJjNlptUTZZQ2ZNVEF3VFNJc0ltbGtJam9pTURrME1qaGhPR1V0TURNM09TMHpOREJqTFdFd05tTXRaalZoTXpNNE5qVXpOREV3SWl3aVkyeGhjM01pT2pGOQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSXhNQzVyWVd0aGVYVnVMbWh2YldWeklpd2ljRzl5ZENJNk16QXdNVEFzSW1GcFpDSTZNaXdpYm1WMElqb2lkR053SWl3aWFHVmhaR1Z5Vkhsd1pTSTZJbTV2Ym1VaUxDSjJJam9pTWlJc0luUjVjR1VpT2lKdWIyNWxJaXdpY0hNaU9pSmJkbWx3TVYwZzRwR25JQ0RtbHJEbGlxRGxuYUVnTVRBd01FM3Z2WnpEbHpIbGdJM25qb2Z2dlp6cG1aRHBnSjh4TURCTklpd2ljbVZ0WVhKcklqb2lXM1pwY0RGZElPS1JweUFnNXBhdzVZcWc1WjJoSURFd01EQk43NzJjdzVjeDVZQ041NDZINzcyYzZabVE2WUNmTVRBd1RTSXNJbWxrSWpvaU1EazBNamhoT0dVdE1ETTNPUzB6TkRCakxXRXdObU10WmpWaE16TTROalV6TkRFd0lpd2lZMnhoYzNNaU9qRjkKdm1lc3M6Ly9leUpvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUlzSW5abGNtbG1lVjlqWlhKMElqcDBjblZsTENKaFpHUWlPaUl4TVM1cllXdGhlWFZ1TG1odmJXVnpJaXdpY0c5eWRDSTZNekF3TVRFc0ltRnBaQ0k2TWl3aWJtVjBJam9pZEdOd0lpd2lhR1ZoWkdWeVZIbHdaU0k2SW01dmJtVWlMQ0oySWpvaU1pSXNJblI1Y0dVaU9pSnViMjVsSWl3aWNITWlPaUpiZG1sd01WMGc0cEdvSU9hV3NPV0tvT1dkb1NBeE1EQXdUZSs5bk1PWE1lV0FqZWVPaCsrOW5PbVprT21BbnpFd01FMGlMQ0p5WlcxaGNtc2lPaUpiZG1sd01WMGc0cEdvSU9hV3NPV0tvT1dkb1NBeE1EQXdUZSs5bk1PWE1lV0FqZWVPaCsrOW5PbVprT21BbnpFd01FMGlMQ0pwWkNJNklqQTVOREk0WVRobExUQXpOemt0TXpRd1l5MWhNRFpqTFdZMVlUTXpPRFkxTXpReE1DSXNJbU5zWVhOeklqb3hmUT09CnZtZXNzOi8vZXlKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlJc0luWmxjbWxtZVY5alpYSjBJanAwY25WbExDSmhaR1FpT2lJeE5DNXJZV3RoZVhWdUxtaHZiV1Z6SWl3aWNHOXlkQ0k2TXpBd01UUXNJbUZwWkNJNk1pd2libVYwSWpvaWRHTndJaXdpYUdWaFpHVnlWSGx3WlNJNkltNXZibVVpTENKMklqb2lNaUlzSW5SNWNHVWlPaUp1YjI1bElpd2ljSE1pT2lKYmRtbHdNVjBnNHBHcklPYVdzT1dLb09XZG9TQXhNREF3VGUrOW5NT1hNZVdBamVlT2grKzluT21aa09tQW56RXdNRTBpTENKeVpXMWhjbXNpT2lKYmRtbHdNVjBnNHBHcklPYVdzT1dLb09XZG9TQXhNREF3VGUrOW5NT1hNZVdBamVlT2grKzluT21aa09tQW56RXdNRTBpTENKcFpDSTZJakE1TkRJNFlUaGxMVEF6TnprdE16UXdZeTFoTURaakxXWTFZVE16T0RZMU16UXhNQ0lzSW1Oc1lYTnpJam94ZlE9PQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSXhOUzVyWVd0aGVYVnVMbWh2YldWeklpd2ljRzl5ZENJNk16QXdNVFVzSW1GcFpDSTZNaXdpYm1WMElqb2lkR053SWl3aWFHVmhaR1Z5Vkhsd1pTSTZJbTV2Ym1VaUxDSjJJam9pTWlJc0luUjVjR1VpT2lKdWIyNWxJaXdpY0hNaU9pSmJkbWx3TVYwZzRwR3NJT2FXc09XS29PV2RvVEV3TURCTjc3MmN3NWN4NVlDTjU0Nkg3NzJjNlptUTZZQ2ZNVEF3VFNJc0luSmxiV0Z5YXlJNklsdDJhWEF4WFNEaWthd2c1cGF3NVlxZzVaMmhNVEF3TUUzdnZaekRsekhsZ0kzbmpvZnZ2WnpwbVpEcGdKOHhNREJOSWl3aWFXUWlPaUl3T1RReU9HRTRaUzB3TXpjNUxUTTBNR010WVRBMll5MW1OV0V6TXpnMk5UTTBNVEFpTENKamJHRnpjeUk2TVgwPQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSXhOaTVyWVd0aGVYVnVMbWh2YldWeklpd2ljRzl5ZENJNk16QXdNVFlzSW1GcFpDSTZNaXdpYm1WMElqb2lkR053SWl3aWFHVmhaR1Z5Vkhsd1pTSTZJbTV2Ym1VaUxDSjJJam9pTWlJc0luUjVjR1VpT2lKdWIyNWxJaXdpY0hNaU9pSmJkbWx3TVYwZzRwR3RJT2FXc09XS29PV2RvU0F4TURBd1RlKzluTU9YTWVXQWplZU9oKys5bk9tWmtPbUFuekV3TUUwaUxDSnlaVzFoY21zaU9pSmJkbWx3TVYwZzRwR3RJT2FXc09XS29PV2RvU0F4TURBd1RlKzluTU9YTWVXQWplZU9oKys5bk9tWmtPbUFuekV3TUUwaUxDSnBaQ0k2SWpBNU5ESTRZVGhsTFRBek56a3RNelF3WXkxaE1EWmpMV1kxWVRNek9EWTFNelF4TUNJc0ltTnNZWE56SWpveGZRPT0Kdm1lc3M6Ly9leUpvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUlzSW5abGNtbG1lVjlqWlhKMElqcDBjblZsTENKaFpHUWlPaUl4Tnk1cllXdGhlWFZ1TG1odmJXVnpJaXdpY0c5eWRDSTZNekF3TVRjc0ltRnBaQ0k2TWl3aWJtVjBJam9pZEdOd0lpd2lhR1ZoWkdWeVZIbHdaU0k2SW01dmJtVWlMQ0oySWpvaU1pSXNJblI1Y0dVaU9pSnViMjVsSWl3aWNITWlPaUpiZG1sd01WMGc0cEd1SU9lK2p1V2J2U0F4TURBd1RlKzluTU9YTWVXQWplZU9oKys5bk9tWmtPbUFuekV3TUUwaUxDSnlaVzFoY21zaU9pSmJkbWx3TVYwZzRwR3VJT2UranVXYnZTQXhNREF3VGUrOW5NT1hNZVdBamVlT2grKzluT21aa09tQW56RXdNRTBpTENKcFpDSTZJakE1TkRJNFlUaGxMVEF6TnprdE16UXdZeTFoTURaakxXWTFZVE16T0RZMU16UXhNQ0lzSW1Oc1lYTnpJam94ZlE9PQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSXhPQzVyWVd0aGVYVnVMbWh2YldWeklpd2ljRzl5ZENJNk16QXdNVGdzSW1GcFpDSTZNaXdpYm1WMElqb2lkR053SWl3aWFHVmhaR1Z5Vkhsd1pTSTZJbTV2Ym1VaUxDSjJJam9pTWlJc0luUjVjR1VpT2lKdWIyNWxJaXdpY0hNaU9pSmJkbWx3TVYwZzRwR3ZJT2UranVXYnZTQXhNREF3VGUrOW5NT1hNZVdBamVlT2grKzluT21aa09tQW56RXdNRTBpTENKeVpXMWhjbXNpT2lKYmRtbHdNVjBnNHBHdklPZStqdVdidlNBeE1EQXdUZSs5bk1PWE1lV0FqZWVPaCsrOW5PbVprT21BbnpFd01FMGlMQ0pwWkNJNklqQTVOREk0WVRobExUQXpOemt0TXpRd1l5MWhNRFpqTFdZMVlUTXpPRFkxTXpReE1DSXNJbU5zWVhOeklqb3hmUT09CnZtZXNzOi8vZXlKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlJc0luWmxjbWxtZVY5alpYSjBJanAwY25WbExDSmhaR1FpT2lJeE9TNXJZV3RoZVhWdUxtaHZiV1Z6SWl3aWNHOXlkQ0k2TXpBd01Ua3NJbUZwWkNJNk1pd2libVYwSWpvaWRHTndJaXdpYUdWaFpHVnlWSGx3WlNJNkltNXZibVVpTENKMklqb2lNaUlzSW5SNWNHVWlPaUp1YjI1bElpd2ljSE1pT2lKYmRtbHdNVjBnNHBHd0lPZStqdVdidlNBeE1EQXdUZSs5bk1PWE1lV0FqZWVPaCsrOW5PbVprT21BbnpFd01FMGlMQ0p5WlcxaGNtc2lPaUpiZG1sd01WMGc0cEd3SU9lK2p1V2J2U0F4TURBd1RlKzluTU9YTWVXQWplZU9oKys5bk9tWmtPbUFuekV3TUUwaUxDSnBaQ0k2SWpBNU5ESTRZVGhsTFRBek56a3RNelF3WXkxaE1EWmpMV1kxWVRNek9EWTFNelF4TUNJc0ltTnNZWE56SWpveGZRPT0Kdm1lc3M6Ly9leUpvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUlzSW5abGNtbG1lVjlqWlhKMElqcDBjblZsTENKaFpHUWlPaUl5TUM1cllXdGhlWFZ1TG1odmJXVnpJaXdpY0c5eWRDSTZNekF3TWpBc0ltRnBaQ0k2TWl3aWJtVjBJam9pZEdOd0lpd2lhR1ZoWkdWeVZIbHdaU0k2SW01dmJtVWlMQ0oySWpvaU1pSXNJblI1Y0dVaU9pSnViMjVsSWl3aWNITWlPaUpiZG1sd01WMGc0cEd4SU9tZnFlV2J2U0F4TURBd1RlKzluTU9YTWVXQWplZU9oKys5bk9tWmtPbUFuekV3TUUwaUxDSnlaVzFoY21zaU9pSmJkbWx3TVYwZzRwR3hJT21mcWVXYnZTQXhNREF3VGUrOW5NT1hNZVdBamVlT2grKzluT21aa09tQW56RXdNRTBpTENKcFpDSTZJakE1TkRJNFlUaGxMVEF6TnprdE16UXdZeTFoTURaakxXWTFZVE16T0RZMU16UXhNQ0lzSW1Oc1lYTnpJam94ZlE9PQp2bWVzczovL2V5Sm9iM04wSWpvaUlpd2ljR0YwYUNJNklpSXNJblJzY3lJNklpSXNJblpsY21sbWVWOWpaWEowSWpwMGNuVmxMQ0poWkdRaU9pSXlNUzVyWVd0aGVYVnVMbWh2YldWeklpd2ljRzl5ZENJNk16QXdNakVzSW1GcFpDSTZNaXdpYm1WMElqb2lkR053SWl3aWFHVmhaR1Z5Vkhsd1pTSTZJbTV2Ym1VaUxDSjJJam9pTWlJc0luUjVjR1VpT2lKdWIyNWxJaXdpY0hNaU9pSmJkbWx3TVYwZzRwR3lJT21mcWVXYnZTQXhNREF3VGUrOW5NT1hNZVdBamVlT2grKzluT21aa09tQW56RXdNRTBpTENKeVpXMWhjbXNpT2lKYmRtbHdNVjBnNHBHeUlPbWZxZVdidlNBeE1EQXdUZSs5bk1PWE1lV0FqZWVPaCsrOW5PbVprT21BbnpFd01FMGlMQ0pwWkNJNklqQTVOREk0WVRobExUQXpOemt0TXpRd1l5MWhNRFpqTFdZMVlUTXpPRFkxTXpReE1DSXNJbU5zWVhOeklqb3hmUT09CnZtZXNzOi8vZXlKb2IzTjBJam9pSWl3aWNHRjBhQ0k2SWlJc0luUnNjeUk2SWlJc0luWmxjbWxtZVY5alpYSjBJanAwY25WbExDSmhaR1FpT2lJeU1pNXJZV3RoZVhWdUxtaHZiV1Z6SWl3aWNHOXlkQ0k2TXpBd01qSXNJbUZwWkNJNk1pd2libVYwSWpvaWRHTndJaXdpYUdWaFpHVnlWSGx3WlNJNkltNXZibVVpTENKMklqb2lNaUlzSW5SNWNHVWlPaUp1YjI1bElpd2ljSE1pT2lKYmRtbHdNVjBnNHBHeklPbW1tZWE0cnlBeE1EQXdUZSs5bk1PWE1lV0FqZWVPaCsrOW5PbVprT21BbnpFd01FMGlMQ0p5WlcxaGNtc2lPaUpiZG1sd01WMGc0cEd6SU9tbW1lYTRyeUF4TURBd1RlKzluTU9YTWVXQWplZU9oKys5bk9tWmtPbUFuekV3TUUwaUxDSnBaQ0k2SWpBNU5ESTRZVGhsTFRBek56a3RNelF3WXkxaE1EWmpMV1kxWVRNek9EWTFNelF4TUNJc0ltTnNZWE56SWpveGZRPT0Kdm1lc3M6Ly9leUpvYjNOMElqb2lJaXdpY0dGMGFDSTZJaUlzSW5Sc2N5STZJaUlzSW5abGNtbG1lVjlqWlhKMElqcDBjblZsTENKaFpHUWlPaUl4TWk1cllXdGhlWFZ1TG1odmJXVnpJaXdpY0c5eWRDSTZNekF3TVRJc0ltRnBaQ0k2TWl3aWJtVjBJam9pZEdOd0lpd2lhR1ZoWkdWeVZIbHdaU0k2SW01dmJtVWlMQ0oySWpvaU1pSXNJblI1Y0dVaU9pSnViMjVsSWl3aWNITWlPaUxscElmbmxLamxuNS9sa0kwZ1hIUjNkM2N1YTJGcllYbDFiaTVoY25RaUxDSnlaVzFoY21zaU9pTGxwSWZubEtqbG41L2xrSTBnWEhSM2QzY3VhMkZyWVhsMWJpNWhjblFpTENKcFpDSTZJakE1TkRJNFlUaGxMVEF6TnprdE16UXdZeTFoTURaakxXWTFZVE16T0RZMU16UXhNQ0lzSW1Oc1lYTnpJam93ZlE9PQo='):
    base64_str2 = base64.b64decode(base64_str)
    base64_str3 = base64_str2.decode('UTF-8')
    base64_str3_list = base64_str3.split('\n')
    # print(base64_str3_list)
    return base64_str3_list

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

# def handle_proxy_list(proxy_list):
#     new_proxy_list = []
#     for proxy_str in proxy_list:
#         proxy_dict = {}
#         proxy_dict['d_pass_word'] = proxy_str['password']
#         proxy_dict['d_url'] = proxy_str['server']
#         proxy_dict['d_prot'] = proxy_str['port']
#         proxy_dict['d_note'] = proxy_str['name']
#         new_proxy_list.append(proxy_dict)
#     return new_proxy_list

def close_v2ray():
    try:
        # 替换成实际关闭V2RayN的命令，这里假设使用taskkill命令
        # taskkill是Windows上用于终止进程的命令
        # /IM参数指定要终止的进程名，这里假设V2RayN的进程名为v2rayN.exe
        subprocess.run(['taskkill', '/IM', 'v2rayN.exe', '/F'])
        time.sleep(5)
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
    print(new_proxy_list2)
    f = open(path+"guiNConfig.json", 'w', encoding='UTF-8')
    # 字典转为字符串
    jsonobj = json.dumps(data)
    f.write(jsonobj)
    f.close()
    start_v2ray(path)
    pass


if __name__ == '__main__':
    # url = 'https://github.com/abshare/abshare.github.io'
    url = 'https://g.nite07.org/mksshare/mksshare.github.io/blob/main/README.md'
    # url = 'https://freemc.mcsslk.xyz/Jjk3lTM'
    # url = 'https://abshare.github.io/'
    # path = 'E:\\v2rayN-Core\\'
    path = 'F:\\FQ\\v2rayN\\'
    proxy_base64 = get_proxy_url(url)
    base_proxy_list = handle_proxy_base64url(proxy_base64)
    new_proxy_list = handle_proxy_list(base_proxy_list)
    # print(new_proxy_list)

    # ran_str = register_web(url,validate)
    # cookies = login_web(url, ran_str)
    # checkin_web(url, cookies)
    # v2ray_url = get_v2ray_url(url, cookies)
    write_config_file(path, new_proxy_list)
    # get_v2ray_suburl(v2ray_url)
    # print('程序执行完毕，15S后自动结束本程序。')
    # time.sleep(15)