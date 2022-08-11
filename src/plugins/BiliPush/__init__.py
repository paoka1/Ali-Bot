from nonebot import require, get_bot, get_driver
from nonebot.adapters.cqhttp import MessageSegment, Message

from .config import *
from .sqlite import *
from .bili_live_api import *
from .bili_dynamic_api import *

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
        await asyncio.sleep(plugin_config.bili_live_time_get)
        bili_live_info = await bili_live_api.bli_live_status(int(uid))

        # 如果获取到的信息有问题，就直接跳到下一次查询（由网络原因或数据解析时发生错误导致）
        if bili_live_info.code != 0:
            continue

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


# 所有要进行动态推送 up 的 uid 列表
dynamic_uid_list = []
# dynamic_inform_to_group 用来记录要推送的群聊
dynamic_inform_to_group = []

# 加载关注列表
for item in plugin_config.bili_dynamic_inform_group:
    dynamic_uid_list.extend(plugin_config.bili_dynamic_inform_group[item])
dynamic_uid_list = list(set(dynamic_uid_list))

# 初始化数据库
sqlite.init_dynamic_table(plugin_config.db_path)
sqlite.empty_dynamic_table(plugin_config.db_path)


# 获取最新的动态，并插入数据库
async def bili_dynamic_push_init():
    for up_uid in dynamic_uid_list:
        bili_dynamic_status = await bili_dynamic_api.get_bli_dynamic_status(int(up_uid))
        last_dynamic = bili_dynamic_status[0]

        sqlite.insert_to_dynamic_table(plugin_config.db_path, last_dynamic.get_up_uid(), last_dynamic.get_up_name(),
                                       last_dynamic.dynamic_id_str, last_dynamic.timestamp,
                                       last_dynamic.get_orig_dynamic_id_str())
        await asyncio.sleep(plugin_config.bili_dynamic_time_init_get)
asyncio.run(bili_dynamic_push_init())


