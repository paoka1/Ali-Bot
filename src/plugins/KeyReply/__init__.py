# 主要是关键字回复，有一些依据时间做判断的功能

from nonebot import on_keyword
import random
import time

# 注册事件响应器 kaibai 关键字回复，优先级为 5
kaibai = on_keyword({'摆烂', '摆大烂', '开摆'}, priority=5)


@kaibai.handle()
# 触发了就回复
async def kaibai_reply_handle():
    reply_msg = "_(:з」∠)_"
    await kaibai.finish(reply_msg)


what_time = on_keyword({'几点了'}, priority=5)


# 注册事件响应器 what_time 关键字回复，优先级为 5
@what_time.handle()
# 触发了就回复
async def what_time_handle():
    reply_msg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    await what_time.finish(reply_msg)


# 注册事件响应器 ali_is_good 关键字回复，优先级为 5
ali_is_good = on_keyword({'阿狸好聪明', '阿狸真聪明'}, priority=5)


@ali_is_good.handle()
async def ali_is_good_reply_handle():
    reply_msg = "阿狸以后还会更努力噢！"
    await ali_is_good.finish(reply_msg)


# 注册事件响应器 yummy_fish 关键字回复，优先级为 5
yummy_fish = on_keyword({'秋刀鱼'}, priority=5)


@yummy_fish.handle()
async def yummy_fish_reply_handle():
    reply_msg = "秋刀鱼，哪里有秋刀鱼？"
    await yummy_fish.finish(reply_msg)


# 注册事件响应器 ali_source_code 关键字回复，优先级为 5
ali_source_code = on_keyword({'阿狸源码', '阿狸开源'}, priority=5)
# 回复字典
reply_ali_source_code_list = ['不给你看！', 'https://github.com/paoka1/Ali-Bot']


@ali_source_code.handle()
async def ali_source_code_reply_handle():
    # 随机选择回复消息
    reply_msg = random.choice(reply_ali_source_code_list)
    await ali_source_code.finish(reply_msg)


# 注册事件响应器 ali_brith 关键字回复，优先级为 5
ali_birth = on_keyword({'阿狸几岁了', '阿狸多大了', '你几岁了', '你多大了'}, priority=5)
# 阿狸出生的时间戳
birth_unix = 1642870599


@ali_birth.handle()
async def ali_birth_reply_handle():
    # 现在的时间
    now_time = int(time.time())
    # 计算出生的天数
    birth_day_to_today = int((now_time - int(birth_unix)) / 86400) + 1
    reply_msg = str(birth_day_to_today)
    # 整合消息
    reply_msg = "阿狸已经出生" + reply_msg + "天了哦"
    await ali_birth.finish(reply_msg)


# 注册事件响应器 call_ali，优先级为 6，防止冲突
call_ali = on_keyword({'阿狸', 'Ali'}, priority=6)
# 回复列表
reply_call_ali_list = ['怎么啦', '有什么事吗', '阿狸不在', '阿狸喜欢美味的秋刀鱼！', '诶？']


@call_ali.handle()
async def call_ali_reply_handle():
    # 随机选择回复消息
    reply_msg = random.choice(reply_call_ali_list)
    await call_ali.finish(reply_msg)


# 回应早安，具有判断时间选择性回复的功能
# 注册事件响应器 good_morning，优先级为 5
good_morning = on_keyword({'早上好'}, priority=5)
# 回复列表
reply_good_morning_list = ['这也太早了吧', '早上好~', '不早了，这都几点了', '晚上好']


@good_morning.handle()
async def good_morning_reply_handle():
    # 现在的小时数
    now_hour = int(time.strftime('%H', time.localtime(time.time())))
    # 根据时间选择回复内容
    if 3 <= now_hour <= 6:
        reply_msg = reply_good_morning_list[0]
    elif 6 < now_hour <= 9:
        reply_msg = reply_good_morning_list[1]
    elif 9 < now_hour <= 18:
        reply_msg = reply_good_morning_list[2]
    else:
        reply_msg = reply_good_morning_list[3]
    await good_morning.finish(reply_msg)
