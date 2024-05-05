import time
import random
from pprint import pprint

import cv2
import execjs
import numpy as np
import requests
import json
import os
import sys
sys.path.append('')

from PIL import Image


url1 = "https://www.geetest.com/demo/gt/register-slide"
url2 = "https://apiv6.geetest.com/gettype.php"
url22 = "https://api.geetest.com/gettype.php"
url3 = "https://apiv6.geetest.com/get.php"
url4 = "https://api.geetest.com/ajax.php"
url44 = "https://api.geevisit.com/ajax.php"
url5 = "https://api.geetest.com/get.php"
url55 = "https://api.geevisit.com/get.php"

# 生成一个时间戳
temp_time = int(time.time() * 100)

# 设置一个请求头
head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.44',
}
# 轨迹大全
slide_track = [
    [
        -26,
        -40,
        0
    ],
    [
        0,
        0,
        0
    ],
    [
        1,
        0,
        144
    ],
    [
        2,
        0,
        304
    ],
    [
        3,
        0,
        558
    ],
    [
        4,
        0,
        576
    ],
    [
        5,
        0,
        596
    ],
    [
        6,
        0,
        600
    ],
    [
        7,
        0,
        620
    ],
    [
        8,
        0,
        643
    ],
    [
        9,
        0,
        666
    ],
    [
        10,
        0,
        676
    ],
    [
        11,
        -1,
        696
    ],
    [
        12,
        -1,
        706
    ],
    [
        13,
        -1,
        733
    ],
    [
        14,
        -1,
        736
    ],
    [
        15,
        -1,
        758
    ],
    [
        16,
        -1,
        784
    ],
    [
        17,
        -1,
        806
    ],
    [
        17,
        -2,
        812
    ],
    [
        18,
        -2,
        828
    ],
    [
        19,
        -2,
        858
    ],
    [
        20,
        -2,
        886
    ],
    [
        21,
        -2,
        908
    ],
    [
        22,
        -2,
        924
    ],
    [
        23,
        -2,
        938
    ],
    [
        24,
        -2,
        964
    ],
    [
        25,
        -2,
        992
    ],
    [
        26,
        -2,
        1012
    ],
    [
        27,
        -2,
        1025
    ],
    [
        27,
        -3,
        1036
    ],
    [
        28,
        -3,
        1041
    ],
    [
        29,
        -3,
        1054
    ],
    [
        30,
        -3,
        1149
    ],
    [
        31,
        -3,
        1152
    ],
    [
        32,
        -3,
        1176
    ],
    [
        33,
        -3,
        1198
    ],
    [
        34,
        -3,
        1228
    ],
    [
        35,
        -3,
        1244
    ],
    [
        36,
        -3,
        1258
    ],
    [
        37,
        -3,
        1270
    ],
    [
        38,
        -3,
        1284
    ],
    [
        39,
        -3,
        1288
    ],
    [
        40,
        -3,
        1306
    ],
    [
        41,
        -3,
        1338
    ],
    [
        42,
        -3,
        1358
    ],
    [
        43,
        -3,
        1368
    ],
    [
        44,
        -3,
        1390
    ],
    [
        45,
        -3,
        1402
    ],
    [
        46,
        -3,
        1416
    ],
    [
        47,
        -3,
        1424
    ],
    [
        48,
        -3,
        1440
    ],
    [
        49,
        -3,
        1483
    ],
    [
        50,
        -3,
        1526
    ],
    [
        51,
        -3,
        1544
    ],
    [
        52,
        -3,
        1560
    ],
    [
        53,
        -3,
        1578
    ],
    [
        54,
        -3,
        1601
    ],
    [
        55,
        -3,
        1632
    ],
    [
        56,
        -3,
        1640
    ],
    [
        57,
        -3,
        1662
    ],
    [
        58,
        -3,
        1672
    ],
    [
        59,
        -3,
        1684
    ],
    [
        60,
        -3,
        1694
    ],
    [
        61,
        -3,
        1704
    ],
    [
        62,
        -3,
        1714
    ],
    [
        63,
        -3,
        1733
    ],
    [
        64,
        -3,
        1734
    ],
    [
        65,
        -3,
        1750
    ],
    [
        66,
        -3,
        1772
    ],
    [
        67,
        -3,
        1784
    ],
    [
        68,
        -3,
        1798
    ],
    [
        69,
        -3,
        1812
    ],
    [
        69,
        -2,
        1832
    ],
    [
        70,
        -2,
        1837
    ],
    [
        71,
        -2,
        1852
    ],
    [
        72,
        -2,
        1860
    ],
    [
        73,
        -2,
        1874
    ],
    [
        74,
        -2,
        1894
    ],
    [
        75,
        -2,
        1922
    ],
    [
        76,
        -2,
        1950
    ],
    [
        77,
        -2,
        1972
    ],
    [
        78,
        -2,
        1998
    ],
    [
        79,
        -2,
        2048
    ],
    [
        80,
        -2,
        2079
    ],
    [
        81,
        -2,
        2096
    ],
    [
        82,
        -2,
        2112
    ],
    [
        83,
        -2,
        2126
    ],
    [
        84,
        -2,
        2128
    ],
    [
        84,
        -1,
        2138
    ],
    [
        85,
        -1,
        2150
    ],
    [
        86,
        -1,
        2170
    ],
    [
        87,
        -1,
        2185
    ],
    [
        88,
        -1,
        2204
    ],
    [
        89,
        -1,
        2212
    ],
    [
        90,
        -1,
        2224
    ],
    [
        91,
        -1,
        2244
    ],
    [
        92,
        -1,
        2267
    ],
    [
        93,
        -1,
        2339
    ],
    [
        94,
        -1,
        2354
    ],
    [
        95,
        -1,
        2368
    ],
    [
        96,
        -1,
        2382
    ],
    [
        97,
        -1,
        2392
    ],
    [
        98,
        -1,
        2428
    ],
    [
        99,
        -1,
        2464
    ],
    [
        100,
        -1,
        2490
    ],
    [
        101,
        -1,
        2500
    ],
    [
        102,
        -1,
        2518
    ],
    [
        103,
        -1,
        2534
    ],
    [
        104,
        -1,
        2580
    ],
    [
        105,
        -1,
        2602
    ],
    [
        106,
        -1,
        2624
    ],
    [
        107,
        -1,
        2715
    ],
    [
        108,
        -1,
        2730
    ],
    [
        109,
        -1,
        2740
    ],
    [
        110,
        -1,
        2769
    ],
    [
        111,
        -1,
        2832
    ],
    [
        112,
        -1,
        2975
    ],
    [
        113,
        -1,
        3506
    ],
    [
        114,
        -1,
        3542
    ],
    [
        115,
        -1,
        3834
    ],
    [
        116,
        -1,
        3860
    ],
    [
        117,
        -1,
        3868
    ],
    [
        117,
        0,
        3896
    ],
    [
        118,
        0,
        3910
    ],
    [
        119,
        0,
        4110
    ],
    [
        120,
        0,
        4124
    ],
    [
        121,
        0,
        4138
    ],
    [
        122,
        0,
        4146
    ],
    [
        123,
        0,
        4160
    ],
    [
        124,
        0,
        4200
    ],
    [
        125,
        0,
        4239
    ],
    [
        126,
        0,
        4248
    ],
    [
        127,
        0,
        4264
    ],
    [
        128,
        0,
        4278
    ],
    [
        129,
        0,
        4416
    ],
    [
        130,
        0,
        4631
    ],
    [
        131,
        0,
        4640
    ],
    [
        132,
        0,
        4661
    ],
    [
        133,
        0,
        4672
    ],
    [
        134,
        0,
        4676
    ],
    [
        135,
        0,
        4698
    ],
    [
        136,
        0,
        4716
    ],
    [
        137,
        0,
        4752
    ],
    [
        138,
        0,
        4764
    ],
    [
        139,
        0,
        4786
    ],
    [
        140,
        0,
        4809
    ],
    [
        141,
        0,
        4922
    ],
    [
        142,
        0,
        4947
    ],
    [
        143,
        0,
        4972
    ],
    [
        144,
        0,
        4990
    ],
    [
        145,
        0,
        5238
    ],
    [
        146,
        0,
        5248
    ],
    [
        147,
        0,
        5268
    ],
    [
        148,
        0,
        5289
    ],
    [
        149,
        0,
        5418
    ],
    [
        150,
        0,
        5441
    ],
    [
        151,
        0,
        5452
    ],
    [
        152,
        0,
        5469
    ],
    [
        153,
        0,
        5484
    ],
    [
        154,
        0,
        5532
    ],
    [
        155,
        0,
        5548
    ],
    [
        156,
        0,
        5570
    ],
    [
        157,
        0,
        5733
    ],
    [
        158,
        0,
        5892
    ],
    [
        159,
        0,
        5896
    ],
    [
        160,
        0,
        5928
    ],
    [
        161,
        0,
        6338
    ],
    [
        162,
        0,
        6360
    ],
    [
        163,
        0,
        6434
    ],
    [
        164,
        0,
        6464
    ],
    [
        165,
        0,
        6494
    ],
    [
        166,
        0,
        6946
    ],
    [
        167,
        0,
        6950
    ],
    [
        167,
        1,
        6964
    ],
    [
        168,
        1,
        6970
    ],
    [
        169,
        1,
        7173
    ],
    [
        170,
        1,
        7188
    ],
    [
        171,
        1,
        7197
    ],
    [
        172,
        1,
        7216
    ],
    [
        173,
        1,
        7403
    ],
    [
        174,
        1,
        8030
    ],
    [
        175,
        1,
        8032
    ],
    [
        176,
        1,
        8049
    ],
    [
        177,
        1,
        8060
    ],
    [
        178,
        1,
        8169
    ],
    [
        179,
        1,
        8200
    ],
    [
        180,
        1,
        8292
    ],
    [
        181,
        1,
        8309
    ],
    [
        182,
        1,
        8334
    ],
    [
        183,
        1,
        8637
    ],
    [
        184,
        1,
        8646
    ],
    [
        185,
        1,
        8748
    ],
    [
        186,
        1,
        8920
    ],
    [
        187,
        1,
        8944
    ],
    [
        188,
        1,
        8972
    ],
    [
        189,
        1,
        9062
    ],
    [
        190,
        1,
        9123
    ],
    [
        191,
        1,
        9202
    ],
    [
        192,
        1,
        9331
    ],
    [
        193,
        1,
        9350
    ],
    [
        194,
        1,
        9372
    ],
    [
        195,
        1,
        9390
    ],
    [
        196,
        1,
        9419
    ],
    [
        197,
        1,
        9658
    ],
    [
        198,
        1,
        9716
    ],
    [
        199,
        1,
        9755
    ],
    [
        199,
        2,
        9759
    ],
    [
        200,
        2,
        9764
    ],
    [
        200,
        2,
        9765
    ]
]

