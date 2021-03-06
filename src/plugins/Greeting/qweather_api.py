import json
import httpx
import asyncio
import httpcore
from datetime import date


class Today:
    day: str
    month: str
    week_day: str

    def __init__(self, data: dict) -> None:
        self.day = data['day']
        self.month = data['month']
        self.week_day = data['week_day']


class WeatherInfo:
    pos: str
    code: int
    today: Today
    tempMax: str
    tempMin: str
    textDay: str
    textNight: str

    def __init__(self, data: dict, code: int, today: dict, pos: str) -> None:
        self.pos = pos
        self.code = code
        self.today = Today(today)
        self.tempMax = data['tempMax']
        self.tempMin = data['tempMin']
        self.textDay = data['textDay']
        self.textNight = data['textNight']


# get_today 获取今天的月份，天数和星期几
def get_today() -> dict:
    today = date.today()
    week_day_list = ['一', '二', '三', '四', '五', '六', '日']
    today_info = dict(day=str(today.day), month=str(today.month), week_day=week_day_list[today.weekday()])
    return today_info


# get_weather_info 获取天气信息
async def get_weather_info(location: str, key: str) -> dict:
    async with httpx.AsyncClient() as client:
        url = "https://devapi.qweather.com/v7/weather/3d?key={0}&location={1}".format(key, location)
        r = await client.get(url)
        r.encoding = 'utf-8'
        return json.loads(r.text)


# get_pos 获取城市等信息
async def get_pos(location: str, key: str) -> dict:
    async with httpx.AsyncClient() as client:
        url = "https://geoapi.qweather.com/v2/city/lookup?key={0}&location={1}".format(key, location)
        r = await client.get(url)
        r.encoding = 'utf-8'
        return json.loads(r.text)


# qweather_api 接口
async def get_weather(location: str, key: str) -> WeatherInfo:
    today = get_today()
    try:
        pos = await get_pos(location, key)
        weather = await get_weather_info(location, key)
    # 捕获因网络原因造成的 timeout 异常
    except (asyncio.exceptions.CancelledError, TimeoutError, httpcore.ConnectTimeout, httpx.ConnectTimeout):
        none_data = {"pos": '',
                     "code": -100,
                     "today": {"day": '', "month": '', "week_day": ''},
                     "daily": {"tempMax": '', "tempMin": '', "textDay": '', "textNight": ''}}
        weather_status = WeatherInfo(none_data["daily"], none_data["code"], none_data["today"], none_data['pos'])
        return weather_status
    weather_status = WeatherInfo(weather['daily'][0], int(weather['code']), today, pos['location'][0]['name'])
    return weather_status


if __name__ == '__main__':
    # 在这里填上你的 key
    qw_key = ''
    res = asyncio.run(get_weather('101190101', qw_key))
    print(res.__dict__)
    print(res.today.__dict__)
