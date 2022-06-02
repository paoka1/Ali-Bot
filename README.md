# Ali-Bot

阿狸（Ali）是一个正在成长的 QQ Bot

## 如何使用：

插件目录：`src\plugins`

工具目录：`tools`

Ali 正处于开发阶段，所以其插件有很多不完善的地方，如果想使用更优秀的插件，可以参考：

1. [官方插件商店](https://v2.nonebot.dev/store)
2. [Pallas Bot](https://github.com/InvoluteHell/Pallas-Bot)
3. [真寻 Bot](https://github.com/HibiKier/zhenxun_bot)

如果想从头开始创建 Bot，可参考：

1. Windows 下搭建教程：[新-基于 Nonebot2 和 go-cqhttp 的机器人搭建](https://yzyyz.top/archives/nb2b1.html)

2. 若要在 Linux 下部署教程：[Linux 端部署 nonebot2](https://blog.csdn.net/realttr/article/details/122238677)


## Ali 的功能

1. 基本的发消息功能（关键语句、关键字回复、图片回复，都是预定好的）

2. 随机 +1 和随机回复消息（回复的消息是预定的）

3. 哔哩哔哩直播推送，效果如下

   ![bili_live](/img/bili_live.jpg)

4. 每天问早（外加当天天气信息），效果如下

   ![weather](/img/hw_greeting.jpg)

## ToDo List

- [x] [关键句](https://github.com/paoka1/Ali-Bot/tree/main/src/plugins/DictReply)，[关键词消息回复](https://github.com/paoka1/Ali-Bot/tree/main/src/plugins/KeyReply)
- [x] [回复图片类型的消息](https://github.com/paoka1/Ali-Bot/tree/main/src/plugins/SendImage)
- [x] [哔哩哔哩直播推送](https://github.com/paoka1/Ali-Bot/tree/main/src/plugins/Push)
- [x] [成为复读机（完善中）](https://github.com/paoka1/Ali-Bot/tree/main/src/plugins/Repeater)
- [x] [每天问好功能（完善中）](https://github.com/paoka1/Ali-Bot/tree/main/src/plugins/Greeting)
- [ ] CVE 更新推送
- [ ] 自主从聊天中学习
- [ ] 统治人类（bushi

## 官方文档链接

[nonebot 官方文档](https://v2.nonebot.dev/)

[go-cqhttp 官方文档](https://docs.go-cqhttp.org/)

## 配置参考链接

[新-基于 Nonebot2 和 go-cqhttp 的机器人搭建](https://yzyyz.top/archives/nb2b1.html)

[Linux 端部署 nonebot2](https://blog.csdn.net/realttr/article/details/122238677)

## 致谢

[开源项目：跨平台 Python 异步机器人框架 nonebot](https://github.com/nonebot/nonebot2)

[开源项目：cqhttp 使用 golong 的实现 go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

[开源项目：Pallas-Bot](https://github.com/InvoluteHell/Pallas-Bot)
