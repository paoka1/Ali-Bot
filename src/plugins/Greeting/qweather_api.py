import json
import requests
from datetime import date


class Today:
    day: str
    month: str
    week_day: str

    def __init__(self, data: dict):
        self.day = data['day']
        self.month = data['month']
        self.week_day = data['week_day']


class WeatherInfo:
    pos: str
    today: Today
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str

    def __init__(self, data: dict, today: dict, pos: str):
        self.pos = pos
        self.today = Today(today)
        self.tempMax = data['tempMax']
        self.tempMin = data['tempMin']
        self.textDay = data['textDay']
        self.textNight = data['textNight']


# 获取今天的月份，天数和星期几
def get_today():
    today = date.today()
    week_day_list = ['一', '二', '三', '四', '五', '六', '日']
    today_info = dict(day=str(today.day), month=str(today.month), week_day=week_day_list[today.weekday()])
    return today_info


# 获取天气信息
def weather_info(location: str, key: str):
    url = 'https://devapi.qweather.com/v7/weather/3d?key={0}&location={1}'.format(key, location)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return json.loads(r.text)


# 获取城市等信息
def get_pos(location: str, key: str):
    url = 'https://geoapi.qweather.com/v2/city/lookup?key={0}&location={1}'.format(key, location)
    r = requests.get(url)
    r.encoding = 'utf-8'
    return json.loads(r.text)


# qweather api 接口
def get_weather(location: str, key: str):
    today = get_today()
    pos = get_pos(location, key)
    weather = weather_info(location, key)
    weather_status = WeatherInfo(weather['daily'][0], today, pos['location'][0]['name'])
    return weather_status
