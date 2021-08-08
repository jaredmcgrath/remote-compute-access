#!/usr/bin/env python3
"""
Created on Wed May 26 2021

@author: jaredmcgrath
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

import signal

from local.eolib.utils.use_git import Git_Reader

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Define functions

# .....................................................................................................................

def register_waitress_shutdown_command():
    '''
    Awkward hack to get waitress server to close on SIGTERM signals
    This also greatly speeds up 'docker stop' commands!
    '''

    def convert_sigterm_to_keyboard_interrupt(signal_number, _):

        # Some feedback about catching kill signal
        print("", "", "*" * 48, "Kill signal received! ({})".format(signal_number), "*" * 48, "", sep = "\n")

        # Raise a keyboard interrupt, which waitress will respond to! (unlike SIGTERM)
        raise KeyboardInterrupt

    # Replaces SIGTERM signals with a Keyboard interrupt, which the server will handle properly
    signal.signal(signal.SIGTERM, convert_sigterm_to_keyboard_interrupt)

# .....................................................................................................................

def force_server_shutdown():
    ''' Function used to intentionally stop the server! Useful for restarting when used with docker containers '''

    os.kill(os.getpid(), signal.SIGTERM)

# .....................................................................................................................

def check_git_version():
    
    ''' Helper function used to generate versioning info to be displayed on main web page '''
    
    # Initialize output in case of errors
    is_valid = False
    version_indicator_str = "unknown"
    commit_date_str = "unknown"
    
    # Try to get versioning info    
    try:
        commit_id, commit_tags_list, commit_dt = GIT_READER.get_current_commit()
        
        # Use tag if possible to represent the version
        version_indicator_str = ""
        if len(commit_tags_list) > 0:
            version_indicator_str = ", ".join(commit_tags_list)
        else:
            version_indicator_str = commit_id
        
        # Add time information
        commit_date_str = commit_dt.strftime("%b %d")
        
        # If we get here, the info is probably good
        is_valid = True
        
    except:
        pass
    
    return is_valid, commit_date_str, version_indicator_str

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Set up globals

# Set up git repo access
GIT_READER = Git_Reader(None)

# ---------------------------------------------------------------------------------------------------------------------
#%% Scrap
