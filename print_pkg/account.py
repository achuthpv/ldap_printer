#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Original Author: Sushant Mahajan, CSE IITB

This script takes care of logging the print logs present in cups page_log file
to Account.csv. Logging is done based on the time stamp difference in the page_log file
and the  Account.csv file for a certain user.
"""
import csv
import gzip
import time
import os
import ConfigParser
import datetime
from collections import defaultdict


def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))


config = ConfigParser.ConfigParser()
config.read(get_abs_path("../config/printer.cfg"))
printer_name = config.get('printer', 'name')
log_file_dir = config.get('printer', 'logfile_dir')
log_file_name = config.get('printer', 'logfile')
acc_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/account.csv'))


def account(username='dummy', custom_acc_file=acc_file, verbose=False, month=None):
    col_log = {'printer': 0, 'user': 1, 'jid': 2, 'timestamp': 3, 'page_no': 5, 'copies': 6}
    col_acc = {'user': 0, 'pages': 1, 'timestamp': 2, 'max': 3}
    # MAX = 200
    printers = [printer_name]
    rows_log = []

    # Get all log files including gzip ones
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

    users = defaultdict(list)

    pattern = '%d/%b/%Y:%H:%M:%S'
    if not month:
        month = datetime.datetime.now().month

    for row in rows_log:
        recorded_timestamp = row[col_log['timestamp']]
        py_time = time.strptime(recorded_timestamp, pattern)
        log_month = py_time.tm_mon
        if month == log_month:
            prints = row[col_log['copies']]  # type: str
            if not prints.isdigit():
                continue
            prints = int(prints)
            username = row[col_log['user']]
            users[username].append([prints, recorded_timestamp])

    compact_info = []
    verbose_info = []
    user_total_pages = 0

    for user, acc_list in users.items():
        total_prints = 0
        for acc in acc_list:
            total_prints += acc[0]
            if verbose:
                verbose_info.append([user, acc[0], acc[1]])

        if user == username:
            user_total_pages = total_prints

        last_timestamp = acc_list[-1][1]
        compact_info.append([user, total_prints, last_timestamp])

    # update account file
    with open(custom_acc_file, 'wb') as csv_file:
            writer = csv.writer(csv_file)

            for row in compact_info:
                writer.writerow(row)

    if verbose:
        dir, filename = os.path.split(custom_acc_file)
        verbose_filename = os.path.join(dir, 'verbose_' + filename)

        with open(verbose_filename, 'wb') as csv_file:
            writer = csv.writer(csv_file)

            for row in verbose_info:
                writer.writerow(row)

    return user_total_pages
