#! /usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:31:15 2015

@author: achuth

This is the main script for the LDAP based Printer Solution to be used in IITB
All the other necessary functions are imported to this script and are called
when desired.

"""
import cups
import time
import sys
import ConfigParser
import easygui as eg
import os

from oauth.sso_login import login
from print_pkg.account import account
from print_pkg.cups_print import selection
from print_pkg.cups_print import cups_print
from oauth.exceptions import OAuthError
from utils.colors import RED, GREEN, NATIVE
from socket import error as socket_error

def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))
config = ConfigParser.ConfigParser()
config.read(get_abs_path("config/printer.cfg"))
lp_file = config.get('printer','lpfile')
printer_name = config.get('printer','name')
try:
    username, login_status = login()
except (OAuthError, ValueError, socket_error) as err:
    msg = 'Unable to Authenticate. \nError: %s\n' % err.message
    sys.stderr.write(RED + msg + NATIVE)
    sys.stderr.flush()
    sys.exit()

sys.stdout.write(GREEN + 'Authentication Successful\n' + NATIVE)
sys.stdout.flush()

if login_status:
    choice = selection()
    while choice != 3:
        if choice == 1:
            job_id = cups_print(username, printer_name)
        if choice == 2:
            eg.msgbox('Total number of pages printed = %s' % account(username), 'Total Printed Pages')
        choice = selection()

    conn = cups.Connection()
    while conn.getJobs(my_jobs=True):
        time.sleep(1)
    eg.msgbox('Total number of pages printed = %s' % account(username), 'Total Printed Pages')

else:
    print 'Login failed. Please try again later'

sys.exit()
