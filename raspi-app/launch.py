#!/usr/bin/env python3
"""
Created on Fri May 28 2021

@author: Jared McGrath
"""

# ---------------------------------------------------------------------------------------------------------------------
# %% Imports
from flask import Flask
from flask_cors import CORS

from waitress import serve as wsgi_serve

from wakeonlan import send_magic_packet
from local.lib.network import nmap_host_info, ping_machine, reboot_desktop_to_os
from local.lib.response_helpers import json_response

from local.lib.server_helpers import check_git_version, register_waitress_shutdown_command
from local.lib.environment import get_remote_host, get_remote_mac, get_remote_ssh_port, get_service_host, get_service_protocol, get_service_port, get_debugmode
# ---------------------------------------------------------------------------------------------------------------------
# %% Create main routes

# Create wsgi app so we can start adding routes
wsgi_app = Flask(__name__)
CORS(wsgi_app)

# .....................................................................................................................


@wsgi_app.route("/")
def home_route():
    '''Home route that serves a home page of some sort'''

    # For convenience
    def indent_by_2(message): return "  {}".format(message)

    # Generate versioning info
    version_is_valid, version_date_str, version_id_str = check_git_version()
    bad_version_entry = "<p>error getting version info!</p>"
    good_version_entry = "<p>version: {} ({})</p>".format(
        version_id_str, version_date_str)
    git_version_str = (
        good_version_entry if version_is_valid else bad_version_entry)

    # Build html line-by-line
    html_list = ["<!DOCTYPE html>",
                 "<html>",
                 "<head>",
                 indent_by_2("<title>Raspberry Pi Gateway</title>"),
                 indent_by_2(
                     "<link rel='icon' href='data:;base64,iVBORw0KGgo='>"),
                 "</head>",
                 "<body>",
                 indent_by_2(
                     "<h1>Info: <a href='/help'>Route listing</a></h1>"),
                 indent_by_2(git_version_str),
                 "</body>",
                 "</html>"]

    return "\n".join(html_list)

# .....................................................................................................................


@wsgi_app.route("/help")
def help_route():

    # Initialize output html listing
    html_strs = ["<title>Access Help</title>", "<h1>Route List:</h1>"]

    # Get valid methods to print
    valid_methods = ("GET", "POST")
    def check_methods(method): return method in valid_methods

    url_list = []
    html_entry_list = []
    for each_route in wsgi_app.url_map.iter_rules():

        # Ignore the static path
        if "static" in each_route.rule:
            continue

        # Get route urls (for sorting)
        each_url = each_route.rule
        url_list.append(each_url)

        # Clean up url and get GET/POST listing
        cleaned_url = each_url.replace("<", " (").replace(">", ") ")
        method_str = ", ".join(filter(check_methods, each_route.methods))

        # Generate a inactive/active link versions of the url
        method_html = "<b>[{}]</b>&nbsp;&nbsp;&nbsp;".format(method_str)
        dead_html_entry = "<p>{}{}</p>".format(method_html, cleaned_url)
        link_html_entry = "<p>{}<a href={}>{}</a></p>".format(
            method_html, cleaned_url, cleaned_url)

        # Decide which style url to present
        show_as_dead = ("(" in cleaned_url) or (
            cleaned_url == "/help") or (cleaned_url == "/")
        add_html_entry = dead_html_entry if show_as_dead else link_html_entry
        html_entry_list.append(add_html_entry)

    # Alphabetically sort url listings (so they group nicely) then add to html
    _, sorted_html_entries = zip(*sorted(zip(url_list, html_entry_list)))
    html_strs += sorted_html_entries

    return "\n".join(html_strs)

# .....................................................................................................................

@wsgi_app.route("/bring-online")
def bring_online_route():
    '''
    Brings the machine online
    '''

    send_magic_packet(REMOTE_MAC)

    return json_response({"success": "magic packet sent"})

# .....................................................................................................................

@wsgi_app.route("/check-online")
@wsgi_app.route("/check-online/<int:timeout_ms>")
def check_online_route(timeout_ms=100):
    '''
    Checks if the machine is online
    '''

    is_online = ping_machine(REMOTE_HOST, timeout_ms)

    return json_response({"is_online": is_online})

# .....................................................................................................................

@wsgi_app.route("/get-host-info")
def get_host_info_route():
    '''
    Runs an nmap to query the host info
    '''

    result = nmap_host_info(REMOTE_HOST)

    return json_response(result)

# .....................................................................................................................

@wsgi_app.route("/get-current-os")
def get_current_os():
    '''
    Gets the current operating system
    '''

    result = nmap_host_info(REMOTE_HOST)

    return json_response(result)

# .....................................................................................................................

@wsgi_app.route("/set-current-os/<string:os_select>")
def get_current_os(os_select):
    '''
    Sets the current operating system
    '''

    result = reboot_desktop_to_os(os_select)

    return json_response(result)


# ---------------------------------------------------------------------------------------------------------------------
# %% Configure globals

REMOTE_HOST = get_remote_host()
REMOTE_SSH_PORT = get_remote_ssh_port()
REMOTE_MAC = get_remote_mac()


# ---------------------------------------------------------------------------------------------------------------------
# %% *** Launch server ***

if __name__ == "__main__":

    # Set server access parameters
    service_protocol = get_service_protocol()
    service_host = get_service_host()
    service_port = get_service_port()
    SERVER_URL = "{}://{}:{}".format(service_protocol,
                                     service_host, service_port)

    # Launch wsgi server
    print("")
    enable_debug_mode = get_debugmode()
    if enable_debug_mode:
        # Launch server using flask built-in debugging server
        wsgi_app.run(service_host, port=service_port, debug=True)
    else:
        # Launch server using waitress
        register_waitress_shutdown_command()
        wsgi_serve(wsgi_app, host=service_host,
                   port=service_port, url_scheme=service_protocol)

    # Feedback in case we get here
    print("Done! Closing server...")


# ---------------------------------------------------------------------------------------------------------------------
# %% Scrap
