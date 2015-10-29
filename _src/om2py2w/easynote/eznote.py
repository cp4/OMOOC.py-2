import time
import datetime
import re

def recthis(note):
	if isinstance(note, unicode):
		noteStr = note.encode("utf8")
	else:
		noteStr = note

	db = open('endb.txt','a')
	now = time.strftime('%Y/%m/%d %X', time.localtime())
	db.write("[" + now + "] " + noteStr.strip('\r\n') + "\n")
	db.close()


def readnotes(dtstart="2001/01/01 00:00:00", dtsend="2020/12/12 23:59:59"):
	tstart = time.mktime(datetime.datetime.strptime(dtstart, "%Y/%m/%d %X").timetuple())
	tend = time.mktime(datetime.datetime.strptime(dtsend, "%Y/%m/%d %X").timetuple())
	db = open('endb.txt','r')
	selectedNotes = []
	for line in db.readlines():
		timepart = line.split(']')
		if len(timepart) > 1:
			timestr = timepart[0][1:]
			timestamp = time.mktime(datetime.datetime.strptime(timestr, "%Y/%m/%d %X").timetuple())
			if tstart < timestamp < tend:
				yield line
				#selectedNotes.append(line)

	db.close()
	#return selectedNotes