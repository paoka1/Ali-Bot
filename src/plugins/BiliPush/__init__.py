from nonebot import require, get_bot, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message

from .bili_live_api import *
from .config import *

scheduler = require('nonebot_plugin_apscheduler').scheduler

# 导入配置文件
global_config = get_driver().config
plugin_config = Config(**global_config.dict())

# 所有要进行直播推送 up 的 uid 列表
live_uid_list = []
# live_bili_status 用来记录直播状态
live_bili_status = {}
# live_inform_to_group 用来记录要推送的群聊
live_inform_to_group = []

# 加载关注列表
for item in plugin_config.bili_live_inform_group:
    live_uid_list.extend(plugin_config.bili_live_inform_group[item])
live_uid_list = list(set(live_uid_list))


# 设置定时任务，间隔 40 秒
@scheduler.scheduled_job('interval', seconds=plugin_config.bili_live_time_all)
async def bili_live_push():
    global live_bili_status

    for uid in live_uid_list:
        # 获取直播状态
        bili_live_info = await bili_live_api.bli_live_status(int(uid))
        # 如果获取到的信息有问题，就直接取消本次查询（由网络原因或数据解析时发生错误导致）
        if bili_live_info.code != 0:
            return
        await asyncio.sleep(plugin_config.bili_live_time_get)
        # 避免 bot 启动时正在直播，又推送了，默认 True
        pre: bool = live_bili_status.get(uid, True)
        now: bool = bili_live_info.room.liveStatus == 1
        live_bili_status[uid] = now

        if now and not pre:
            msg: Message = MessageSegment.text('阿婆主：' + bili_live_info.name) \
                           + MessageSegment.text(' 开播啦！') \
                           + MessageSegment.text(bili_live_info.room.title) \
                           + MessageSegment.image(bili_live_info.room.cover) \
                           + MessageSegment.text(bili_live_info.room.url.split('?')[0])

            live_inform_to_group.clear()

            # 查找出要推送的群聊
            for group in plugin_config.bili_live_inform_group:
                if uid in plugin_config.bili_live_inform_group[group]:
                    live_inform_to_group.append(group)

            # 开始推送
            for group in live_inform_to_group:
                await get_bot().call_api('send_group_msg', **{
                    'message': msg,
                    'group_id': int(group)
                })
                await asyncio.sleep(plugin_config.bili_live_time_send)