def get_js_object(js_file_path):
    """获取js可执行对象"""
    with open(js_file_path, encoding='GBK') as f:
        js_file = f.read()
        return execjs.compile(js_file)

# js path
get_geetest_w_js_path = './js/get_geetest_w.js'
get_geetest_w_js = get_js_object(get_geetest_w_js_path)

# 第一此请求，获取gt 和 challenge
def step1():
    parm = {
        "t":int(time.time() * 100)
    }
    response = requests.get(url1,params=parm,headers=head)
    return response.text

# 第一此请求，获取gt 和 challenge
def step1_for_proxyweb(url):
    values_map = {}
    content = requests.get(url,headers=head).text
    gt_index = content.find('gt: "')
    if gt_index != -1:
        gt_start = gt_index + len('gt: "')
        gt_end = content.find('"', gt_start)
        gt_value = content[gt_start:gt_end]
        values_map["gt"] = gt_value


    challenge_index = content.find('challenge: "')
    if challenge_index != -1:
        challenge_start = challenge_index + len('challenge: "')
        challenge_end = content.find('"', challenge_start)
        challenge_value = content[challenge_start:challenge_end]
        values_map["challenge"] = challenge_value
    pprint("第一步请求{}网址，获得的参数为：{}".format(url,str(values_map)))
    return values_map

