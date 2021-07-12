#!/bin/bash

# pathing
this_script_relative_path=$0
this_script_full_path=$(realpath $this_script_relative_path)
this_script_dir_path=$(dirname $this_script_full_path)
app_root_path=$this_script_dir_path/raspi-app
venv_path=$this_script_dir_path/venv

cd $app_root_path
source $venv_path/bin/activate
python3 launch.py
