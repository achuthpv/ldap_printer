#! /usr/bin/python

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:31:15 2015

@author: achuth

This is the main script for the LDAP based Printer Solution to be used in IITB
All the other necessary functions are imported to this script and are called
when desired.

"""
from ldap_login import login
from account import account
from cupsprin import selection
from cupsprin import cupsprint

import cups,time

lpfile="lp"
printername="PDF"
login_status=True
username="sasi"

username,login_status=login()
while not login_status:
    username,login_status=login()
#if login_status:
#    choice = selection()
#    while choice != 3:
#        if choice == 1:
#            cupsprint(username,printername,lpfile)
#        if choice == 2:
#            print account(username)
#        choice = selection()
#    stuff()
#    conn = cups.Connection()
#    while conn.getJobs().get(jobid, None) is not None:
#        time.sleep(1)
#    account(username)