# 根据第一个请求的返回值GT请求第二个链接(请求没啥用)
def  step2(gt):
    parm = {
        "gt":gt,
        "callback":"geetest_"+str(int(time.time() * 100))
    }
    response = requests.get(url22,params=parm,headers=head)
    pprint("第二步请求{}网址，获得的响应为：{}".format(url22, response.text))
    return response.text

# 根据第一个请求的返回值GT和challenge请求第三个链接拿到 C 和 S
def step3(gt,challenge):
    parm = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt": 0,
        "client_type": "web",
        "w": "lg(yu(Df9nh3BXUPmZIbJa7XLmxbtVYGvU2mh0jatg(OKv(O2QucayKgi0yQi4SgT(sjfFlvjUVSD(PGdbGnyUBfxOIqSwLofMdsSVxox8CqBcqy9c9RWpAf5WXQeSOaYAX5Ut)YEgTMUE9ialzHbWaadyiGdbO)SU4SIgNXsTRaJ9s8kVHmxqSLC03PPxTgzdX0PGdCBnU8qfFCz8dItkxcv6ei6X)o(FbYw55h1IY4IYjUXGoJthSqoZVTwQiCOx0EVebmFQpJpEHe1PzW9XU2zvvwExTj0zro8kNCGeCX2YU0dOIc4dke8icf2M6nrpGb62gQ5Vug5A2TjCu7jmf6o0slBTfFoEOvdyYx)C1uDSXJdGIGd3t6U4enqyGSYXx7Q0em9yP2qYOpaQKey6A)6K81KiR7(k)oceKdFzDc9BPORqRt6gZXwCauD2vDSMa4fSmDkiVINqCLVZ9bLNAIBpLDiGBeh1QW((3gfZvkfjm8cmlOZ(Dx(OmEpe7Ea36T3OfCS1E9g5gKOuAnPWwXHvAbWj7wpvxeOBUdSE2Dnp)W(OnzoxSpYkXHxFDawJ8MX9ZdGIPZcfNH1OBc5CEfyxtWL92zL(1Xc6htUhfoCFhgpRmQ0i(9aYivQHGY7T((io2v8Xj3QD95VcZgu3UZwDgplET)9RrBtsIkm41(WuQYuw8d8tzD7zvuJu4Tipj3FITH1vFeHNvcIXj8lzteFoFLv)75yA2S7svQKeQXM(wKwqMxnYTnQyTCwbb39Il7Um(FEAG88M9j8M5DESqKDCEvaJf27vzwybY(I0xDzu0f43TyhgYX(Qd5GTPA8HVyXRBRI7DRmgUyP8M3xFN3jCUHr0mza11sJjuhkq66YTJ3onecnfJvd1gG5D9lv2RlmXtZjWzJ0v(ArdGy4iJQaV6Pgd2s(pyKb107Az7BoaVV2OoHDap0APQOFGgwgX7wgfsvRipxdmVHVVO7pgMCGFmrX1HlQ9dokcYuPqWcxmKF71XKUMNnsA4JY4wq1aBemMoxWBgEJOIcqrQa7EbJpHhXTruZJpOiO5AET)5vzpRRETelSonFjyeP5fvwL6Z1(4YNdoZt63(WMzToBmOwGlLL)9uV(XpdBYYpU(LApkhW2pMnQ(LVIAiXlIiv6d25d7436f7b7800db0d1a91490aa02792fb1110994570a6d3b9316ceda7834204c0b6ba459d93179575eb50c0d555c0c812b7ce342b0ecb8d24568e360fd2f70e49c8203dcc31c7ec6eb03eca64790a38395ae0162e398ee8d223c2da52a5d1194d3090985324b47170712e10f12810d5967527f0f47fc996fb3a1575196aee",
        "callback": "geetest_" + str(int(time.time() * 100))
    }
    response = requests.get(url5,params=parm,headers=head)
    pprint("第三步请求{}网址，获得的响应为：{}".format(url5, response.text))
    return response.text

