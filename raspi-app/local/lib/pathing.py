#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 1 2021

@author: Jack Malloch 
"""

# ---------------------------------------------------------------------------------------------------------------------
#%% Imports

import os
import sys

# ---------------------------------------------------------------------------------------------------------------------
#%% Pathing functions

# .....................................................................................................................

def find_root_path(dunder_file = None, target_folder = "local"):
    '''
    Finds the path of the root project directory (i.e. scv2_services_classifier)
    Relies on finding the 'local' folder inside of it
    '''
    
    # Clean up dunder file pathing if needed
    try:
        dunder_file = __file__ if dunder_file is None else dunder_file
    except NameError:
        dunder_file = ""
    dunder_file = dunder_file if dunder_file else os.getcwd()
    
    # Set up starting path
    working_path = os.path.dirname(os.path.abspath(dunder_file))
    
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # Check if we're already in the root folder
    if target_folder in os.listdir(working_path):
        root_path = working_path
        return root_path
    
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # Check if the target folder is already part of the path
    
    if "/{}".format(target_folder) in working_path:
        root_path = working_path.split("/{}".format(target_folder))[0]
        return root_path
    
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # Still didn't find root folder?! Start searching towards the system root directory
    
    curr_path = working_path
    while True:
        
        # Check for the target folder in the current path
        if target_folder in os.listdir(curr_path):
            root_path = curr_path
            return root_path
        
        # Step one folder up and try again, unless we hit the root path, then stop
        old_path = curr_path
        curr_path = os.path.dirname(curr_path)
        if old_path == curr_path:
            break
    
    # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
    # Now we're in trouble. Try searching inside all the working directory folders
    
    print("Trying to find '{}' folder. Searching down path...".format(target_folder))
    for parent, dirs, files in os.walk(working_path):
        print(parent)
        print(dirs)
        print(files)
        if target_folder in dirs:
            root_path = parent
            return root_path
        
    raise FileNotFoundError("Couldn't find target folder: {}. Using: {}".format(target_folder, working_path))

# %%
