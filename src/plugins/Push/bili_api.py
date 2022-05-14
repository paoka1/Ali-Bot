import requests
import json


class LiveRoom:
    liveStatus: int
    url: str
    title: str
    cover: str

    def __init__(self, data: dict):
        self.liveStatus = data['liveStatus']
        self.url = data['url']
        self.title = data['title']
        self.cover = data['cover']


class User:
    uid: int
    name: str
    face: str
    room: LiveRoom

    def __init__(self, data: dict):
        self.uid = data['mid']
        self.name = data['name']
        self.face = data['face']
        self.room = LiveRoom(data['live_room'])


# get_status 用于获取状态报文
def get_status(uid: int):
    url = "https://api.bilibili.com/x/space/acc/info?mid={0}&jsonp=jsonp".format(uid)
    r = requests.get(url)
    r.encoding = "utf-8"
    return json.loads(r.text)


# bili_api 程序接口
def bli_status(uid: int):
    resp = get_status(uid)
    bli_info = User(resp['data'])
    return bli_info