# 根据第一个请求的返回值GT和challenge请求第四个链接，好像也没啥用
def step4(gt,challenge):
    parm = {
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "pt": 0,
        "client_type": "web",
        "w": "",
        "callback": "geetest_" + str(int(time.time() * 100))
    }
    response = requests.get(url44,params=parm,headers=head)
    pprint("第四步请求{}网址，获得的响应为：{}".format(url44, response.text))
    return response.text

# 根据第一个请求的返回值GT和challenge请求第五个链接，拿到图片信息 和 新的challenge（比原先的challenge多2位）
def step5(gt,challenge):
    parm = {
        "is_next": "true",
        "type": "slide3",
        "gt": gt,
        "challenge": challenge,
        "lang": "zh-cn",
        "https": "true",
        "protocol": "https://",
        "offline": "false",
        "product": "embed",
        "api_server": "api.geetest.com",
        "isPC": "true",
        "autoReset": "true",
        "width": "100%",
        "callback": "geetest_" + str(int(time.time() * 100))
    }
    response = requests.get(url55,params=parm,headers=head)
    pprint("第五步请求{}网址，获得的响应为：{}".format(url55, response.text))
    return response.text

# 根据第一个请求的返回值GT和challenge请求第四个链接，好像也没啥用
def step6(gt, challenge, w):
    parm = {
     "gt": gt,
     "challenge": challenge,
     "lang": "zh-cn",
     "$_BCN": 0,
     "client_type": "web",
     "w": w,
     "callback": "geetest_" + str(int(time.time() * 100))
    }
    response = requests.get(url44, params=parm, headers=head)
    pprint("第六步请求{}网址，获得的响应为：{}".format(url55, response.text))
    # print(response.text)
    return response.text

