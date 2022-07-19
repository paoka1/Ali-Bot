# How To Use

### 1.功能

1. 每天问早（外加天气信息），效果如下

   ![weather](../../../img/hw_greeting.jpg)

### 2.安装依赖

Windows 下（进入 Bot 的目录）

```bash
nb plugin install nonebot-plugin-apscheduler
```

Linux 下（进入 Bot 目录）

```bash
python3 -m nb_cli plugin
# 选择安装插件，再输入插件名称，如下（不需要井号和空格）
# nonebot-plugin-apscheduler
```

安装完后需要进行配置：请参考官方的 [配置方法指南](https://v2.nonebot.dev/docs/advanced/scheduler)（如果无效，可尝试把添加到`.env`文件的内容也添加到`.env.dev`文件中去，如果还是出现错误，请参考本 Bot 的`bot.py`文件来配置你的`bot.py`）。

### 3.使用教程

- 每天问好

  1. 在`config.py`向`qweather_key`添加你的和风天气的 key，向`weather_inform_group`添加要通知的群，群号是这个字典的键，要通知天气的区域代码写成一个列表作为字典的值（在下面我会介绍如何获取 key 和 区域代码）

  2. 例如，123 群关注了北京，456 群关注了 北京和南京，而你的 key 是 xxxx，则可以写成

     ```python
     # 和风天气 key
     qweather_key = 'xxxx'
     
     # 通知群聊与地区
     weather_inform_group = {'123': ['101010100'], '456': ['101010100', '101190101']}
     ```

     其中`101010100`和`101190101`分别为北京和南京的代码

  3. 获取 key

     天气获取使用的是和风天气的 api（可免费使用），[官方教程](https://dev.qweather.com/docs/resource/get-key/)

  4. 获取区域代码

     访问下面的链接，key 为你和风天气的 key，location 为查询的城市返回数据中 id 字段即为该区域的代码
  
     ```txt
     https://geoapi.qweather.com/v2/city/lookup?location=[location]&key=[key]
     ```

     例如，key 为 xxxx，要查询的城市是 河南
  
     ```txt
     https://geoapi.qweather.com/v2/city/lookup?location=河南&key=xxxx
     ```

  5. 配置推送时间和间隔（可选）

     在`config.py`中改变下面代码的`hour`和`minute`即可改变推送时间（24 小时制）
  
     ```python
     # 天气信息推送时间
     weather_push_time = {"hour": 7, "minute": 0}
     ```
  
     在`config.py`中改变下面代码数字的值即可改变单次推送之间的间隔（单位：秒，在 48 行左右）
  
     ```python
     # 发送消息后的间隔时间
     weather_time_send = 2
     ```

  6. 配置重试次数和间隔（可选）
  
     由于网络的原因，有时获取天气信息会出现超时，于是插件更新了超时重试的功能，在`config.py`里改变下面的代码即可改变重试次数和间隔：
  
     ```python
     # 获取天气信息的最大次尝试次数
     weather_max_try = 5
     
     # 天气信息获取失败时再次尝试前的时间间隔
     weather_time_fail = 2
     ```
  
  7. 改变推送文字（可选）
  
     在`__init__.py`中改变下面代码内的内容即可改变推送文字内容
  
     ```python
     msg: Message = (MessageSegment.text('早上好！')
                     + MessageSegment.text("今天是")
                     + MessageSegment.text(weather_status.today.month + '月')
                     + MessageSegment.text(weather_status.today.day + '日，')
                     + MessageSegment.text('星期')
                     + MessageSegment.text(weather_status.today.week_day + '。')
                     + MessageSegment.text(weather_status.pos)
                     + MessageSegment.text('今天白天天气：' + weather_status.textDay + '，')
                     + MessageSegment.text('今天夜间天气：' + weather_status.textNight + '。')
                     + MessageSegment.text('最高温度' + weather_status.tempMax + '度，')
                     + MessageSegment.text('最低温度' + weather_status.tempMin + '度。')
                     + MessageSegment.text('阿狸祝大家一切顺利 (⁄ ⁄•⁄ω⁄•⁄ ⁄)'))
     ```
  
  8. 测试天气获取功能（可选）
  
     在`qweather_api.py`里第 83 行填上你的 key，就可以进行测试了
  
     ```python
     # 在这里填上你的 key
     qw_key = ''
     ```

### 4.ToDo List

- [x] 每天问早（带天气信息）
- [ ] 新人入群欢迎

### 5.特别感谢

[和风天气提供天气 api](https://dev.qweather.com/)