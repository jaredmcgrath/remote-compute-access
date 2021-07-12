#!/bin/sh

if [[ -z "${RASPI_APP_ROOT_PATH}" ]]; then
  this_script_relative_path=$0
  this_script_full_path=$(realpath $this_script_relative_path)
  this_script_dir_path=$(dirname $this_script_full_path)
  app_root_path=$this_script_dir_path/raspi-app
else
  app_root_path=$RASPI_APP_ROOT_PATH
fi

if [[ -z "${RASPI_APP_VENV_PATH}" ]]; then
  this_script_relative_path=$0
  this_script_full_path=$(realpath $this_script_relative_path)
  this_script_dir_path=$(dirname $this_script_full_path)
  venv_root_path=$this_script_dir_path/venv
else
  venv_root_path=$RASPI_APP_VENV_PATH
fi

venv_path=$venv_root_path/bin/activate
launch_path=$app_root_path/launch.py

source $venv_path
python3 $launch_path