# 下载图片
def download_img_with_url(img_url):
    response = requests.get(img_url)
    create_directory_if_not_exists(os.path.dirname(os.path.abspath(__file__)) + "\\img\\")
    if response.status_code == 200:
        with open(os.path.dirname(os.path.abspath(__file__)) + "\\img\\"+img_url.split("/")[-1], 'wb') as f:
            f.write(response.content)

# 对图片进行还原
def huanyuantupian(img):
    # 还原图片 https://zhuanlan.zhihu.com/p/569492595
    IMG_SHUFFLE_ORDER = [
        39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13,23,22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17,
    ]
    # 图片会被切分为 10x80 的小图
    IMG_SHUFFLE_X_STEP = 10
    IMG_SHUFFLE_Y_STEP = 80

    # 最后图片的宽高
    IMG_WIDTH = 260
    IMG_HEIGHT = 160
    # 创建一个空白图片
    newImg = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT))
    # 获取当前脚本所在目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # 图片文件路径
    image_path = os.path.join(current_directory, "img\\"+img.split("/")[-1])
    # 打开本地图片文件
    image = Image.open(image_path)
    for i in range(len(IMG_SHUFFLE_ORDER)):
        x = IMG_SHUFFLE_ORDER[i] % 26 * 12 + 1
        y = IMG_SHUFFLE_Y_STEP if IMG_SHUFFLE_ORDER[i] > 25 else 0
        # 根据刚才 JS 的逻辑，把图片裁剪出一小块儿
        cut = image.crop((x, y, x + IMG_SHUFFLE_X_STEP, y + IMG_SHUFFLE_Y_STEP))
        # 根据刚才的逻辑，确定新图片的位置
        newX = i % 26 * 10
        newY = IMG_SHUFFLE_Y_STEP if i > 25 else 0
        # 把新图片拼接过去
        newImg.paste(cut, (newX, newY))
        newImg.save(current_directory+"\\img\\new"+img.split("/")[-1])

