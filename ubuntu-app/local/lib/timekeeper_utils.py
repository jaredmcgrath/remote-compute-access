#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 15:15:26 2020

@author: eo
"""


# ---------------------------------------------------------------------------------------------------------------------
#%% Imports

import time
import datetime as dt


# ---------------------------------------------------------------------------------------------------------------------
#%% General functions

# .....................................................................................................................
    
def get_utc_datetime():

    ''' Returns a datetime object based on UTC time, with timezone information included '''

    return dt.datetime.utcnow().replace(tzinfo = get_utc_tzinfo())
    
# .....................................................................................................................
    
def get_local_datetime():

    ''' Returns a datetime object based on the local time, with timezone information included '''

    return dt.datetime.now(tz = get_local_tzinfo())

# .....................................................................................................................

def get_local_tzinfo():
    
    ''' Function which returns a local tzinfo object. Accounts for daylight savings '''
    
    # Figure out utc offset for local time, accounting for daylight savings
    is_daylight_savings = time.localtime().tm_isdst
    utc_offset_sec = time.altzone if is_daylight_savings else time.timezone
    utc_offset_delta = dt.timedelta(seconds = -utc_offset_sec)
    
    return dt.timezone(offset = utc_offset_delta)
    
# .....................................................................................................................

def get_utc_tzinfo():
    
    ''' Convenience function which returns a utc tzinfo object '''
    
    return dt.timezone.utc

# .....................................................................................................................

def get_current_ems():
    
    ''' Convenience function which gets the local datetime and converts it to an epoch ms value '''
    
    curr_dt = get_local_datetime()
    curr_ems = datetime_to_epoch_ms(curr_dt)
    
    return curr_ems

# .....................................................................................................................
# .....................................................................................................................


# ---------------------------------------------------------------------------------------------------------------------
#%% Reporting functions

# .....................................................................................................................

def timestamped_log(message):
    
    # Get current time
    locat_dt = get_local_datetime()
    timestamp_str = datetime_to_human_readable_string(locat_dt)
    
    # Prefix message with timestamp
    print_str =  "{}  |  {}".format(timestamp_str, message)
    
    return print_str

# .....................................................................................................................
# .....................................................................................................................

# ---------------------------------------------------------------------------------------------------------------------
#%% Datetime conversion functions

# .....................................................................................................................

def datetime_to_human_readable_string(input_datetime):
    
    '''
    Converts a datetime object into a 'human friendly' string
    Example:
        "2019-01-30 05:11:33 PM (-0400 UTC)"
    
    Note: This function assumes the datetime object has timezone information (tzinfo)
    '''
    
    return input_datetime.strftime("%Y-%m-%d %I:%M:%S %p (%z UTC)")

# .....................................................................................................................

def datetime_to_isoformat_string(input_datetime):
    
    '''
    Converts a datetime object into an isoformat string
    Example:
        "2019-01-30T11:22:33+00:00.000000"
    
    Note: This function assumes the datetime object has timezone information (tzinfo)
    '''
    
    return input_datetime.isoformat()

# .....................................................................................................................

def datetime_to_epoch_ms(input_datetime):
    
    ''' Function which converts a datetime to the number of milliseconds since the 'epoch' (~ Jan 1970) '''
    
    return int(round(1000 * input_datetime.timestamp()))

# .....................................................................................................................

def datetime_convert_to_day_start(input_datetime):
    
    ''' Function which takes in a datetime and returns a datetime as of the start of that day '''
    
    return input_datetime.replace(hour = 0, minute = 0, second = 0, microsecond = 0)

# .....................................................................................................................

def datetime_convert_to_day_end(input_datetime):
    
    ''' Function which takes in a datetime and returns a datetime as of the end of that day (minus 1 second) '''
    
    return input_datetime.replace(hour = 23, minute = 59, second = 59, microsecond = 0)

# .....................................................................................................................

def local_datetime_to_utc_datetime(local_datetime):
    
    ''' Convenience function for converting datetime objects from local timezones to utc '''
    
    return (local_datetime - local_datetime.utcoffset()).replace(tzinfo = get_utc_tzinfo())

# .....................................................................................................................
# .....................................................................................................................

# .....................................................................................................................

def epoch_ms_to_local_datetime(epoch_ms):
    
    ''' Function which converts a millisecond epoch value into a datetime object with the local timezone '''
    
    epoch_sec = epoch_ms / 1000.0
    return dt.datetime.fromtimestamp(epoch_sec).replace(tzinfo = get_local_tzinfo())

# .....................................................................................................................

def epoch_ms_to_image_folder_names(epoch_ms):
    
    '''
    Helper function used to provided consistent folder naming, based on input epoch_ms times
    Returns:
        date_folder_name, hour_folder_name
    '''
    
    # Convert provided epoch_ms value into a datetime, so we can create date + hour folder names from it
    target_time_dt = epoch_ms_to_local_datetime(epoch_ms)
    date_name = target_time_dt.strftime(DATE_FORMAT)
    hour_name = target_time_dt.strftime(HOUR_FORMAT)
    
    return date_name, hour_name

# .....................................................................................................................

#%% Global setup

# Set string formatting globally, so it can be applied consistently wherever possible
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
HOUR_FORMAT = "%H"

# ---------------------------------------------------------------------------------------------------------------------
#%% Demo

if __name__ == "__main__":
    pass


# ---------------------------------------------------------------------------------------------------------------------
#%% Scrap

