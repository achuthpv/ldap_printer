#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 20:31:15 2015

@author: achuth

This script contains the functions which takes care LDAP login.
It also return username and the login status of the user
username: string (rollno of the student)
login_status: boolean (True when login is successful, False otherwise)

"""
import ldap
import easygui as eg
## first you must open a connection to the server
def login ():
    rollno = None
    login_status = False
    try:

        l = ldap.init("ldap.iitb.ac.in")
        l.protocol_version = ldap.VERSION3
        l.simple_bind(who="testconnection")
    except ldap.LDAPError, e:
        eg.msgbox(title="Cannot connect to LDAP server", msg="Please check the network connection")

        return rollno, login_status
    # handle error however you like
    



    msg = "Enter LDAP Credentials"
    title = "Printer Login"
    fieldNames = ["Username * ", "Password * "]
    fieldValues = []  # we start with blanks for the values
    fieldValues = eg.multpasswordbox(msg,title, fieldNames)
 
     # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None:
            return rollno, login_status
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a mandatory field.' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = eg.multpasswordbox(errmsg, title, fieldNames, fieldValues) 

    baseDN = "dc=iitb,dc=ac,dc=in"
    searchScope = ldap.SCOPE_SUBTREE
    uid=fieldValues[0].strip()
    searchFilter = '(uid='+uid+')'
    dn=None

    try:
        search_output= l.search_s(baseDN, searchScope, searchFilter)
        if not search_output:
            raise ValueError("Invalid credentials",'Invalid Username')
        for dne,entry in search_output:
            dn=dne
            err=None

            if dn.find("ou=Alumni") > -1:
                raise ValueError('Invalid credentials', 'Alumni Account')
            rollno=entry['employeeNumber'][0]
            employeeType=entry['employeeType'][0]
            employeeTypeList="ug,pg,dd,rs"
            if employeeType==None or employeeTypeList.find(employeeType) == -1:
                raise ValueError('Invalid credentials', 'Not a Student Account')
            password=fieldValues[1].strip()
            l.bind_s(dn,password)
            login_status= 'uid='+uid in l.whoami_s()

    except ValueError as e:
        eg.msgbox(title=e.args[0], msg=e.args[1])

    except ldap.LDAPError, e:
        #print e
        eg.msgbox(title=e.message.get('desc'), msg='Invalid Password')
    return rollno, login_status
#[rollno,match]= login()
#print rollno,match