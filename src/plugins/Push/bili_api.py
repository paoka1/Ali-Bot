import asyncio
import httpcore
import httpx
import random
import json
import time


class LiveRoom:
    liveStatus: int
    url: str
    title: str
    cover: str

    def __init__(self, data: dict) -> None:
        self.liveStatus = data['liveStatus']
        self.url = data['url']
        self.title = data['title']
        self.cover = data['cover']


class User:
    uid: int
    code: int
    name: str
    face: str
    message: str
    room: LiveRoom

    def __init__(self, data: dict, code: int, message: str) -> None:
        self.code = code
        self.uid = data['mid']
        self.name = data['name']
        self.face = data['face']
        self.message = message
        self.room = LiveRoom(data['live_room'])


# 随机请求头
def get_header() -> dict:
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 '
        '(maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
        '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    ]
    user_agent = random.choice(user_agent_list)
    header = {'User-Agent': user_agent}
    return header


# get_status 用于获取状态报文
async def get_status(uid: int) -> dict:
    async with httpx.AsyncClient() as client:
        url = "https://api.bilibili.com/x/space/acc/info?mid={0}&jsonp=jsonp".format(uid)
        try:
            r = await client.get(url, headers=get_header())
            r.encoding = 'utf-8'
        # 捕获因网络原因造成的 timeout 异常
        except (asyncio.exceptions.CancelledError, TimeoutError, httpcore.ConnectTimeout, httpx.ConnectTimeout):
            print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
                  f"1;31mERROR\033[0m] \033[4;36m哔哩哔哩直播推送(Push)\033[0m | 请求 {url} 时出错，"
                  f"这可能是因为 API 失效或者网络不佳而造成的")
            none_data = {"data": {"mid": 0,
                                  "name": '',
                                  "face": '',
                                  "live_room": {"liveStatus": 0, "url": "", "title": "", "cover": ""}},
                         "code": -1000,
                         "message": ""}
            return none_data
        try:
            bili_data = json.loads(r.text)
        # 捕获因解析 json 造成的 json.decoder.JSONDecodeError 异常
        except json.decoder.JSONDecodeError:
            print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
                  f"1;31mERROR\033[0m] \033[4;36m哔哩哔哩直播推送(Push)\033[0m | 解析 json 数据时出错，"
                  f"这可能是因为接收到的数据不正确而造成的")
            none_data = {"data": {"mid": 0,
                                  "name": '',
                                  "face": '',
                                  "live_room": {"liveStatus": 0, "url": "", "title": "", "cover": ""}},
                         "code": -2000,
                         "message": ""}
            return none_data
        return bili_data


# bili_api 程序接口
async def bli_status(uid: int) -> User:
    resp = await get_status(uid)
    try:
        bli_info = User(resp['data'], resp['code'], resp['message'])
    # 捕获 API 返回数据解析时发生的异常
    except (TypeError, KeyError):
        print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033[1;31mERROR\033[0m] "
              f"\033[4;36m哔哩哔哩直播推送(Push)\033[0m | 解析时出错，这可能是因为 API "
              f"返回数据不正确而导致的，错误代码：{resp['code']}，错误消息：{resp['message']}")
        none_data = {"data": {"mid": 0,
                              "name": '',
                              "face": '',
                              "live_room": {"liveStatus": 0, "url": "", "title": "", "cover": ""}},
                     "code": -3000,
                     "message": ""}
        bli_info = User(none_data['data'], none_data['code'], none_data['message'])
    return bli_info

if __name__ == '__main__':
    res = asyncio.run(bli_status(53456))
    print(res.__dict__)
    print(res.room.__dict__)
