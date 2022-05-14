from nonebot.adapters.cqhttp import Event
from nonebot.plugin import on_message
import random

# 注册事件响应器 random_repeater 优先级为 10
random_repeater = on_message(priority=10, block=False)

# 颜文字列表
kaomoji_list = ['(๑• . •๑)',
                '(´▽｀)ノ♪',
                '|･ω･｀)',
                '(｢･ω･)｢嘿',
                '(｢･ω･)｢哈',
                '( •̥́ ˍ •̀ू )',
                '(⁄ ⁄•⁄ω⁄•⁄ ⁄)',
                '(〃′o`)',
                '╭( ′• o •′ )╭就是这个人！',
                'ヽ(*´з｀*)ﾉ',
                '|ω・)']


@random_repeater.handle()
async def random_repeater_reply(event: Event):
    user_msg = str(event.get_message()).strip()
    ran_num = random.random()
    # 对于非 CQ 码消息随机回复 +1
    if (0 < ran_num < 0.005) and ("CQ" not in user_msg):
        await random_repeater.finish(user_msg)
    # 随机回复颜文字
    if 0.5 < ran_num < 0.505:
        reply_msg = random.choice(kaomoji_list)
        await random_repeater.finish(reply_msg)
    await random_repeater.finish()
