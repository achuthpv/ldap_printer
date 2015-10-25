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


def login():
    rollno = None
    login_status = False
    roll_no_file = 'roll_no_list.txt'
    l = ldap.initialize('ldap://ldap.iitb.ac.in')
    # try:
    #
    #     l = ldap.init("ldap.iitb.ac.in")
    #     l.protocol_version = ldap.VERSION3
    #     l.simple_bind(who="testconnection")
    # except ldap.LDAPError:
    #     eg.msgbox(title="Cannot connect to LDAP server", msg="Please check the network connection")
    #     return rollno, login_status
    # handle error however you like

    msg = "Enter LDAP Credentials"
    title = "Printer Login"
    field_names = ["Username * ", "Password * "]

    field_values = eg.multpasswordbox(msg, title, field_names)

    # make sure that none of the fields was left blank
    while True:
        if not field_values:
            return rollno, login_status
        errmsg = ''
        for i in range(len(field_names)):
            if field_values[i].strip() == '':
                errmsg += ('"%s" is a mandatory field.' % field_names[i])
        if errmsg == '':
            break  # no problems found
        field_values = eg.multpasswordbox(errmsg, title, field_names, field_values)

    uid = field_values[0].strip()

    try:
        search_output = l.search_s('dc=iitb,dc=ac,dc=in', ldap.SCOPE_SUBTREE, 'uid=%s' % uid)
        if not search_output:
            raise ValueError("Invalid credentials", 'Invalid Username')
        for dne, entry in search_output:
            dn = dne

            if dn.find("ou=Alumni") > -1:
                raise ValueError('Invalid credentials', 'Alumni Account')
            rollno = entry['employeeNumber'][0]
            employee_type = entry['employee_type'][0]
            employee_type_list = "ug,pg,dd,rs"
            if not employee_type or employee_type_list.find(employee_type) == -1:
                raise ValueError('Invalid credentials', 'Not a Student Account')
            mess_member = False
            with open(roll_no_file, 'r') as mess_member_list:
                for line in mess_member_list:
                    if rollno in line:
                        mess_member = True
            if not mess_member:
                raise ValueError('Invalid credentials', 'Not a Member of the Hostel Mess')

            password = field_values[1].strip()
            l.bind_s(dn, password)
            login_status = 'uid=' + uid in l.whoami_s()

    except ValueError as e:
        eg.msgbox(title=e.args[0], msg=e.args[1])

    except ldap.LDAPError as e:
        # print e
        eg.msgbox(title=e.message.get('desc'), msg='Invalid Password')
    return rollno, login_status
    # [rollno,match]= login()
    # print rollno,match
