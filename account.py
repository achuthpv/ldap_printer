#! /usr/bin/python
import csv
import time
import sys


	#username = sys.argv[1]
def account(username):
	colLog = {'printer':0,'user':1,'jid':2,'timestamp':3,'page_no':5,'copies':6}
	colAcc = {'user':0,'pages':1,'timestamp':2,'max':3}
	logFile = "/var/log/cups/page_log"
	accFile = "/home/achuth/scripts/account.txt"
	#MAX = 200
	printers = ['PDF']

	csvFile = open(logFile,'rb')
	csvFile.seek(0)
	reader = csv.reader(csvFile,delimiter=' ')
	rowsLog = []
	for row in reader:
		if row[colLog['printer']] in printers and row[colLog['page_no']] != 'total':
			row[colLog['timestamp']]=row[colLog['timestamp']][1:]	#fix the opening brace of timestamp
			rowsLog.append(row)
	csvFile.close()

	csvFile = open(accFile,"a+b")
	reader = csv.reader(csvFile)
	rowsAcc = []

	for row in reader:
		rowsAcc.append(row)

	csvFile.close()

	#add new people
	users = {}
	for row in rowsLog:
		users[row[colLog['user']]]=0;

	for row in rowsAcc:
		try:
			users[row[colAcc['user']]] = users[row[colAcc['user']]] + 1
		except:
			pass

	for key in users.keys():
		if users[key] == 0:
			rowsAcc.append([key,0,1,0])	#name,pages,timestamp

	#compare and update
	pattern = '%d/%b/%Y:%H:%M:%S'
	total_pages=0
	for rowa in rowsAcc:
		user = rowa[colAcc['user']]
		latest = (rowa[colAcc['timestamp']] == 1) and 1 or time.mktime(time.strptime(rowa[colAcc['timestamp']],pattern))
		validRows = filter(lambda x:x[colLog['user']]==user and (latest == 1 or latest < time.mktime(time.strptime(x[colLog['timestamp']],pattern))),rowsLog)
		if len(validRows) > 0:
			rowa[colAcc['timestamp']] = validRows[-1][colLog['timestamp']]
			prints = sum(map(lambda y:int(y[colLog['copies']]),validRows))
			rowa[colAcc['pages']] = int(rowa[colAcc['pages']])+prints
			total_pages=rowa[colAcc['pages']]
	#warn
	row = filter(lambda x:x[colAcc['user']]==username,rowsAcc)
	status = 0

	#if len(row) == 1 and int(row[0][colAcc['pages']]) >= int(row[0][colAcc['max']]):
	#	print "\nDear %s,\nYou have exceeded your allocated quota of print outs for this semester.\nIncase of emergency, contact your nearest friendly sysad...\n" % (username)
	#	status = 1	#non-standard return code

	#if len(row) == 0:
	#	print "\nUsername: %s\nPrints so far: 0\nMaximum allowed this semester: 200\n" % (username)
	#elif status == 0:
	#	print "\nUsername: %s\nPrints so far: %s\nMaximum allowed this semester: %s\n" % (username,row[0][colAcc['pages']],row[0][colAcc['max']])

	#update accountfile
	csvFile = open(accFile,"wb")
	writer = csv.writer(csvFile)
	for row in rowsAcc:
		writer.writerow(row)
	csvFile.close()
	return total_pages
