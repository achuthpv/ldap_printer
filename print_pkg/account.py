#! /usr/bin/python
# -*- coding: utf-8 -*-
"""

I got the script from Sushant Mahajan of CSE Department
edited by: Achuth PV

This script takes care of logging the print logs present in cups page_log file
to Account.csv. Logging is done based on the time stamp difference in the page_log file
and the  Account.csv file for a certain user.

"""
import csv
import time
import os


acc_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/account.csv'))


def account(username):
    col_log = {'printer': 0, 'user': 1, 'jid': 2, 'timestamp': 3, 'page_no': 5, 'copies': 6}
    col_acc = {'user': 0, 'pages': 1, 'timestamp': 2, 'max': 3}
    log_file = '/var/log/cups/page_log'
    # MAX = 200
    printers = ['PDF']

    csv_file = open(log_file, 'rb')
    csv_file.seek(0)
    reader = csv.reader(csv_file, delimiter=' ')
    rows_log = []
    for row in reader:
        if row[col_log['printer']] in printers and row[col_log['page_no']] != 'total':
            row[col_log['timestamp']] = row[col_log['timestamp']][1:]  # fix the opening brace of timestamp
            rows_log.append(row)
    csv_file.close()

    csv_file = open(acc_file, 'a+b')
    reader = csv.reader(csv_file)
    rows_acc = []

    for row in reader:
        rows_acc.append(row)

    csv_file.close()

    # add new people
    users = {}
    for row in rows_log:
        users[row[col_log['user']]] = 0

    for row in rows_acc:
        try:
            users[row[col_acc['user']]] += 1
        except (IndexError, TypeError, KeyError):
            pass

    for key in users.keys():
        if users[key] == 0:
            rows_acc.append([key, 0, 1])  # name,pages,timestamp

    # compare and update
    pattern = '%d/%b/%Y:%H:%M:%S'
    for rowa in rows_acc:
        user = rowa[col_acc['user']]
        latest = (rowa[col_acc['timestamp']] == 1) and 1 or time.mktime(
            time.strptime(rowa[col_acc['timestamp']], pattern))
        valid_rows = filter(lambda x: x[col_log['user']] == user and (
            latest == 1 or latest < time.mktime(time.strptime(x[col_log['timestamp']], pattern))), rows_log)
        if len(valid_rows) > 0:
            rowa[col_acc['timestamp']] = valid_rows[-1][col_log['timestamp']]
            prints = sum(map(lambda y: int(y[col_log['copies']]), valid_rows))
            rowa[col_acc['pages']] = int(rowa[col_acc['pages']]) + prints
    # warn
    row = filter(lambda x: x[col_acc['user']] == username, rows_acc)

    if len(row) == 0:
        total_pages = 0
    else:
        total_pages = row[0][col_acc['pages']]

    # update accountfile
    csv_file = open(acc_file, "wb")
    writer = csv.writer(csv_file)
    for row in rows_acc:
        writer.writerow(row)
    csv_file.close()
    return total_pages
