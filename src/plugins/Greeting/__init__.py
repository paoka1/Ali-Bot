import time
from nonebot import require, get_bot, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message

from .qweather_api import *
from .config import *

scheduler = require('nonebot_plugin_apscheduler').scheduler

# 导入配置文件
global_config = get_driver().config
plugin_config = Config(**global_config.dict())


@scheduler.scheduled_job('cron', hour=plugin_config.weather_push_time['hour'],
                         minute=plugin_config.weather_push_time['minute'])
async def morning_push():
    for group in plugin_config.weather_inform_group:
        for location in plugin_config.weather_inform_group[group]:
            try_count = 1
            push_status = True

            weather_status = await get_weather(location, plugin_config.qweather_key)
            # 获取的信息不正确就重试
            while weather_status.code != 200:
                # 已经耗尽了尝试次数
                if try_count > plugin_config.weather_max_try:
                    print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
                          f"1;31mERROR\033[0m] \033[4;36m天气插件(Greeting)\033[0m | 对群聊 {group} "
                          f"地区 {location} 天气信息获取失败，已使用最大重试次数")
                    push_status = False
                    break
                print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
                      f"1;31mERROR\033[0m] \033[4;36m天气插件(Greeting)\033[0m | 对群聊 {group} "
                      f"地区 {location} 天气信息获取失败，已尝试次数：{try_count}，还剩余 "
                      f"{plugin_config.weather_max_try - try_count} 次重试的次数")
                weather_status = await get_weather(location, plugin_config.qweather_key)
                try_count += 1
                await asyncio.sleep(plugin_config.weather_time_fail)

            # 耗尽了尝试次数就跳过本次推送，进行下一个地区的推送
            if not push_status:
                continue
            print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
                  f"1;34mSUCCESS\033[0m] \033[4;36m天气插件(Greeting)\033[0m | 对群聊 {group} "
                  f"地区 {location} 天气信息获取成功，已尝试次数：{try_count}")
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
            await asyncio.sleep(plugin_config.weather_time_send)
