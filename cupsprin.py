#! /usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:31:15 2015

@author: achuth

"""

import os
import cups
import time
from ldap_login import login
from account import account
import easygui as eg
def cupsprint(username,printername,lpfile):
    conn = cups.Connection()
    filename=eg.fileopenbox("Select the file to be printed","File Selector",None)
    jobid=0
    if filename!=None :

        printer_returns = conn.getPrinters()
        cups.setUser(username)
        #for printer in printer_returns:
        #    print printer_returns.keys()[1]

    #commandline=lpfile+" -U "+username+" -d "+printername+"  "+filename
    #os.system(commandline)
        options={}
        options['sides']='two-sided-long-edge'
        try:
            jobid = conn.printFile(printername,filename,filename,options)
        except cups.IPPError as (status, description):
            eg.msgbox(title='IPP status is %d' % status, msg='Meaning: %s'% description)

        #account(username)
    return jobid

def selection ():
    msg = "Please select your choice"
    title = "LDAP Based Printer"
    choices = ["1: Take Printout", "2: See the current count","3: Quit"]
    choice = eg.choicebox(msg, title, choices)
    if choice == None:
        return 3
    else:
        return choices.index(choice)+1

