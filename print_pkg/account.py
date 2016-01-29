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
import gzip
import time
import os
import ConfigParser


def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))


config = ConfigParser.ConfigParser()
config.read(get_abs_path("../config/printer.cfg"))
printer_name = config.get('printer', 'name')
log_file_dir = config.get('printer', 'logfile_dir')
log_file_name = config.get('printer', 'logfile')
acc_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/account.csv'))


def account(username='dummy', custom_acc_file=acc_file):
    col_log = {'printer': 0, 'user': 1, 'jid': 2, 'timestamp': 3, 'page_no': 5, 'copies': 6}
    col_acc = {'user': 0, 'pages': 1, 'timestamp': 2, 'max': 3}
    # MAX = 200
    printers = [printer_name]
    rows_log = []

    log_files = [filename for filename in os.listdir(log_file_dir) if filename.startswith(log_file_name)]

    for relative_log_file in log_files:
        log_file = os.path.join(log_file_dir, relative_log_file)
        if log_file.endswith('gz'):  # Gzip file
            csv_file = gzip.open(log_file, 'rb')
        else:
            csv_file = open(log_file, 'rb')

        csv_file.seek(0)
        reader = csv.reader(csv_file, delimiter=' ')

        for row in reader:
            if row[col_log['printer']] in printers and row[col_log['page_no']] != 'total':
                row[col_log['timestamp']] = row[col_log['timestamp']][1:]  # fix the opening brace of timestamp
                rows_log.append(row)

        csv_file.close()

    # Write into account file
    csv_file = open(custom_acc_file, 'a+b')
    reader = csv.reader(csv_file)
    rows_acc = []

    for row in reader:
        rows_acc.append(row)

    csv_file.close()

    # add new people

    # Get Users list in rows_log (from page_log)
    users = {}
    for row in rows_log:
        users[row[col_log['user']]] = 0

    # Get users in current account.csv
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

    # update account file
    csv_file = open(custom_acc_file, "wb")
    writer = csv.writer(csv_file)
    for row in rows_acc:
        writer.writerow(row)
    csv_file.close()
    return total_pages
