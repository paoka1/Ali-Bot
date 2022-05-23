#!/bin/bash
# Program:
#	This script will restart Ali-Bot.
# History:
#	2022/05/23	paoka1	First release

PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:~/.local/bin:~/bin
export PATH

SCRIPT_PATH=""
NB_PATH=""
CQ_PATH=""
NB_COMMAND=""
CQ_COMMAND=""

cd ${SCRIPT_PATH}
echo "===***** RESTART *****===" >> Restart.log
echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO]    Start to restart Ali-Bot." >> Restart.log

# Find out the PID of the `${NB_COMMAND}`
nb=`ps -ef | grep -n "${NB_COMMAND}" | grep -v "grep"  | awk '{print $2}'`
if [ "${nb}" == ""  ]; then
	echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Nb is not running. Exited.\n\n\n" >> Restart.log
	exit 1
fi
echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] The PID of nb is ${nb}." >> Restart.log

# Find out the PID of the `${CQ_COMMAND}`
cq=`ps -ef | grep -n "${CQ_COMMAND}" | grep -v "grep"  | awk '{print $2}'`
if [ "${cq}" == ""  ]; then
        echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Cq is not running. Exited.\n\n\n" >> Restart.log
        exit 1
fi
echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] The PID of cq is ${cq}." >> Restart.log

# Try to stop nb
kill ${nb}

# If can't stop nb
nbj=`ps -ef | grep -n "${NB_COMMAND}" | grep -v "grep"  | awk '{print $2}'`
if [ "${nbj}" == ""  ]; then
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop nb." >> Restart.log
else
	echo "[$(date "+%Y-%m-%d %H:%M:%S")] [Error]   Can't stop nb with SIGTERM, will try SIGKILL." >> Restart.log
	kill -9 ${nbj}
	echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop nb." >> Restart.log
fi

# Try to stop cq
kill ${cq}

# If can't stop cq
cqj=`ps -ef | grep -n "${CQ_COMMAND}" | grep -v "grep"  | awk '{print $2}'`
if [ "${cqj}" == ""  ]; then
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop cq." >> Restart.log
else
	echo "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Can't stop cq with SIGTERM, will try SIGKILL." >> Restart.log
        kill -9 ${cqj}
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop cq." >> Restart.log
fi

# Restart nb
cd ${NB_PATH}
NB_LOG=${SCRIPT_PATH}"/nb.out"
nohup ${NB_COMMAND} >${NB_LOG} 2>&1 &
cd -

# If can't run nb
nbs=`ps -ef | grep -n "${NB_COMMAND}" | grep -v "grep"  | awk '{print $2}'`
if [ "${nbs}" == ""  ]; then
        echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Can't run nb. Exited.\n\n\n" >> Restart.log
        exit 1
fi
echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to restart nb, the PID of nb is ${nbs}." >> Restart.log

# Restart cq
cd ${CQ_PATH}
CQ_LOG=${SCRIPT_PATH}"/cq.out"
nohup ${CQ_COMMAND} >${CQ_LOG} 2>&1 &
cd -

# If can't run cq
cqs=`ps -ef | grep -n "${CQ_COMMAND}" | grep -v "grep"  | awk '{print $2}'`
if [ "${cqs}" == ""  ]; then
        echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Can't run cq. Exited.\n\n\n" >> Restart.log
        exit 1
fi
echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to restart cq, the PID of cq is ${cqs}." >> Restart.log

# If success
echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to restart Ali-Bot.\n\n\n" >> Restart.log
exit 0