# 识别图片缺口距离
def shibietupian(img):
    newbgimg = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img\\new" +img.split("/")[-1] ))
    newsliceimg = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img\\" + img.split("/")[-1].replace("jpg","png")))
    grayImg = cv2.cvtColor(np.asarray(newbgimg), cv2.COLOR_BGR2GRAY)
    graySlice  = cv2.cvtColor(np.asarray(newsliceimg), cv2.COLOR_BGR2GRAY)
    # 做边缘检测进一步降低干扰，阈值可以自行调整
    grayImg = cv2.Canny(grayImg, 255, 255)
    # showImg(grayImg) # 可以通过它来看处理后的图片效果
    graySlice = cv2.Canny(graySlice, 255, 255)
    # 通过模板匹配两张图片，找出缺口的位置
    result = cv2.matchTemplate(grayImg, graySlice, cv2.TM_CCOEFF_NORMED)
    maxLoc = cv2.minMaxLoc(result)[3]
    # 匹配出来的滑动距离
    distance = maxLoc[0]
    return distance

# 对返回值进行处理成json对象
def handle_response_to_json(respText):
    start_index = respText.find('(')
    end_index = respText.rfind(')')
    json_data = json.loads(respText[start_index + 1:end_index])
    return json_data


def get_geetest_w_js_call(gt_value,challage_value,c,s,distance,passtime,trace):
    return get_geetest_w_js.call('get_parm_w', gt_value,challage_value,c,s,distance,passtime,trace)

"""
    如果指定的目录不存在，则创建目录。
    参数：
    directory: 要检查和创建的目录路径。
"""
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"目录 '{directory}' 不存在，已自动创建。")
    else:
        print(f"目录 '{directory}' 已存在。")

def delete_files_in_directory(directory = "./img"):
 for root, dirs, files in os.walk(directory):
  for file in files:
   file_path = os.path.join(root, file)
   os.remove(file_path)

# 获取轨迹数组
def find_array_starting_with_number(two_dim_array, target_number):
    result = []
    for array in two_dim_array:
     result.append(array)
     if array[0] == target_number:
      break
    return result

def get_validate(url = "https://www.kakayun.homes"):
    step1Json = step1_for_proxyweb(url + "/auth/register")
    # 根据第一个请求的返回值GT请求第二个链接(请求没啥用) 请求了一些js文件
    step2Response = step2(step1Json["gt"])
    step2Json = handle_response_to_json(step2Response)
    # 根据第一个请求的返回值GT和challenge请求第三个链接拿到 C 和 S，好像也没啥用 s后期也会变
    step3Response = step3(step1Json["gt"], step1Json["challenge"])
    step3Json = handle_response_to_json(step3Response)
    # 根据第一个请求的返回值GT和challenge请求第四个链接，好像也没啥用
    step4Response = step4(step1Json["gt"], step1Json["challenge"])
    step4Json = handle_response_to_json(step4Response)
    # 根据第一个请求的返回值GT和challenge请求第五个链接，拿到图片信息 和 新的challenge（比原先的challenge多2位）
    step5Response = step5(step1Json["gt"], step1Json["challenge"])
    step5Json = handle_response_to_json(step5Response)
    # 获取极验静态地址的前缀，用来拼接下载图片的
    static_servers_prefix_url = "https://" + step3Json["data"]["static_servers"][0] + "/"
    # 下载图片 todo 这里需要优化下载的图片名称不能为乱码
    # print(static_servers_prefix_url + step5Json["bg"])
    download_img_with_url(static_servers_prefix_url + step5Json["bg"])
    download_img_with_url(static_servers_prefix_url + step5Json["slice"])
    # 还原图片
    huanyuantupian(step5Json["bg"])
    # 识别图片距离
    distance = shibietupian(step5Json["bg"])
    # track = get_track(distance)
    # track = get_slide_track(distance)[0]
    track = find_array_starting_with_number(slide_track, distance)
    print("轨迹为" + str(track))
    passtime = track[-1][-1]
    print("使用时间为" + str(track))
    # w = get_slide_w(step5Json["gt"], step5Json["challenge"], step5Json["s"], distance, track)
    # pprint(step5Json)
    w = get_geetest_w_js_call(step5Json["gt"], step5Json["challenge"], step5Json["c"], step5Json["s"], distance,
                              passtime, track)
    print("计算得到的w值为" + w)
    # 根据轨迹暂停几秒钟
    time.sleep(passtime / 1000)
    # 请求获取检验结果
    step6Response = step6(step5Json["gt"], step5Json["challenge"], w)
    step6Json = handle_response_to_json(step6Response)
    if (step6Json['message'] != 'success'):
        print("校验失败，准备重新校验")
        # 如果校验失败重新校验
        get_validate(url)
    delete_files_in_directory()
    validate_value = {}
    validate_value['geetest_challenge'] = step5Json["challenge"]
    validate_value['geetest_validate'] = step6Json['validate']
    validate_value['geetest_seccode'] = step6Json['validate'] + ' | jordan'
    print('校验成功，校验结果为：' + validate_value)
    return validate_value


