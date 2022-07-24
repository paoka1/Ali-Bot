#!/bin/bash
# Program:
#	This script can start, restart or stop Ali-Bot.
# History:
#	2022/07/24	paoka1	Third release

PATH=/bin:/sbin:/usr/bin:/usr/sbin/:/usr/local/bin:/usr/local/sbin:~/bin
export PATH

# # # # # # # # # # # # # # #
# Customize configure start #
# # # # # # # # # # # # # # #

# Path & Command of nb & cq
nb_path=""
cq_path=""
nb_command=""
cq_command=""

# Path of this script
script_path=""

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

# # # # # # # # # # # # # #
# Customize configure end #
# # # # # # # # # # # # # #

# Is nb_log_folder exist
if [ ! -d "${script_path}/nb_logs" ]; then
  mkdir "${script_path}/nb_logs"
fi

# Is cq_log_folder exist
if [ ! -d "${script_path}/cq_logs" ]; then
  mkdir "${script_path}/cq_logs"
fi

# Del log file
old_log_date=$(date -d "-${log_file_max} days" "+%Y%m%d")

# Del log file of nb
cd ${nb_log_folder}
for sig_nb_log_file in `ls ${nb_log_folder}`
do
    nb_file_date=`date "+%Y%m%d" -r ${sig_nb_log_file}`
    [ ${nb_file_date} -lt ${old_log_date} ] && rm ${sig_nb_log_file} && echo -e \
    "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO]    Deleted log file: ${sig_nb_log_file}.\n\n" >> ${script_log_file}
done

# Del log file of cq
cd ${cq_log_folder}
for sig_cq_log_file in `ls ${cq_log_folder}`
do
    cq_file_date=`date "+%Y%m%d" -r ${sig_cq_log_file}`
    [ ${cq_file_date} -lt ${old_log_date} ] && rm ${sig_cq_log_file} && echo -e \
    "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO]    Deleted log file: ${sig_cq_log_file}.\n\n" >> ${script_log_file}
done

function start() {
        nb_path=${1}
        cq_path=${2}
        nb_command=${3}
        cq_command=${4}
        nb_log_file=${5}
        cq_log_file=${6}
        script_log_file=${7}

        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO]    Start to start Ali-Bot." >> ${script_log_file}

        nbs=`ps -ef | grep -n "${nb_command}" | grep -v "grep"  | awk '{print $2}'`
        # If nb is running
        if [ "${nbs}" != ""  ]; then
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Nb is running. Exited." >> ${script_log_file}
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Fail to start Ali-Bot.\n\n" >> ${script_log_file}
                echo "Fail to start Ali-Bot, See the log for more information."
                exit 1
        fi

        cqs=`ps -ef | grep -n "${cq_command}" | grep -v "grep"  | awk '{print $2}'`
        # If cq is running
        if [ "${cqs}" != ""  ]; then
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Cq is running. Exited." >> ${script_log_file}
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Fail to start Ali-Bot.\n\n" >> ${script_log_file}
                echo "Fail to start Ali-Bot, See the log for more information."
                exit 1
        fi

        # Start nb
        cd ${nb_path}
        nohup ${nb_command} >> ${nb_log_file} 2>&1 &
        sleep 1

        # If can't run cq
        nbs=`ps -ef | grep -n "${nb_command}" | grep -v "grep"  | awk '{print $2}'`
        if [ "${nbs}" == ""  ]; then
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Can't run nb. Exited." >> ${script_log_file}
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Fail to start Ali-Bot.\n\n" >> ${script_log_file}
                echo "Fail to start Ali-Bot, See the log for more information."
                exit 1
        fi
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to start nb, the PID of nb is ${nbs}." >> ${script_log_file}

        # Start cq
        cd ${cq_path}
        nohup ${cq_command} >> ${cq_log_file} 2>&1 &
        sleep 1

        # If can't run cq
        cqs=`ps -ef | grep -n "${cq_command}" | grep -v "grep"  | awk '{print $2}'`
        if [ "${cqs}" == ""  ]; then
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Can't run cq. Exited." >> ${script_log_file}
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Fail to start Ali-Bot.\n\n" >> ${script_log_file}
                echo "Fail to start Ali-Bot, See the log for more information."
                exit 1
        fi
        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to start cq, the PID of cq is ${cqs}." >> ${script_log_file}

        # Start success
        echo "Success to start Ali-Bot."
}

