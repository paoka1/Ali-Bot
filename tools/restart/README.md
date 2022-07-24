# Bot 重启脚本

### 1.使用脚本

**脚本功能：**重启、运行、停止 Bot，按日期管理日志

**使用命令：**

```shell
# 启动 Bot
./restart.sh start
# 重启 Bot
./restart.sh restart
# 停止 Bot
./restart.sh stop
# 显示帮助
./restart.sh hhelp
```

*可以手动使用，也可以把脚本启动命令放到定时任务`crontab`中来定时重启，或者放在`git hooks`里实现更新自动部署*

**历史版本：**

上一个版本：[README.md](old-README.md)、[old-restart.sh](old-restart.sh)

现在的版本：[README.md](README.md)、[restart.sh](restart.sh)

### 2.配置脚本

可配置的内容在 15 行到 35 行，配置说明如下：

1. **脚本基本配置**

   向`nb_path`变量添加 nb 的根目录路径

   向`cq_path`变量添加 cq 的根目录路径

   向`nb_command`变量添加启动 nb 的命令（在 nb 根目录下的运行命令）

   向`cq_command`变量添加启动 cq 的命令（在 cq 根目录下的运行命令）

   向`script_path`变量添加重启脚本的路径

   向`log_file_max`变量添加想保留的日志数量

2. **日志文件配置（可选配置）**

   `nb_log_folder`：nb 日志存放目录

   `cq_log_folder`：cq 日志存放目录

   `nb_log_file`：nb 日志文件名

   `cq_log_file`：cq 日志文件名

   `script_log_file`：脚本日志文件名

3. **配置实例**

   假如你的脚本放在`/home/xiaoha/mybot/Tools`，nb 根目录路径为`/home/xiaoha/mybot/xiaoha`，cq 根目录路径为`/home/xiaoha/mybot/go-cqhttp`，运行 nb 的命令为`nohup python3 bot.py &`，运行 cq 的命令为`nohup ./go-cqhttp &`，nb、cq 想保留的文件数量为 5，则脚本配置如下

   ```sh
   nb_path="/home/xiaoha/mybot/xiaoha"
   cq_path="/home/xiaoha/mybot/go-cqhttp"
   nb_command="python3 bot.py"
   cq_command="./go-cqhttp"
   
   # Path of this script
   script_path="/home/xiaoha/mybot/Tools"
   
   # Maximum number of logs to save
   log_file_max=5
   
   # Log folder of nb & cq
   nb_log_folder="${script_path}/nb_logs"
   cq_log_folder="${script_path}/cq_logs"
   
   # Log file of nb & cq
   nb_log_file="${nb_log_folder}/nb_$(date "+%Y_%m_%d").out"
   cq_log_file="${cq_log_folder}/cq_$(date "+%Y_%m_%d").out"
   
   # Log file of this script
   script_log_file="${script_path}/log_restart.log"
   ```

4. **注意事项**

   1. 脚本只测试过使用`python3 bot.py`启动 nb 的情况，对使用`nb run`或者其他命令启动的情况脚本能否正常工作是未知的
   2. 脚本重启后的 nb 和 cq 都是可以持久化运行的（脚本使用`nohup [command] &`来实现）
   3. 脚本寻找 nb 和 cq 的 PID 是根据其启动命令来寻找的
   4. 当 nb 或 cq 中有一个或都在运行时，启动 Bot 会失败
   5. 当 nb 或 cq 中有一个或都不在运行时，停止 Bot 会失败
   6. 重启 Bot 是由停止、启动 Bot 两个步骤组成的，停止、重启失败时，重启会失败

### 3.日志文件

按照默认配置，脚本的日志是这样分布的：

```tree
.
├── cq_logs
│   ├── cq_2022_07_22.out
│   ├── cq_2022_07_23.out
│   └── cq_2022_07_24.out
├── nb_logs
│   ├── nb_2022_07_22.out
│   ├── nb_2022_07_23.out
│   └── nb_2022_07_24.out
├── log_restart.log
└── restart.sh
```

脚本的日志会追加在`log_restart.log`，nb、cq 输出会按日期放在 nb_logs 和 cq_logs 下，同一天的会追加到同一个文件内，不同日期的会记录在新的文件内，会按照配置删除日志文件

**注意事项：**

运行脚本时脚本才会检查删除多余的日志，所以实际上日志存在的数量并不等于配置的日志保留数量，另外，脚本通过日志最后修改的时间来判断是否要删除日志，所以可能出现应该要删除的日志没有删除的问题

所以建议将脚本的重启命令加入`crontab`，每天重启 Bot，这样问题就解决了（否则你要定期检查日志文件，防止它占用不必要的空间），步骤如下：

1. 命令行输入`crontab -e`

2. 选择你喜欢的编辑器

3. 添加如下的内容（假如本脚本路径为`/home/xiaoha/mybot/Tools`）

   ```sh
   0 0 * * * /bin/bash -c "/home/xiaoha/mybot/Tools/restart.sh restart"
   ```

4. 保存退出

实际上的日志数量和配置的日志数量有出入是正常的，你可以通过实际情况来不断重新设置配置的日志数量