if __name__ == '__main__':

    # 第一此请求，获取gt 和 challenge
    # step1Json = json.loads(step1())
    # print(step1Json)
    url = "https://www.douluoyun.lol"
    step1Json = step1_for_proxyweb(url+"/auth/register")
    # 根据第一个请求的返回值GT请求第二个链接(请求没啥用) 请求了一些js文件
    step2Response = step2(step1Json["gt"])
    step2Json = handle_response_to_json(step2Response)
    # 根据第一个请求的返回值GT和challenge请求第三个链接拿到 C 和 S，好像也没啥用 s后期也会变
    step3Response = step3(step1Json["gt"], step1Json["challenge"])
    step3Json = handle_response_to_json(step3Response)
    # 根据第一个请求的返回值GT和challenge请求第四个链接，好像也没啥用
    step4Response = step4(step1Json["gt"], step1Json["challenge"])
    step4Json = handle_response_to_json(step4Response)
    # 根据第一个请求的返回值GT和challenge请求第五个链接，拿到图片信息 和 新的challenge（比原先的challenge多2位）
    step5Response = step5(step1Json["gt"], step1Json["challenge"])
    step5Json = handle_response_to_json(step5Response)
    pprint(step5Json)
    # 获取极验静态地址的前缀，用来拼接下载图片的
    static_servers_prefix_url ="https://" + step3Json["data"]["static_servers"][0] + "/"
    # 下载图片 todo 这里需要优化下载的图片名称不能为乱码
    # print(static_servers_prefix_url + step5Json["bg"])
    download_img_with_url(static_servers_prefix_url + step5Json["bg"])
    download_img_with_url(static_servers_prefix_url + step5Json["slice"])
    # 还原图片
    huanyuantupian(step5Json["bg"])
    # 识别图片距离
    distance = shibietupian(step5Json["bg"])
    # track = get_track(distance)
    # track = get_slide_track(distance)[0]
    track = find_array_starting_with_number(slide_track,distance)
    print("轨迹为"+str(track))
    passtime = track[-1][-1]
    pprint(distance)
    pprint(passtime)
    # w = get_slide_w(step5Json["gt"], step5Json["challenge"], step5Json["s"], distance, track)
    # pprint(step5Json)
    w = get_geetest_w_js_call(step5Json["gt"], step5Json["challenge"],  step5Json["c"], step5Json["s"], distance, passtime , track)
    # 根据第一个请求的返回值GT和challenge请求第四个链接
    print(w)
    time.sleep(passtime/1000)
    step6Response = step6(step5Json["gt"], step5Json["challenge"],w)
    step6Json = handle_response_to_json(step6Response)
    if(step6Json['message'] != 'success'):
        print("获取校验失败")
    pprint(step6Json)
    delete_files_in_directory()