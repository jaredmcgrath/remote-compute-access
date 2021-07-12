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

import subprocess

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Network functions

def run_single_command(host, user, cmd, port=22, timeout=1):
    '''
    Runs a single command on the host. Assumes SSH access has been set up with a key for the given user
    '''

    ssh_connection_string = user + "@" + host + ":" + port
    ssh_command = ["ssh", "-o", "ConnectionTimeout=" + str(timeout), ssh_connection_string, cmd]

    conn = subprocess.Popen(ssh_command, shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

    response = conn.stdout.readlines()

    return response

# .....................................................................................................................
# .....................................................................................................................


# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
#%% Demo

if __name__ == "__main__":

    pass


# ---------------------------------------------------------------------------------------------------------------------
#%% Scrap
