import json
import time
import httpx
import random
import asyncio
import httpcore


# 动态基类
class Dynamic(object):
    code: int
    message: str
    timestamp: int
    dynamic_id_str: str
    dynamic_type: int
    dynamic_desc: dict
    dynamic_card: dict

    def __init__(self, code, message, dynamic_desc, dynamic_card) -> None:
        self.code = code
        self.message = message
        self.timestamp = dynamic_desc['timestamp']
        self.dynamic_id_str = dynamic_desc['dynamic_id_str']
        self.dynamic_desc = dynamic_desc
        self.dynamic_card = dynamic_card

    # 获取动态链接
    def get_dynamic_link(self) -> str:
        dynamic_link = "https://t.bilibili.com/" + self.dynamic_id_str
        return dynamic_link

    # 获取 up 主昵称
    def get_up_name(self) -> str:
        up_name = self.dynamic_desc['user_profile']['info']['uname']
        return up_name

    # 获取 up 主 uid
    def get_up_uid(self) -> int:
        up_uid = self.dynamic_desc['user_profile']['info']['uid']
        return up_uid

    # 获取动态发布时间（%m-%d %H:%M）
    def get_post_time(self) -> str:
        post_time_array = time.localtime(self.timestamp)
        post_time = time.strftime("%m-%d %H:%M", post_time_array)

        return post_time

    # 获取转发动态的原动态 id_str
    def get_orig_dynamic_id_str(self) -> None:
        return None


# 发生错误的动态类型
class ErrorDynamic(object):
    code: int
    message: str

    def __init__(self, code, message) -> None:
        self.code = code
        self.message = message


# 不支持的动态类型
class UnsupportedDynamic(Dynamic):

    def __init__(self, code, message, dynamic_desc, dynamic_card) -> None:
        super().__init__(code, message, dynamic_desc, dynamic_card)
        self.dynamic_type = -1

    # 获取不支持的动态内容，为 `「不支持的动态类型」请点击链接查看`
    @staticmethod
    def get_dynamic_content() -> str:
        dynamic_content = "「不支持的动态类型」请点击链接查看"
        return dynamic_content


# 带图片的动态类型
class PictureDynamic(Dynamic):

    def __init__(self, code, message, dynamic_desc, dynamic_card) -> None:
        super().__init__(code, message, dynamic_desc, dynamic_card)
        self.dynamic_type = 2

    # 获取动态文字内容
    def get_dynamic_content(self) -> str:
        dynamic_content = self.dynamic_card['item']['description']
        return dynamic_content

    # 裁剪动态内容
    def get_short_dynamic_content(self, dynamic_length: int) -> str:
        dynamic_content = self.get_dynamic_content()

        if dynamic_length == -1:
            short_dynamic_content = dynamic_content
            return short_dynamic_content

        if len(dynamic_content) > dynamic_length:
            short_dynamic_content = dynamic_content[:dynamic_length]
            short_dynamic_content += "..."
        else:
            short_dynamic_content = dynamic_content

        return short_dynamic_content

    # 获取图片的 url（list）
    def get_dynamic_picture_url_list(self) -> list:
        dynamic_picture_url_list = []

        for dynamic_picture_url in self.dynamic_card['item']['pictures']:
            dynamic_picture_url_list.append(dynamic_picture_url['img_src'])
        return dynamic_picture_url_list

    # 裁剪图片数量
    def get_dynamic_picture_less_url_list(self, picture_amount: int) -> list:
        dynamic_picture_url_list = self.get_dynamic_picture_url_list()

        if picture_amount == -1:
            dynamic_picture_less_url_list = dynamic_picture_url_list
            return dynamic_picture_less_url_list

        if len(dynamic_picture_url_list) > picture_amount:
            dynamic_picture_less_url_list = dynamic_picture_url_list[:picture_amount]
        else:
            dynamic_picture_less_url_list = dynamic_picture_url_list

        return dynamic_picture_less_url_list


# 纯文字的动态类型
class TextDynamic(Dynamic):

    def __init__(self, code, message, dynamic_desc, dynamic_card) -> None:
        super().__init__(code, message, dynamic_desc, dynamic_card)
        self.dynamic_type = 4

    # 获取动态内容
    def get_dynamic_content(self) -> str:
        dynamic_content = self.dynamic_card['item']['content']
        return dynamic_content

    # 裁剪动态内容
    def get_short_dynamic_content(self, dynamic_length: int) -> str:
        dynamic_content = self.get_dynamic_content()

        if dynamic_length == -1:
            short_dynamic_content = dynamic_content
            return short_dynamic_content

        if len(dynamic_content) > dynamic_length:
            short_dynamic_content = dynamic_content[:dynamic_length]
            short_dynamic_content += "..."
        else:
            short_dynamic_content = dynamic_content

        return short_dynamic_content


