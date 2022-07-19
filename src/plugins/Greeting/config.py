from pydantic import BaseSettings


class Config(BaseSettings):
    # 天气信息推送时间
    weather_push_time = {"hour": 7, "minute": 0}

    # 获取天气信息的最大次尝试次数
    weather_max_try = 5

    # 天气信息获取失败时再次尝试前的时间间隔
    weather_time_fail = 2
    # 发送消息后的间隔时间
    weather_time_send = 2

    # 和风天气 key
    qweather_key = ''

    # 通知群聊与地区
    weather_inform_group = {}

    class Config:
        extra = "ignore"
