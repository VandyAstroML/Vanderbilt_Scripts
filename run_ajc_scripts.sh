#!/usr/bin/env bash

## Description: Runs the commands to run scripts
##
# Activate Environment
env_name=vandyscripts
activate=`which activate`
deactivate=`which deactivate`
my_dir=`pwd`
# echo "my_dir: ${my_dir}"
source ${activate} ${env_name}
# source activate ${env_name}
# conda env list
# Run Scripts
# echo "python ${my_dir}/Astroweb_post/Astroweb_updates_xmlrpc.py >> ${my_dir}/Astroweb_post/updatelog2 2>&1"
python ${my_dir}/Astroweb_post/Astroweb_updates_xmlrpc.py >> ${my_dir}/Astroweb_post/updatelog2 2>&1
# echo   "python ${my_dir}/AJC_Scheduler/AJC_Reminders.py >> ${my_dir}/AJC_Scheduler/ajc_log 2>&1"
python ${my_dir}/AJC_Scheduler/AJC_Reminders.py >> ${my_dir}/AJC_Scheduler/ajc_log 2>&1
# Deactivating Environment
source deactivatesource ${deactivate}