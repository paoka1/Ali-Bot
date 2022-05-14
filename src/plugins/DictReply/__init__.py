from nonebot import get_driver
from nonebot.adapters.cqhttp import Event
from nonebot.plugin import on_message

from .config import *

# 导入配置文件
global_config = get_driver().config
plugin_config = Config(**global_config.dict())

reply_dic = plugin_config.reply_dic

# 注册事件响应器 reply 优先级为 8
# 修复 BUG: 设置 block 为 False 让优先级靠后的响应器也能接着处理
reply = on_message(priority=8, block=False)


@reply.handle()
async def reply_handle(event: Event):
    user_msg = str(event.get_message()).strip()
    # 在回复字典找到了 key 就回复
    try:
        reply_msg = reply_dic[user_msg]
        await reply.finish(reply_msg)
    # 没找到 key 就当什么都没有发生
    except KeyError:
        await reply.finish()