function stop() {
        nb_path=${1}
        cq_path=${2}
        nb_command=${3}
        cq_command=${4}
        nb_log_file=${5}
        cq_log_file=${6}
        script_log_file=${7}

        echo "[$(date "+%Y-%m-%d %H:%M:%S")] [INFO]    Start to stop Ali-Bot." >> ${script_log_file}

        nb=`ps -ef | grep -n "${nb_command}" | grep -v "grep"  | awk '{print $2}'`
        # If nb is not running
        if [ "${nb}" == ""  ]; then
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Nb is not running. Exited." >> ${script_log_file}
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Fail to stop Ali-Bot.\n\n" >> ${script_log_file}
                echo "Fail to stop Ali-Bot, See the log for more information."
                exit 1
        fi

        cq=`ps -ef | grep -n "${cq_command}" | grep -v "grep"  | awk '{print $2}'`
        # If cq is not running
        if [ "${cq}" == ""  ]; then
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Cq is not running. Exited." >> ${script_log_file}
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Fail to stop Ali-Bot.\n\n" >> ${script_log_file}
                echo "Fail to stop Ali-Bot, See the log for more information."
                exit 1
        fi

        # Try to stop nb
        kill ${nb}
        sleep 1

        # If can't stop nb
        nbj=`ps -ef | grep -n "${nb_command}" | grep -v "grep"  | awk '{print $2}'`
        if [ "${nbj}" == ""  ]; then
                echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop nb." >> ${script_log_file}
        else
                echo "[$(date "+%Y-%m-%d %H:%M:%S")] [Error]   Can't stop nb with SIGTERM, will try SIGKILL." >> ${script_log_file}
                kill -9 ${nbj}
                echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop nb." >> ${script_log_file}
        fi

        # Try to stop cq
        kill ${cq}
        sleep 1

        # If can't stop cq
        cqj=`ps -ef | grep -n "${cq_command}" | grep -v "grep"  | awk '{print $2}'`
        if [ "${cqj}" == ""  ]; then
                echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop cq." >> ${script_log_file}
        else
                echo "[$(date "+%Y-%m-%d %H:%M:%S")] [ERROR]   Can't stop cq with SIGTERM, will try SIGKILL." >> ${script_log_file}
                kill -9 ${cqj}
                echo "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop cq." >> ${script_log_file}
        fi

        # Stop success
        echo "Success to stop Ali-Bot."
}

function hhelp() {
        echo -e "\033[33mUsage: ${1} {start | stop | restart | hhelp}\033[0m"
        echo "start: Start Ali-Bot."
        echo "stop: Stop Ali-Bot."
        echo "restart: Restart Ali-Bot."
        echo "hhelp: Show this help."
}

case ${1} in
        "start")
                # Start
                echo "======== START ========" >> ${script_log_file}
                start "${nb_path}" "${cq_path}" "${nb_command}" "${cq_command}" "${nb_log_file}" "${cq_log_file}" "${script_log_file}"
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to start Ali-bot.\n\n" >> ${script_log_file}
        ;;
        "stop")
                # Stop
                echo "======== STOP ========" >> ${script_log_file}
                stop "${nb_path}" "${cq_path}" "${nb_command}" "${cq_command}" "${nb_log_file}" "${cq_log_file}" "${script_log_file}"
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to stop Ali-bot.\n\n" >> ${script_log_file}
        ;;
        "restart")
                # Restart
                echo "======== RESTART ========" >> ${script_log_file}
                stop "${nb_path}" "${cq_path}" "${nb_command}" "${cq_command}" "${nb_log_file}" "${cq_log_file}" "${script_log_file}"
                start "${nb_path}" "${cq_path}" "${nb_command}" "${cq_command}" "${nb_log_file}" "${cq_log_file}" "${script_log_file}"
                echo -e "[$(date "+%Y-%m-%d %H:%M:%S")] [SUCCESS] Success to restart Ali-bot.\n\n" >> ${script_log_file}
                echo "Success to restart Ali-Bot."
        ;;
        "hhelp")
                # Help
                hhelp "${0}"
        ;;
        *)
                echo -e "\033[33mUsage: ${0} {start | stop | restart | hhelp}\033[0m"
        ;;
esac
