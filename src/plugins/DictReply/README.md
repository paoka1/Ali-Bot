# How To Use

### 1.插件功能

这个插件的功能是利用预先设置的字典，对消息进行回复（非关键词判断）

### 2.使用教程

1. 向`config.py`里的`reply_dic`添加键值，就可以回复了

2. 例如，想让 Bot 在收到 早安，晚安 时发送 早上好，晚上好 就可以写成下面这样：

   ```python
   reply_dic = {'早安': '早上好',
               '晚安': '晚上好'}
   ```

### 3.注意事项

1. 字典内的键不要重复

2. 在事件响应器中添加`block=False`（默认值 True），可让优先级位于本插件之后的插件继续处理消息

   ```python
   reply = on_message(priority=8, block=False)
   ```

   