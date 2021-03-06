# How To Use

### 1.功能

哔哩哔哩直播推送，效果如下

![bili_live](../../../img/bili_live.jpg)


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

安装完后需要进行配置：可以参考官方的 [配置方法指南](https://v2.nonebot.dev/docs/advanced/scheduler)

### 3.使用教程

1. 在`config.py`向`bili_live_inform_group`添加群聊和对应订阅 up 的 uid（群号是这个字典里的键，关注的 up 写成一个列表作为字典的值）

2. 例如：123 群订阅了 1 和 2，456 群订阅了 3，就可以写成如下

   ```python
   # 订阅群聊和阿婆主
   bili_live_inform_group = {'123': ['1', '2'], '456': ['3']}
   ```

3. 改变`config.py`中以下的代码中的数值可改变向哔哩哔哩服务器请求间隔（可选）

   ```python
   # 请求直播状态整体间隔时间
   bili_live_time_all = 40
   # 请求直播状态整体单次时间
   bili_live_time_get = 1
   ```

4. 改变`config.py`中以下代码中的数值可改变单次推送间隔（可选）

   ```python
   # 发送消息后的间隔时间
   bili_live_time_send = 1
   ```

5. 在`__init__.py`改变以下代码内容可改变推送时的文字内容（可选）

   ```python
   msg: Message = MessageSegment.text('阿婆主：' + bili_info.name) \
                  + MessageSegment.text(' 开播啦！') \
                  + MessageSegment.text(bili_info.room.title) \
                  + MessageSegment.image(bili_info.room.cover) \
                  + MessageSegment.text(bili_info.room.url.split('?')[0])
   ```

### 4.注意事项

在关注的 up 数量较多时，定时插件可能会有如下的一个警告，这可能会影响直播推送的准时性

```txt
Execution of job "push_bili (trigger: interval[0:00:40], next run at: 2022-05-03 11:08:31 CST)" skipped: maximum number of running instances reached (1)
```

这时可以通过增加整体的请求间隔（`bili_live_time_all`），或者减小单个请求间隔（`bili_live_time_get`）来解决

### 5.ToDo List

- [x] 哔哩哔哩直播推送
- [x] 哔哩哔哩直播推送差异化（给不同的群推送不同的 up 直播信息）
- [ ] 哔哩哔哩动态更新推送

### 6.参考链接

[QQ 机器人 牛牛](https://github.com/InvoluteHell/Pallas-Bot)

[nonebot 插件编写指南 2](https://blog.csdn.net/a1255652/article/details/118740313)

[基于 nonebot2 框架的插件编写：开播信息推送](https://kusarinoshojo.space/2022/01/18/nonebot2-python-api/)