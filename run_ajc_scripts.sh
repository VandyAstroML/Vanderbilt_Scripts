#!/usr/bin/env bash

## Author: Victor Calderon

### --- Variables
# Home Directory
home_dir=`eval echo "~$different_user"`
# Project directory
proj_dir=`dirname $0`
# Type of OS
ostype=`uname`
# Environment name
ENV_NAME="vandyscripts"

## Description: Runs the commands to run scripts
##
# Sourcing profile
if [[ $ostype == "Linux" ]]; then
    source $home_dir/.bashrc
else
    source $home_dir/.bash_profile
fi
# Activating Environment
conda activate $ENV_NAME
# cd into Script Directory
cd $proj_dir
# Run AJC Script
python AJC_Scheduler/AJC_Reminders.py >> AJC_Scheduler/ajc_log 2>&1
# Run Astro Website Script
python Astroweb_post/Astroweb_updates_xmlrpc.py >> Astroweb_post/updatelog2 2>&1
# Deactivating Environment
conda deactivate