# 发布视频的动态类型
class VideoDynamic(Dynamic):

    def __init__(self, code, message, dynamic_desc, dynamic_card) -> None:
        super().__init__(code, message, dynamic_desc, dynamic_card)
        self.dynamic_type = 8

    # 获取动态内容
    def get_dynamic_content(self) -> str:
        dynamic_content = self.dynamic_card['dynamic']
        return dynamic_content

    # 裁剪动态内容
    def get_short_dynamic_content(self, dynamic_length: int) -> str:
        dynamic_content = self.get_dynamic_content()

        if dynamic_length == -1:
            short_dynamic_content = dynamic_content
            return short_dynamic_content

        if len(dynamic_content) > dynamic_length:
            short_dynamic_content = dynamic_content[:dynamic_length]
            short_dynamic_content += "..."
        else:
            short_dynamic_content = dynamic_content

        return short_dynamic_content

    # 获取视频标题
    def get_video_title(self) -> str:
        video_title = self.dynamic_card['title']
        return video_title

    # 获取视频简介
    def get_video_describe(self) -> str:
        video_describe = self.dynamic_card['desc']
        return video_describe

    # 裁剪视频简介
    def get_short_video_describe(self, describe_length: int) -> str:
        video_describe = self.get_video_describe()

        if describe_length == -1:
            short_video_describe = video_describe
            return short_video_describe

        if len(video_describe) > describe_length:
            short_video_describe = video_describe[:describe_length]
            short_video_describe += "..."
        else:
            short_video_describe = video_describe

        return short_video_describe

    # 获取视频链接
    def get_video_link(self) -> str:
        video_link = self.dynamic_card['short_link_v2']
        return video_link

    # 获取视频封面
    def get_video_cover(self) -> str:
        video_cover = self.dynamic_card['pic']
        return video_cover


# 转发的动态类型
class ForwardDynamic(Dynamic):
    orig_dynamic_timestamp: int

    def __init__(self, code, message, dynamic_desc, dynamic_card) -> None:
        super().__init__(code, message, dynamic_desc, dynamic_card)
        self.dynamic_type = 1
        self.orig_dynamic_timestamp = self.dynamic_desc['origin']['timestamp']

    # 原动态 id_str
    def get_orig_dynamic_id_str(self) -> str:
        orig_dynamic_id_str = self.dynamic_desc['orig_dy_id']
        return orig_dynamic_id_str

    # 原动态链接
    def get_orig_dynamic_link(self) -> str:
        orig_dynamic_id_str = self.get_orig_dynamic_id_str()
        orig_dynamic_link = "https://t.bilibili.com/" + orig_dynamic_id_str

        return orig_dynamic_link

    # 原动态 up 主的名字
    def get_orig_up_name(self) -> str:
        orig_up_name = self.dynamic_card['origin_user']['info']['uname']
        return orig_up_name

    # 原动态 up uid
    def get_orig_up_uid(self) -> int:
        orig_up_uid = self.dynamic_desc['origin']['uid']
        return orig_up_uid

    # 获取原动态发布时间（%m-%d %H:%M）
    def get_orig_post_time(self) -> str:
        orig_post_time_array = time.localtime(self.orig_dynamic_timestamp)
        orig_post_time = time.strftime("%m-%d %H:%M", orig_post_time_array)

        return orig_post_time

    # 获取动态内容
    def get_dynamic_content(self) -> str:
        dynamic_content = self.dynamic_card['item']['content']
        return dynamic_content

    # 裁剪动态内容
    def get_short_dynamic_content(self, dynamic_length: int) -> str:
        dynamic_content = self.get_dynamic_content()

        if dynamic_length == -1:
            short_dynamic_content = dynamic_content
            return short_dynamic_content

        if len(dynamic_content) > dynamic_length:
            short_dynamic_content = dynamic_content[:dynamic_length]
            short_dynamic_content += "..."
        else:
            short_dynamic_content = dynamic_content

        return short_dynamic_content

    # 获取原动态内容并返回对应类型的实例，注意传入的 dynamic_desc 不是原动态的 dynamic_desc
    # 所以获取原动态某些与 dynamic_desc 有关的属性时请使用本类中 get_orig_xxx() 方法或 orig_dynamic_xxx 字段
    def get_orig_dynamic(self) -> PictureDynamic or TextDynamic or VideoDynamic or None:
        if self.dynamic_card['item']['orig_type'] == 2:
            picture_dynamic = PictureDynamic(self.code, self.message, self.dynamic_desc,
                                             json.loads(self.dynamic_card['origin']))
            return picture_dynamic
        elif self.dynamic_card['item']['orig_type'] == 4:
            text_dynamic = TextDynamic(self.code, self.message, self.dynamic_desc,
                                       json.loads(self.dynamic_card['origin']))
            return text_dynamic
        elif self.dynamic_card['item']['orig_type'] == 8:
            video_dynamic = VideoDynamic(self.code, self.message, self.dynamic_desc,
                                         json.loads(self.dynamic_card['origin']))
            return video_dynamic
        else:
            unsupported_dynamic = UnsupportedDynamic(self.code, self.message, self.dynamic_desc,
                                                     json.loads(self.dynamic_card['origin']))
            return unsupported_dynamic


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


