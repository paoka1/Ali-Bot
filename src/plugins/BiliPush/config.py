from pydantic import BaseSettings


class Config(BaseSettings):
    # 请求直播状态整体间隔时间
    bili_live_time_all = 40
    # 请求直播状态单次间隔时间
    bili_live_time_get = 1
    # 发送消息后的间隔时间
    bili_live_time_send = 1

    # 直播订阅群聊和阿婆主
    bili_live_inform_group = {}

    # 数据库路径
    db_path = "/home/xiaoha/mybot/bot.db"

    # 请求直播动态整体间隔时间
    bili_dynamic_time_all = 90
    # 请求动态状态单次间隔时间
    bili_dynamic_time_get = 2
    # 初始化数据库时请求动态状态单次间隔时间
    bili_dynamic_time_init_get = 1
    # 发送消息后的间隔时间
    bili_dynamic_time_send = 1

    # 动态正文最大长度
    bili_dynamic_length = 40
    # 视频动态视频简介最大长度
    bili_video_describe_length = 40
    # 图文动态最大图片数量
    bili_dynamic_picture_amount = 3
    # 转发动态原动态最大长度
    bili_orig_dynamic_length = 40
    # 转发动态原动态最大图片数量
    bili_orig_picture_amount = 2

    # 动态订阅群聊和阿婆主
    bili_dynamic_inform_group = {}

    class Config:
        extra = "ignore"
