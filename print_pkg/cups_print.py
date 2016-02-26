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
    title = "Filename : " + filename
    msg = "empty - print all pages, '-' for range, ',' separate ranges)"

    field_names = ["Pages to be printed"]
    field_values = []  # we start with blanks for the values
    field_values = eg.multenterbox(msg, title, field_names, field_values)

    job_id = 0
    if filename:
        cups.setUser(username)
        options = {'sides': 'two-sided-long-edge'}
        val = str(field_values[0]).replace(" ", "").strip(',')
        if bool(val):
            options['page-ranges'] = val

        try:
            conn.setPrinterUsersAllowed(printer_name, [username])
            job_id = conn.printFile(printer_name, filename, filename, options)
            conn.setPrinterUsersAllowed(printer_name, ['root'])
        except cups.IPPError as (status, description):
            eg.msgbox(title='IPP status is %d' % status, msg='Meaning: %s' % description)
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
