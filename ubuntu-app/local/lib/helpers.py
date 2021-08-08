#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 8 2021

@author: Jared McGrath
"""


# ---------------------------------------------------------------------------------------------------------------------
#%% Add local path

import os
import sys

def find_path_to_local(target_folder = "local"):
    '''Finds the path to the local folder so that local imports work properly'''

    # Skip path finding if we successfully import the dummy file
    try:
        from local.dummy import dummy_func
        dummy_func()
        return
    except ImportError:
        print("", "Couldn't find local directory!", "Searching for path...", sep="\n")

    # Figure out where this file is located so we can work backwards to find the target folder
    file_directory = os.path.dirname(os.path.abspath(__file__))
    path_check = []

    # Check parent directories to see if we hit the main project directory containing the target folder
    prev_working_path = working_path = file_directory
    while True:
        # If we find the target folder in the given directory, add it to the python path (if it's not already there)
        if target_folder in os.listdir(working_path):
            if working_path not in sys.path:
                tilde_swarm = "~"*(4 + len(working_path))
                print("\n{0}\nPython path updated:\n  {1}\n{0}".format(tilde_swarm, working_path))
                sys.path.append(working_path)
            break

        # Stop if we hit the filesystem root directory (parent directory isn't changing)
        prev_working_path, working_path = working_path, os.path.dirname(working_path)
        path_check.append(prev_working_path)
        if prev_working_path == working_path:
            print("\nTried paths:", *path_check, "", sep="\n  ")
            raise ImportError("Can't find '{}' directory!".format(target_folder))

find_path_to_local()

# ---------------------------------------------------------------------------------------------------------------------
#%% Imports

import subprocess

from local.lib.environment import get_scripts_path

# ---------------------------------------------------------------------------------------------------------------------
#%% Control functions

# .....................................................................................................................


def reboot_with_os(grub_boot_number):
    '''
    Reboot the OS using the specified GRUB boot number

    0 = Ubuntu
    6 = Windows
    '''

    # Get path to scripts folder
    scripts_path = get_scripts_path()
    # Make the path to reboot_os.sh
    reboot_script_path = os.path.join(scripts_path, "reboot_os.sh")
    # USe bash to run the script with the appropriate arg
    command = ["bash", reboot_script_path, "-i", str(grub_boot_number)]

    result = subprocess.run(command, capture_output=True, text=True)

    # Hopefully we don't make it past here. This should run & cause Ubuntu to reboot

    # result.stdout will be a string separated with '\n'
    # Parse this by splitting and returning an array
    result_arr = result.stdout.split("\n")

    return {"result": result_arr}

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Demo

if __name__ == "__main__":
    print("Main of helpers.py")


# ---------------------------------------------------------------------------------------------------------------------
#%% Scrap
