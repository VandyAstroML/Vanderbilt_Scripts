#!/usr/bin/env bash

## Description: Runs the commands to run scripts
##
# Activate Environment
dirpath=eval echo "~$different_user"
echo "$(dirname $(readlink -e $dirpath))/$(basename $dirpath)"
echo "${dirpath}"

# source /home/caldervf/.bashrc
# env_name='vandyscripts'
# activate='/home/caldervf/anaconda3/envs/vandyscripts/bin/activate'
# deactivate='/home/caldervf/anaconda3/envs/vandyscripts/bin/deactivate'
# activate=`which activate`
# deactivate=`which deactivate`
# my_dir=`pwd`
# echo "pwd: ${my_dir}"
# my_dir='/home/caldervf/Repositories/Vanderbilt_Scripts'
# echo "my_dir: ${my_dir}"
# echo "source ${activate} ${env_name}"
# source ${activate} ${env_name}
# echo "${`conda env list`}"
# Run Scripts
# echo "python ${my_dir}/Astroweb_post/Astroweb_updates_xmlrpc.py >> ${my_dir}/Astroweb_post/updatelog2 2>&1"
# python ${my_dir}/Astroweb_post/Astroweb_updates_xmlrpc.py >> ${my_dir}/Astroweb_post/updatelog2 2>&1
# echo   "python ${my_dir}/AJC_Scheduler/AJC_Reminders.py >> ${my_dir}/AJC_Scheduler/ajc_log 2>&1"
# python ${my_dir}/AJC_Scheduler/AJC_Reminders.py >> ${my_dir}/AJC_Scheduler/ajc_log 2>&1
# Deactivating Environment
# echo "source ${deactivate}"
# source ${deactivate}