# 发送请求
async def get_raw_dynamic_data(uid: int) -> dict:
    async with httpx.AsyncClient() as client:
        dynamic_url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history" \
                      f"?host_uid={uid}&offset_dynamic_id=0"
        dynamic_resp = await client.get(dynamic_url, headers=get_header())

    dynamic_resp.encoding = "utf-8"
    raw_dynamic_data = json.loads(dynamic_resp.text)

    return raw_dynamic_data


# 对动态进行分类、实例化动态对象
def get_dynamic_list(raw_dynamic_data: dict) -> list:
    dynamic_list = []
    dynamic_code = raw_dynamic_data['code']
    dynamic_message = raw_dynamic_data['message']
    raw_dynamic_list = raw_dynamic_data['data']['cards']

    for dynamic in raw_dynamic_list:
        dynamic_content = json.loads(dynamic['card'])
        if dynamic['desc']['type'] == 1:
            original_dynamic = ForwardDynamic(dynamic_code, dynamic_message, dynamic['desc'], dynamic_content)
            dynamic_list.append(original_dynamic)
        elif dynamic['desc']['type'] == 2:
            picture_dynamic = PictureDynamic(dynamic_code, dynamic_message, dynamic['desc'], dynamic_content)
            dynamic_list.append(picture_dynamic)
        elif dynamic['desc']['type'] == 4:
            text_dynamic = TextDynamic(dynamic_code, dynamic_message, dynamic['desc'], dynamic_content)
            dynamic_list.append(text_dynamic)
        elif dynamic['desc']['type'] == 8:
            video_dynamic = VideoDynamic(dynamic_code, dynamic_message, dynamic['desc'], dynamic_content)
            dynamic_list.append(video_dynamic)
        else:
            unsupported_dynamic = UnsupportedDynamic(dynamic_code, dynamic_message, dynamic['desc'], dynamic_content)
            dynamic_list.append(unsupported_dynamic)

    return dynamic_list


# bili_dynamic_api 接口
async def get_bli_dynamic_status(uid: int) -> list:
    try:
        raw_dynamic_data = await get_raw_dynamic_data(uid)
    # 捕获因网络原因造成的 timeout 异常
    except (asyncio.exceptions.CancelledError, TimeoutError, httpcore.ConnectTimeout, httpx.ConnectTimeout):
        print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
              f"1;31mERROR\033[0m] \033[4;36m哔哩哔哩动态推送(BiliPush)\033[0m | 请求 "
              f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history"
              f"?host_uid={uid}&offset_dynamic_id=0 时出错，这可能是因为 API 失效或者网络不佳而造成的")
        bli_dynamic_status = [ErrorDynamic(-1000, "")]

        return bli_dynamic_status
    # 捕获因 json 解析失败造成的 json.decoder.JSONDecodeError 异常
    except json.decoder.JSONDecodeError:
        print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
              f"1;31mERROR\033[0m] \033[4;36m哔哩哔哩动态推送(BiliPush)\033[0m | 解析 json 数据时出错，"
              f"这可能是因为接收到的数据不正确而造成的")
        bli_dynamic_status = [ErrorDynamic(-2000, "")]

        return bli_dynamic_status

    try:
        bli_dynamic_status = get_dynamic_list(raw_dynamic_data)
    # 捕获因 json 解析失败造成的 json.decoder.JSONDecodeError 异常
    except json.decoder.JSONDecodeError:
        print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033["
              f"1;31mERROR\033[0m] \033[4;36m哔哩哔哩动态推送(BiliPush)\033[0m | 解析 json 数据时出错，"
              f"这可能是因为接收到的数据不正确而造成的")
        bli_dynamic_status = [ErrorDynamic(-2000, "")]

        return bli_dynamic_status
    # 捕获 API 返回数据解析时发生的异常
    except (TypeError, KeyError):
        print(f"\033[32m{time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))}\033[0m [\033[1;31mERROR\033[0m] "
              f"\033[4;36m哔哩哔哩动态推送(BiliPush)\033[0m | 解析时出错，这可能是因为 API "
              f"返回数据不正确而导致的，错误代码：{raw_dynamic_data['code']}，错误消息：{raw_dynamic_data['message']}")
        bli_dynamic_status = [ErrorDynamic(-3000, "")]

        return bli_dynamic_status
    return bli_dynamic_status


if __name__ == '__main__':
    dynamic_status = asyncio.run(get_bli_dynamic_status(53456))
    print(dynamic_status[0].get_dynamic_link())
    print(dynamic_status[0].get_dynamic_content())
    print(dynamic_status[0].get_post_time())
