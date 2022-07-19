from pydantic import BaseSettings


class Config(BaseSettings):
    # 请求直播状态整体间隔时间
    bili_live_time_all = 40
    # 请求直播状态整体单次时间
    bili_live_time_get = 1
    # 发送消息后的间隔时间
    bili_live_time_send = 1

    # 订阅群聊和阿婆主
    bili_live_inform_group = {}

    class Config:
        extra = "ignore"
