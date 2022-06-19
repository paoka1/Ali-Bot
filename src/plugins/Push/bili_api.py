import httpx
import random
import json


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
    name: str
    face: str
    room: LiveRoom

    def __init__(self, data: dict) -> None:
        self.uid = data['mid']
        self.name = data['name']
        self.face = data['face']
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
        r = await client.get(url, headers=get_header())
        r.encoding = "utf-8"
        return json.loads(r.text)


# bili_api 程序接口
async def bli_status(uid: int) -> User:
    resp = await get_status(uid)
    bli_info = User(resp['data'])
    return bli_info
