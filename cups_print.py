#! /usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:31:15 2015

@author: achuth

"""

import cups

import easygui as eg


def cups_print(username, printer_name):
    conn = cups.Connection()
    filename = eg.fileopenbox("Select the file to be printed", "File Selector")
    job_id = 0
    if filename:

        # printer_returns = conn.getPrinters()
        cups.setUser(username)
        # for printer in printer_returns:
        #    print printer_returns.keys()[1]

        # commandline=lpfile+" -U "+username+" -d "+printer_name+"  "+filename
        # os.system(commandline)
        options = {'sides': 'two-sided-long-edge'}
        try:
            job_id = conn.printFile(printer_name, filename, filename, options)
        except cups.IPPError as (status, description):
            eg.msgbox(title='IPP status is %d' % status, msg='Meaning: %s' % description)
            # account(username)
    return job_id


def selection():
    msg = "Please select your choice"
    title = "LDAP Based Printer"
    choices = ["1: Take Printout", "2: See the current count", "3: Quit"]
    choice = eg.choicebox(msg, title, choices)
    if not choice:
        return 3
    else:
        return choices.index(choice) + 1
