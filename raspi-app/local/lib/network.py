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

import platform
import subprocess

import requests

from local.lib.environment import get_remote_host, get_remote_web_port

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Network functions

def ping_machine(host, timeout=100):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', '-c', '1', '-w', str(round(timeout / 1000)), host]

    try:
        is_online = subprocess.call(command, timeout=timeout / 1000) == 0
    except subprocess.TimeoutExpired:
        is_online = False

    return is_online

# .....................................................................................................................

def nmap_host_info(host):
    if platform.system().lower()=='windows':
        return {"error": "cannot run nmap on windows"}
    else:
        command = ["nmap", "-O", "-sV", host]

        result = subprocess.run(command, capture_output=True, text=True)

        # result.stdout will be a string separated with '\n'
        # Parse this by splitting and returning an array
        result_arr = result.stdout.split("\n")

        return {"result": result_arr}

# .....................................................................................................................

def reboot_desktop_to_os(os_select):
    '''
    Reboots the desktop PC with a specified OS.

    os_select: "windows" | "ubuntu"
    '''

    remote_web_base = "http://" + get_remote_host() + ":" + get_remote_web_port()
    req_url = remote_web_base + "/reboot-with-os/" + os_select

    try:
        http_response = requests.get(req_url)
        response = http_response.json()
    # If we error (e.g. from no response from the remote, )
    except (requests.exceptions.ConnectionError):
        response = {"result": "success with error"}
    
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
