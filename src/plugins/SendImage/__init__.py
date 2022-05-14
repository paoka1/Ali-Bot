# 发送图片

from pathlib import Path
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import MessageSegment

all_right_right = on_keyword({'啊对对对'}, priority=4)


@all_right_right.handle()
async def all_right_right_reply_handle():
    # 本地图片位置
    path = Path(__file__).parent / "../../../resource/image/common/ah_right_right.jpg"
    # 构造图片消息段
    image = MessageSegment.image(path)
    # 发送图片
    await all_right_right.finish(image)


az = on_keyword({'啊这'}, priority=4)


@az.handle()
async def az_reply_handle():
    path = Path(__file__).parent / "../../../resource/image/common/az.jpg"
    image = MessageSegment.image(path)
    await az.finish(image)


happy = on_keyword({'开心', '高兴', '快乐'}, priority=4)


@happy.handle()
async def happy_reply_handle():
    path = Path(__file__).parent / "../../../resource/image/common/happy.jpg"
    image = MessageSegment.image(path)
    await happy.finish(image)


kaibai_sleep = on_keyword({'累', '困', '睡觉'}, priority=4)


@kaibai_sleep.handle()
async def kaibai_sleep_reply_handle():
    path = Path(__file__).parent / "../../../resource/image/common/kaibai.jpg"
    image = MessageSegment.image(path)
    await kaibai_sleep.finish(image)
