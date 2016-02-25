#! /usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:31:15 2015

@author: achuth

This is the main script for the LDAP based Printer Solution to be used in IITB
All the other necessary functions are imported to this script and are called
when desired.

"""
import sys
import ConfigParser
import easygui as eg
import os

from oauth.sso_login import login
from print_pkg.account import account
from print_pkg.cups_print import selection
from print_pkg.cups_print import cups_print
from oauth.exceptions import OAuthError
from utils import PROJECT_ROOT
from utils.colors import RED, GREEN, NATIVE
from socket import error as socket_error


config = ConfigParser.ConfigParser()
config.read(os.path.join(PROJECT_ROOT, "config/printer.cfg"))
printer_name = config.get('printer', 'name')

try:
    username, login_status = login()
except (OAuthError, ValueError, socket_error) as err:
    msg = 'Unable to Authenticate. \nError: %s\n' % err.message
    sys.stderr.write(RED + msg + NATIVE)
    sys.stderr.flush()
    sys.exit()

if login_status:
    sys.stdout.write(GREEN + 'Authentication Successful\n' + NATIVE)
    sys.stdout.flush()

    choice = selection()
    while choice != 3:
        if choice == 1:
            job_id = cups_print(username, printer_name)
        if choice == 2:
            total_pages, _, _ = account(username)
            eg.msgbox('Total number of pages printed in current month = %s' % total_pages, 'Total Printed Pages')
        choice = selection()

else:
    print('Login failed. Please try again later')

sys.exit()
