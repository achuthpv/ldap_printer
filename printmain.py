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

import easygui as eg

from oauth.sso_login import login
from account import account
from cups_print import selection
from cups_print import cups_print

lp_file = "lp"
printer_name = "PDF"
username, login_status = login()

if login_status:
    choice = selection()
    while choice != 3:
        if choice == 1:
            jobid = cups_print(username, printer_name)
        if choice == 2:
            eg.msgbox('Total number of pages printed = %s' % account(username), 'Total Printed Pages')
        choice = selection()

    conn = cups.Connection()
    # while conn.getJobs().get(jobid, None) is not None:
    # waiting for all the jobs of the current user to get finished
    while conn.getJobs():
        time.sleep(1)
    eg.msgbox('Total number of pages printed = %s' % account(username), 'Total Printed Pages')

else:
    print 'Login failed. Please try again later'
