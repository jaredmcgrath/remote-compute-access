#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 1 2021

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

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Environment

# .....................................................................................................................

def get_service_protocol():
    """Returns SERVICE_PROTOCOL (protocol of service) if set, or \'http\'"""
    return os.environ.get("SERVICE_PROTOCOL", "http")

# .....................................................................................................................

def get_service_host():
    """Returns SERVICE_HOST (host address of service) if set, or \'0.0.0.0\'"""
    return os.environ.get("SERVICE_HOST", "0.0.0.0")

# .....................................................................................................................

def get_service_port():
    """Returns SERVICE_PORT (port of service) if set, or \'6969\'"""
    return int(os.environ.get("SERVICE_PORT", 6969))

def get_scripts_path():
    """Returns RASPI_APP_LAUNCH_PATH-based path to the scripts directory, or defaults to \'\'"""
    launch_path = os.environ.get("RASPI_APP_LAUNCH_PATH", "/home/jared/remote-compute-access/ubuntu-app/launch.py")
    ubuntu_app_root = os.path.dirname(launch_path)
    scripts_path = os.path.join(ubuntu_app_root, "scripts")
    return scripts_path

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Control functions

# .....................................................................................................................

def get_debugmode():
    """Returns DEBUG_MODE (bool of the service in debug mode). Defaults to True"""
    return bool(int(os.environ.get("DEBUG_MODE", 1)))

# .....................................................................................................................
# .....................................................................................................................


# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#%% Demo

if __name__ == "__main__":

    # Print out environment variables for quick checks
    print("")
    print("SERVICE_DEBUG:", get_debugmode())
    print("")
    print("SERVICE_PROTOCOL:", get_service_protocol())
    print("SERVICE_HOST:", get_service_host())
    print("SERVICE_PORT:", get_service_port())
    print("")


# ---------------------------------------------------------------------------------------------------------------------
#%% Scrap
