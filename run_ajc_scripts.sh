#!/bin/bash

## Description: Runs the commands to run scripts
##
# Activate Environment
env_name='vandyscripts'
echo "source activate ${env_name}"
source activate ${env_name}
conda env list
# Run Scripts
# echo "python ./Astroweb_post/Astroweb_updates_xmlrpc.py >> ./Astroweb_post/updatelog2 2>&1"
# python ./Astroweb_post/Astroweb_updates_xmlrpc.py >> ./Astroweb_post/updatelog2 2>&1
# echo   "python ./AJC_Scheduler/AJC_Reminders.py >> ./AJC_Scheduler/ajc_log 2>&1"
python ./AJC_Scheduler/AJC_Reminders.py >> ./AJC_Scheduler/ajc_log 2>&1
# Deactivating Environment
source deactivate