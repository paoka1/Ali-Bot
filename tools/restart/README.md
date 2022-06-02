# Bot 重启脚本

### 1.写这个脚本的缘由

因为 Ali 有时会出现卡死的情况，为了使之稳定运行，就出现了这个重启脚本，将其添加到计划任务里，就可以定时重启 Bot，缓解了卡死的情况

### 2.如何使用

1. 在脚本里编辑以下内容

   向`SCRIPT_PATH`变量添加脚本的路径

   向`NB_PATH`变量添加 nb 的根目录路径

   向`CQ_PATH`变量添加 cq 的根目录路径

   向`NB_COMMAND`变量添加启动 nb 的命令

   向`CQ_COMMAND`变量添加启动 cq 的命令

2. 示例

   假如你的脚本放在`/home/xiaoha/mybot/Tools`，nb 根目录路径为`/home/xiaoha/mybot/xiaoha`，cq 根目录路径为`/home/xiaoha/mybot/go-cqhttp`，运行 nb 的命令为`nohup python3 bot.py &`，运行 cq 的命令为`nohup ./go-cqhttp &`，则脚本可配置为

   ```sh
   SCRIPT_PATH="/home/xiaoha/mybot/Tools"
   NB_PATH="/home/xiaoha/mybot/xiaoha"
   CQ_PATH="/home/xiaoha/mybot/go-cqhttp"
   NB_COMMAND="python3 bot.py"
   CQ_COMMAND="./go-cqhttp"

### 3.日志文件

1. `Restart.log`：记录脚本运行信息，位于脚本同目录
2. `nb.out`：记录 nb 的输出，位于脚本同目录
3. `cq.out`：记录 cq 的输出，位于脚本同目录

### 4.注意

1. 脚本重启后的 nb 和 cq 都是可以持久化运行的（即在后台运行，不受登出等因素影响）
2. 后一次运行产生的`*.out`会覆盖前一次的`*.out`，`Restart.log`会追加在上一次的`Restart.log`文件里（若文件不存在，脚本会自己创建）
3. 脚本使用`nohup [command] &`来使任务持久化运行，其他方法尚未支持
4. 脚本寻找 nb 和 cq 的 PID 是根据其启动命令来寻找的，所以启动 nb 和 cq 的命令应和脚本中的启动命令一致

### 5.关于脚本

1. 脚本写的比较匆忙，以后会慢慢进行优化
2. 由于脚本只在我的环境里测试过，其它环境可能会出现问题，若有问题，欢迎提出