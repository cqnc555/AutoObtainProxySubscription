import random

# --- 1. 配置超大词汇库 ---

# 常见的英文名、拼音、昵称前缀 (约 150+)
FIRST_PARTS = [
    # 英文名 (男/女)
    "james", "mary", "robert", "patricia", "john", "jennifer", "michael", "linda",
    "david", "elizabeth", "william", "barbara", "richard", "susan", "joseph", "jessica",
    "thomas", "sarah", "charles", "karen", "christopher", "nancy", "daniel", "lisa",
    "matthew", "betty", "anthony", "margaret", "mark", "sandra", "donald", "ashley",
    "steven", "kimberly", "paul", "emily", "andrew", "donna", "joshua", "michelle",
    "kenneth", "dorothy", "kevin", "carol", "brian", "amanda", "george", "melissa",
    "edward", "deborah", "ronald", "stephanie", "timothy", "rebecca", "jason", "sharon",
    "jeffrey", "laura", "ryan", "cynthia", "jacob", "kathleen", "gary", "amy",
    "nicholas", "shirley", "eric", "angela", "jonathan", "helen", "stephen", "anna",
    "larry", "brenda", "justin", "pamela", "scott", "nicole", "brandon", "emma",
    "benjamin", "samantha", "samuel", "katherine", "gregory", "christine", "alexander",
    "frank", "patrick", "raymond", "jack", "dennis", "jerry", "tyler", "aaron",
    # 常用拼音/形容词
    "happy", "lucky", "sunny", "super", "wonder", "magic", "crazy", "cool",
    "fast", "smart", "brave", "calm", "wild", "free", "sweet", "blue",
    "red", "gold", "silver", "iron", "cyber", "tech", "pro", "master",
    "xiao", "lao", "da", "a", "wei", "fang", "ming", "jie", "hui", "yan"
]

# 常见的姓氏、名词、职业后缀 (约 150+)
SECOND_PARTS = [
    # 英文姓氏
    "smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis",
    "rodriguez", "martinez", "hernandez", "lopez", "gonzalez", "wilson", "anderson",
    "thomas", "taylor", "moore", "jackson", "martin", "lee", "perez", "thompson",
    "white", "harris", "sanchez", "clark", "ramirez", "lewis", "robinson", "walker",
    "young", "allen", "king", "wright", "scott", "torres", "nguyen", "hill",
    "flores", "green", "adams", "nelson", "baker", "hall", "rivera", "campbell",
    # 有趣的名词/代号
    "panda", "tiger", "lion", "cat", "dog", "wolf", "dragon", "eagle", "shark",
    "bear", "fox", "rabbit", "hawk", "falcon", "owl", "whale", "dolphin",
    "star", "moon", "sun", "sky", "cloud", "rain", "storm", "snow", "wind",
    "mountain", "river", "ocean", "forest", "tree", "flower", "leaf", "stone",
    "coder", "gamer", "driver", "rider", "flyer", "runner", "player", "maker",
    "designer", "artist", "writer", "teacher", "doctor", "chef", "pilot",
    "knight", "wizard", "ninja", "samurai", "hero", "king", "queen", "prince",
    "walker", "talker", "singer", "dancer", "dreamer", "hunter", "finder"
]


# --- 2. 核心函数实现 ---

def get_complex_username() -> str:
    """
    生成高随机性、由于组合量巨大而极难重复的用户名。
    """
    # 随机选择两部分
    part1 = random.choice(FIRST_PARTS)
    part2 = random.choice(SECOND_PARTS)

    # 分隔符策略：除了常规的 . 和 _，有些人不加分隔符
    # 权重：不加(40%), .(30%), _(30%)
    sep = random.choices(["", ".", "_"], weights=[40, 30, 30], k=1)[0]
    # 取消中间的分隔符
    # base = f"{part1}{sep}{part2}"
    base = f"{part1}{part2}"

    # 数字后缀策略 (为了保证1000次不重复，数字后缀是关键)
    # 只有 5% 的概率不加数字（模拟那些抢到了纯字母账号的早期用户）
    if random.random() < 0.05:
        return base

    # 生成数字的方式
    num_strategy = random.choice(['year', 'random_2', 'random_3', 'random_4'])

    if num_strategy == 'year':
        # 模拟年份 1980-2025
        suffix = str(random.randint(1980, 2025))
    elif num_strategy == 'random_2':
        # 两位数 01-99
        suffix = f"{random.randint(1, 99):02d}"
    elif num_strategy == 'random_3':
        # 三位数 100-999
        suffix = str(random.randint(100, 999))
    else:
        # 四位数 1000-9999
        suffix = str(random.randint(1000, 9999))

    return f"{base}{suffix}"


def get_random_email() -> str:
    """
    生成完整邮箱，使用加权随机的域名选择（Gmail更常见）。
    """
    domains = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
        "163.com", "qq.com", "icloud.com", "sina.com",
        "live.com", "foxmail.com", "proton.me", "yandex.com"
    ]
    # 权重分配：Gmail/Outlook/QQ/163 概率更高
    weights = [25, 10, 10, 15, 15, 15, 2, 2, 2, 2, 1, 1]

    username = get_complex_username()
    domain = random.choices(domains, weights=weights, k=1)[0]

    return f"{username}@{domain}"


# --- 3. 验证与测试 ---

if __name__ == "__main__":
    # 测试生成 1000 个，检查是否有重复
    count = 1000
    email_set = set()

    print(f"正在生成 {count} 个随机邮箱进行碰撞测试...")

    for i in range(count):
        email = get_random_email()
        email_set.add(email)

        # 打印前10个看看效果
        if i < 10:
            user_part = email.split('@')[0]
            print(f"示例 {i + 1:02d}: {user_part:<25} | {email}")

    print("-" * 50)
    print(f"计划生成: {count}")
    print(f"实际唯一: {len(email_set)}")

    if len(email_set) == count:
        print("✅ 测试通过：1000个结果中无重复项！")
    else:
        print(f"⚠️ 出现重复：重复了 {count - len(email_set)} 个")