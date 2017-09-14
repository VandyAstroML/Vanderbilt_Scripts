#!/usr/bin/env bash

### --- Variables
# Home Directory
home_dir=`pwd`
# Project directory
proj_dir=`dirname $0`
# Type of OS
ostype=`uname`
echo "$ostype"
# Environment name
ENV_NAME="vandyscripts"

## Description: Runs the commands to run scripts
##
# Sourcing profile
if [[ $ostype == "Linux" ]]; then
    source $home_dir/.bashrc
    # echo "source bashrc"
else
    source $home_dir/.bashprofile
    # echo "source bashprofile"
fi
# Activating Environment
activate=`which activate`
source $activate $ENV_NAME
# cd into Script Directory
cd $proj_dir
# Run Astro Website Script
# python Astroweb_post/Astroweb_updates_xmlrpc.py >> Astroweb_post/updatelog2 2>&1
# Run AJC Script
python AJC_Scheduler/AJC_Reminders.py >> AJC_Scheduler/ajc_log 2>&1
# Deactivating Environment
deactivate=`which deactivate`
source $deactivate
# echo "$CONDA_DEFAULT_ENV"






# echo "$proj_dir"
# echo "$home_dir"
# echo "$home_dir/.bashrc"
# echo "$(which activate)"

# # Sourcing
# source $home_dir/.bashrc
# echo "$wp_username"







# Activate Environment
# source $(HOME)/.bashrc
# dirpath=eval echo "~$different_user"
# echo "directory: $(dirname $0)"
# pwd_var=`pwd`
# echo "pwd: $(pwd_var)"
# echo "$(dirname $(readlink -e $dirpath))/$(basename $dirpath)"
# echo "${dirpath}"

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