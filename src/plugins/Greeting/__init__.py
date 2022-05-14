import asyncio
from nonebot import require, get_bot, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message

from .qweather_api import *
from .config import *

scheduler = require('nonebot_plugin_apscheduler').scheduler

# 导入配置文件
global_config = get_driver().config
plugin_config = Config(**global_config.dict())


@scheduler.scheduled_job('cron', hour=7, minute=0)
async def morning_push():
    for group in plugin_config.inform_group:
        for location in plugin_config.inform_group[group]:
            weather_status = get_weather(location, plugin_config.key)

            # 构造消息
            msg: Message = (MessageSegment.text('早上好！')
                            + MessageSegment.text("今天是")
                            + MessageSegment.text(weather_status.today.month + '月')
                            + MessageSegment.text(weather_status.today.day + '日，')
                            + MessageSegment.text('星期')
                            + MessageSegment.text(weather_status.today.week_day + '。')
                            + MessageSegment.text(weather_status.pos)
                            + MessageSegment.text('今天白天天气：' + weather_status.textDay + '，')
                            + MessageSegment.text('今天夜间天气：' + weather_status.textNight + '。')
                            + MessageSegment.text('最高温度' + weather_status.tempMax + '度，')
                            + MessageSegment.text('最低温度' + weather_status.tempMin + '度。')
                            + MessageSegment.text('阿狸祝大家一切顺利 (⁄ ⁄•⁄ω⁄•⁄ ⁄)'))

            # 发送消息
            await get_bot().call_api('send_group_msg', **{
                'message': msg,
                'group_id': int(group)
            })
            await asyncio.sleep(20)
