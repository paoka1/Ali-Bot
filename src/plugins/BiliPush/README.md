# How To Use

### 1.功能

1. 哔哩哔哩直播推送，效果如下

   ![bili_live](../../../img/bili_live.jpg)

2. 哔哩哔哩动态推送（支持文字类动态、图片类动态、转发类动态、视频类动态），其中视频类动态效果如下：

   ![bili_dynamic](../../../img/bili_dynamic.jpg)

### 2.安装依赖

1. 安装`nonebot-plugin-apscheduler`

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

   安装完后需要进行配置：可以参考官方的 [配置方法指南](https://v2.nonebot.dev/docs/advanced/scheduler)

2. 安装 sqlite3

   安装方法取决于你使用的系统，请自行搜索安装教程并安装

### 3.使用教程

1. 哔哩哔哩直播推送使用教程

   1. 在`config.py`向`bili_live_inform_group`添加群聊和对应订阅 up 的 uid（群号是这个字典里的键，关注的 up 写成一个列表作为字典的值），例如：123 群订阅了 1 和 2，456 群订阅了 3，就可以写成如下

      ```python
      # 直播订阅群聊和阿婆主
      bili_live_inform_group = {'123': ['1', '2'], '456': ['3']}
      ```

   2. 改变`config.py`中以下的代码中的数值可改变向哔哩哔哩服务器请求间隔（可选）

      ```python
      # 请求直播状态整体间隔时间
      bili_live_time_all = 40
      # 请求直播状态单次间隔时间
      bili_live_time_get = 1
      ```

   3. 改变`config.py`中以下代码中的数值可改变单次推送间隔（可选）

      ```python
      # 发送消息后的间隔时间
      bili_live_time_send = 1
      ```

   4. 在`__init__.py`改变以下代码内容可改变推送时的文字内容（可选）

      ```python
      msg: Message = MessageSegment.text('阿婆主：' + bili_info.name) \
                     + MessageSegment.text(' 开播啦！') \
                     + MessageSegment.text(bili_info.room.title) \
                     + MessageSegment.image(bili_info.room.cover) \
                     + MessageSegment.text(bili_info.room.url.split('?')[0])
      ```

2. 哔哩哔哩动态推送使用教程

   1. 在`config.py`向`bili_dynamic_inform_group`添加群聊和对应订阅 up 的 uid（群号是这个字典里的键，关注的 up 写成一个列表作为字典的值），例如：123 群订阅了 1 和 2，456 群订阅了 3，就可以写成如下

      ```python
      # 动态订阅群聊和阿婆主
      bili_dynamic_inform_group = {'123': ['1', '2'], '456': ['3']}
      ```

   2. 在`config.py`的`db_path`设置数据库路径

      数据库由阿狸自行创建，你只需告诉阿狸数据库应该放在哪里，例如数据库放在`/home/xiaoha/mybot/`，名称为`bot.db`

      ```python
      # 数据库路径
      db_path = "/home/xiaoha/mybot/bot.db"
      ```

   3. 改变`config.py`中以下的代码中的数值可改变向哔哩哔哩服务器请求间隔（可选）

      ```python
      # 请求直播动态整体间隔时间
      bili_dynamic_time_all = 90
      # 请求动态状态单次间隔时间
      bili_dynamic_time_get = 2
      ```

   4. 改变`config.py`中以下代码中的数值可改变单次推送间隔（可选）

      ```python
      # 发送消息后的间隔时间
      bili_dynamic_time_send = 1
      ```

   5. 改变`config.py`中以下代码中的数值可改变数据库初始化时向哔哩哔哩服务器请求间隔（可选）

      ```python
      # 初始化数据库时请求动态状态单次间隔时间
      bili_dynamic_time_init_get = 1
      ```

      注：该值会影响插件加载的快慢，即 Bot 启动用时，你可以视具体情况将该值设置成较小的值。如果该值设置过大，会导致 Bot 启动所需时间较长，如果设置较小，可能会导致数据库不能正常初始化

   6. 设置动态内容裁剪（可选）

      如果你不想让长长的动态占满屏幕，那么你就可以设置下面的值，让动态被裁剪

      ```python
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
      ```

      如果动态内容超过你设置的值，阿狸会裁剪掉多余的部分，并在最后添加上`...`，如果你不需要这个功能，你可以将他们的值设置为`-1`，这样动态就不会被裁剪

   7. 在`__init__.py`改变以下代码内容可改变推送时的文字内容（可选）

      ```python
      ...
      msg: Message = MessageSegment.text("阿婆主：" + dynamic_info.get_up_name() + "于") \
                     + MessageSegment.text(dynamic_info.get_post_time() + "发布了新动态\n") \
                     + MessageSegment.text(dynamic_info.get_short_dynamic_content(
                      plugin_config.bili_dynamic_length))
      dynamic_picture_less_url_list = dynamic_info.get_dynamic_picture_less_url_list(
          plugin_config.bili_dynamic_picture_amount)
      
      if len(dynamic_picture_less_url_list) == 0:
          msg += "\n"
      
      for picture in dynamic_picture_less_url_list:
          msg += MessageSegment.image(picture)
      
      msg += MessageSegment.text(dynamic_info.get_dynamic_link())
      ...
      ```

### 4.注意事项

1. 哔哩哔哩直播推送

   在关注的 up 数量较多时，定时插件可能会有如下的一个警告，这可能会影响直播推送的准时性

   ```txt
   Execution of job "bili_live_push (trigger: interval[0:00:40], next run at: 2022-05-03 11:08:31 CST)" skipped: maximum number of running instances reached (1)
   ```

   这时可以通过增加整体的请求间隔（`bili_live_time_all`），或者减小单个请求间隔（`bili_live_time_get`）来解决

2. 哔哩哔哩动态推送

   1. 定时插件的警告

      这一点同于哔哩哔哩直播推送的定时插件的警告， 解决方法相同

   2. 如果连续发表多个动态，阿狸会从旧到新将这些动态依次推送（前提是 Bot 在运行）

   3. 在某些情况下动态不会被推送，例如在删除旧动态后立即发表了新动态，或者短时间发表了大量的动态，等等等

   4. 阿狸只支持四种动态类型（文字类动态、图片类动态、转发类动态、视频类动态），[其他动态类型](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/dynamic/get_dynamic_detail.md) 暂不支持，但仍然会推送这些动态，只不过动态内容为一律变为`「不支持的动态类型」请点击链接查看`

### 5.ToDo List

- [x] 哔哩哔哩直播推送
- [x] 哔哩哔哩直播推送差异化（给不同的群推送不同的 up 直播信息）
- [x] 哔哩哔哩动态更新推送

### 6.特别感谢

[QQBot_bilibili](https://github.com/wxz97121/QQBot_bilibili)

[QQ 机器人 牛牛](https://github.com/InvoluteHell/Pallas-Bot)

[nonebot 插件编写指南 2](https://blog.csdn.net/a1255652/article/details/118740313)

[基于 nonebot2 框架的插件编写：开播信息推送](https://kusarinoshojo.space/2022/01/18/nonebot2-python-api/)