# 设置定时任务，间隔 90 秒
@scheduler.scheduled_job('interval', seconds=plugin_config.bili_dynamic_time_all)
async def bili_dynamic_push():
    for uid in dynamic_uid_list:
        # push_status 表明是否进行推送
        push_status = False
        # 要推送的动态
        dynamic_to_push = []

        # 请求间隔
        await asyncio.sleep(plugin_config.bili_dynamic_time_get)
        # 发送请求
        bili_dynamic_info = await bili_dynamic_api.get_bli_dynamic_status(int(uid))

        # 如果获取到的信息有问题，就直接跳到下一次查询（由网络原因或数据解析时发生错误导致）
        if len(bili_dynamic_info) == 0 or bili_dynamic_info[0].code != 0:
            continue

        last_dynamic_id_str = sqlite.get_dynamic_id_str(plugin_config.db_path, uid)

        for dynamic_info in bili_dynamic_info:
            if dynamic_info.dynamic_id_str == last_dynamic_id_str:
                # 索引为 0 表明没有更新动态
                if bili_dynamic_info.index(dynamic_info) == 0:
                    break
                # 拿到新动态的列表，并把这个列表反转（把新发的动态放在后面）
                dynamic_to_push = bili_dynamic_info[:bili_dynamic_info.index(dynamic_info)][::-1]
                sqlite.update_dynamic_id_str(plugin_config.db_path, uid, (dynamic_to_push[-1]).dynamic_id_str)

                push_status = True
                break
            else:
                push_status = False

        # dynamic_to_push 为空或 push_status 为 False
        # 说明没有更新动态或者在返回数据中没找到上次记录的最新动态 id
        # 可能因为删除了动态或者 api 返回的数据全是新发的动态
        # 直接记录最新的动态，跳到对下一个 up 动态的处理
        if not push_status or len(dynamic_to_push) == 0:
            sqlite.update_dynamic_id_str(plugin_config.db_path, uid, (bili_dynamic_info[0]).dynamic_id_str)
            continue

        msgs = []

        # 把动态提取，构造消息
        for dynamic_info in dynamic_to_push:
            # 转发的动态类型
            if dynamic_info.dynamic_type == 1:
                # 原动态的内容
                orig_dynamic = dynamic_info.get_orig_dynamic()
                # 原动态为带图片的动态类型
                if orig_dynamic.dynamic_type == 2:
                    msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                                   + MessageSegment.text(dynamic_info.get_post_time() + "转发了") \
                                   + MessageSegment.text(dynamic_info.get_orig_up_name() + "的动态")
                    short_dynamic_content = dynamic_info.get_short_dynamic_content(plugin_config.bili_dynamic_length)

                    if len(short_dynamic_content) != 0 and short_dynamic_content != "转发动态":
                        msg += MessageSegment.text("，并说" + short_dynamic_content)

                    msg += MessageSegment.text("\n" + orig_dynamic.get_short_dynamic_content(
                        plugin_config.bili_orig_dynamic_length))
                    dynamic_picture_less_url_list = orig_dynamic.get_dynamic_picture_less_url_list(
                        plugin_config.bili_orig_picture_amount)

                    if len(dynamic_picture_less_url_list) == 0:
                        msg += "\n"

                    for picture in dynamic_picture_less_url_list:
                        msg += MessageSegment.image(picture)

                    msg += MessageSegment.text(dynamic_info.get_dynamic_link())
                # 原动态为纯文字的动态类型
                elif orig_dynamic.dynamic_type == 4:
                    msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                                   + MessageSegment.text(dynamic_info.get_post_time() + "转发了") \
                                   + MessageSegment.text(dynamic_info.get_orig_up_name() + "的动态")
                    short_dynamic_content = dynamic_info.get_short_dynamic_content(plugin_config.bili_dynamic_length)

                    if len(short_dynamic_content) != 0 and short_dynamic_content != "转发动态":
                        msg += MessageSegment.text("，并说" + short_dynamic_content)

                    msg += MessageSegment.text("\n" + orig_dynamic.get_short_dynamic_content(
                        plugin_config.bili_orig_dynamic_length))
                    msg += MessageSegment.text("\n" + dynamic_info.get_dynamic_link())
                # 原动态为发布视频的动态类型
                elif orig_dynamic.dynamic_type == 8:
                    msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                                   + MessageSegment.text(dynamic_info.get_post_time() + "转发了") \
                                   + MessageSegment.text(dynamic_info.get_orig_up_name() + "的投稿")
                    short_dynamic_content = dynamic_info.get_short_dynamic_content(plugin_config.bili_dynamic_length)

                    if len(short_dynamic_content) != 0 and short_dynamic_content != "转发动态":
                        msg += MessageSegment.text("，并说" + short_dynamic_content)

                    msg += MessageSegment.text("\n" + orig_dynamic.get_video_title())
                    msg += MessageSegment.image(orig_dynamic.get_video_cover())
                    msg += MessageSegment.text("\n" + dynamic_info.get_dynamic_link())
                # 原动态为不支持的动态类型
                else:
                    msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                                   + MessageSegment.text(dynamic_info.get_post_time() + "转发了") \
                                   + MessageSegment.text(dynamic_info.get_orig_up_name() + "的动态")
                    short_dynamic_content = dynamic_info.get_short_dynamic_content(plugin_config.bili_dynamic_length)

                    if len(short_dynamic_content) != 0 and short_dynamic_content != "转发动态":
                        msg += MessageSegment.text("，并说" + short_dynamic_content)

                    msg += MessageSegment.text("\n" + orig_dynamic.get_dynamic_content())
                    msg += MessageSegment.text("\n" + dynamic_info.get_dynamic_link())

            # 带图片的动态类型
            elif dynamic_info.dynamic_type == 2:
                msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                               + MessageSegment.text(dynamic_info.get_post_time() + "发布了新动态\n") \
                               + MessageSegment.text(dynamic_info.get_short_dynamic_content(
                                plugin_config.bili_dynamic_length))
                dynamic_picture_less_url_list = dynamic_info.get_dynamic_picture_less_url_list(
                    plugin_config.bili_dynamic_picture_amount)

                if len(dynamic_picture_less_url_list) == 0:
                    msg += "\n"

                for picture in dynamic_picture_less_url_list:
                    msg += MessageSegment.image(picture)

                msg += MessageSegment.text(dynamic_info.get_dynamic_link())
            # 纯文字的动态类型
            elif dynamic_info.dynamic_type == 4:
                msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                               + MessageSegment.text(dynamic_info.get_post_time() + "发布了新动态\n") \
                               + MessageSegment.text(dynamic_info.get_short_dynamic_content(
                                plugin_config.bili_dynamic_length) + "\n") \
                               + MessageSegment.text(dynamic_info.get_dynamic_link())
            # 发布视频的动态类型
            elif dynamic_info.dynamic_type == 8:
                msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                               + MessageSegment.text(dynamic_info.get_post_time() + "投稿了新视频\n") \
                               + MessageSegment.text(dynamic_info.get_video_title() + "\n") \
                               + MessageSegment.text(dynamic_info.get_short_dynamic_content(
                                plugin_config.bili_dynamic_length)) \
                               + MessageSegment.image(dynamic_info.get_video_cover()) \
                               + MessageSegment.text(dynamic_info.get_short_video_describe(
                                plugin_config.bili_video_describe_length) + "\n") \
                               + MessageSegment.text(dynamic_info.get_video_link())
            # 不支持的动态类型
            else:
                msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                               + MessageSegment.text(dynamic_info.get_post_time() + "发布了新动态\n") \
                               + MessageSegment.text(dynamic_info.get_dynamic_content() + "\n") \
                               + MessageSegment.text(dynamic_info.get_dynamic_link())
            msgs.append(msg)

        dynamic_inform_to_group.clear()

        # 查找出要推送的群聊
        for group in plugin_config.bili_dynamic_inform_group:
            if uid in plugin_config.bili_dynamic_inform_group[group]:
                dynamic_inform_to_group.append(group)

        # 开始推送
        for group in dynamic_inform_to_group:
            for msg in msgs:
                await get_bot().call_api('send_group_msg', **{
                    'message': msg,
                    'group_id': int(group)
                })
                await asyncio.sleep(plugin_config.bili_dynamic_time_send)
