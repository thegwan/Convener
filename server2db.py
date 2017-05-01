# db2server.py
# parses data from server to database

import json, re
import database as db

#-----------------------------------------------------------------------

# checks if a day is in the right 3 letter format
def day_isValid(day):
	days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
	if day in days:
		return True
	return False

#-----------------------------------------------------------------------

# checks if a date is in the right mm-dd-yy format
def date_isValid(date):
	if not isinstance(date, basestring):
		return False
	r = re.compile('^\d{2}-\d{2}-\d{4}$')
	if r.match(date) is not None:
		return True
	return False

#-----------------------------------------------------------------------

# checks if a time is in the right __[ap]m or _[ap]m format
def time_isValid(time):
	if not isinstance(time, basestring):
		return False
	r = re.compile('^\d{1,2}:\d{2}[a,p]m$')
	if r.match(time) is not None:
		return True
	return False

#-----------------------------------------------------------------------

# checks if a list of dates and times is valid
def datetimes_isValid(datetimes):
	if datetimes is None:
		return False
	datetimeFields = ["date", "time"]
	for dt in datetimes:
		for key in dt:
			if key not in datetimeFields:
				return False
		if not (date_isValid(dt["date"]) and time_isValid(dt["time"])):
			return False
	return True

#-----------------------------------------------------------------------

# checks if a list of days and times is valid
def daytimes_isValid(daytimes):
	if daytimes is None:
		return False
	daytimeFields = ["day", "time"]
	for dt in daytimes:
		for key in dt:
			if key not in daytimeFields:
				return False
		if not (day_isValid(dt["day"]) and time_isValid(dt["time"])):
			return False
	return True

#-----------------------------------------------------------------------

# checks if a list of responder netids is valid
def responders_isValid(responders):
	if responders is None or []:
		return False

	for netid in responders:
		if not isinstance(netid, basestring):
			return False
		with open('netids.txt') as f:
			netids = f.readlines()
		netids = [n.strip() for n in netids]
		if netid not in netids:
			return False
	return True


#-----------------------------------------------------------------------

# checks if creation jpost is valid
def isValid_Creation(jpost):
	creationFields   = ["category", "title", "netid", "response", "responders", "creationDate"]

	for key in creationFields:
		if key not in jpost:
			return False

	if not isinstance(jpost["title"], basestring):
		return False
	if not isinstance(jpost["netid"], basestring):
		return False
	if not datetimes_isValid(jpost["response"]):
		return False
	if not responders_isValid(jpost["responders"]):
		return False
	if not date_isValid(jpost["creationDate"]):
		return False
		
	print "creation ok"
	return True

#-----------------------------------------------------------------------

# checks if response jpost is valid
def isValid_Response(jpost):
	responseFields   = ["category", "mid", "netid", "response"]

	for key in responseFields:
		if key not in jpost:
			return False

	if not isinstance(jpost["mid"], int):
		return False
	if not isinstance(jpost["netid"], basestring):
		return False
	if not datetimes_isValid(jpost["response"]):
		return False

	if db.getResponse(jpost["mid"], db.getUser(jpost["netid"]).uid) is not None:
		return False
		
	print "response ok"
	return True

#-----------------------------------------------------------------------

# checks if decision jpost is valid
def isValid_Decision(jpost):
	decisionFields   = ["category", "mid", "netid", "finalTime"]

	for key in decisionFields:
		if key not in jpost:
			return False

	if not isinstance(jpost["mid"], int):
		return False
	if not isinstance(jpost["netid"], basestring):
		return False
	if len(jpost["finalTime"]) > 1:         # if more than 1 scheduled time
		return False
	if not datetimes_isValid(jpost["finalTime"]):
		return False
		
	print "decision ok"
	return True

#-----------------------------------------------------------------------

# checks if preference jpost is valid
def isValid_Preference(jpost):
	preferenceFields = ["category", "netid", "preferredTimes"]

	for key in preferenceFields:
		if key not in jpost:
			return False

	if not isinstance(jpost["netid"], basestring):
		return False
	if not daytimes_isValid(jpost["preferredTimes"]):
		return False

	print "preference ok"
	return True

#-----------------------------------------------------------------------

def isValid_MeetingDelete(jpost):
	meetingDeleteFields = ["category", "mid", "netid"]
	for key in meetingDeleteFields:
		if key not in jpost:
			return False

	if not isinstance(jpost["netid"], basestring):
		return False
	if not isinstance(jpost["mid"], int):
		return False

	# check if netid is the creator of the meeting
	meeting = db.getMeeting(jpost["mid"])
	if meeting is None:
		return False
	if meeting not in db.getUserCreatedMeetings(jpost["netid"]):
		return False

	print "meeting deletion ok"
	return True


#-----------------------------------------------------------------------		


#-----------------------------------------------------------------------		

# adds invited users to database if not already there
def inviteUsers(responders):
	for netid in responders:
		if db.getUser(netid) == None:
			db.createUser(netid)

#-----------------------------------------------------------------------

# updates database for a meeting creation
def parseCreation(jpost):
	if not isValid_Creation(jpost):
		print "Creation update went wrong. Not updated."
		return False

	responders = jpost["responders"]
	# make sure all responders exist in database
	inviteUsers(responders)

	netid = jpost["netid"]
	title = jpost["title"]
	# remove quotations from titles
	title = title.replace("'", "")
	title = title.replace('"', '')
	creatorId = db.getUser(netid).uid
	respondingIds = str([db.getUser(responder).uid for responder in responders])
	creationDate = jpost["creationDate"]

	meeting = db.createMeeting(title, creatorId, respondingIds, creationDate)
	db.createResponse(meeting.mid, creatorId, str(jpost["response"]))
	if db.getNotRespondedNetids(meeting.mid) == []:
		db.updateMeeting(meeting.mid, allResponded=True)
	return True

#-----------------------------------------------------------------------

# updates database for a meeting response
def parseResponse(jpost):
	if not isValid_Response(jpost):
		print "Response update went wrong. Not updated."
		return False

	mid = jpost["mid"]

	netid = jpost["netid"]
	creatorId = db.getUser(netid).uid

	db.createResponse(mid, creatorId, str(jpost["response"]))
	if db.getNotRespondedNetids(mid) == []:
		db.updateMeeting(mid, allResponded=True)
	return True


#-----------------------------------------------------------------------

# updates database for a meeting time decision
def parseDecision(jpost):
	if not isValid_Decision(jpost):
		print "Final Time update went wrong. Not updated."
		return False

	mid = jpost["mid"]

	netid = jpost["netid"]
	creatorId = db.getUser(netid).uid
	finalTime = str(jpost["finalTime"])

	if db.getNotRespondedNetids(mid) == []:
		db.updateMeeting(mid, allResponded=True, scheduledTime=finalTime)
	else:
		db.updateMeeting(mid, scheduledTime=finalTime)
	return True


#-----------------------------------------------------------------------

# updates database with user preferred times
def parsePreference(jpost):
	if not isValid_Preference(jpost):
		print "Preferred Times update went wrong. Not updated."
		return False

	netid = jpost["netid"]
	preferredTimes = str(jpost["preferredTimes"])

	db.updateUser(netid, preferredTimes=preferredTimes)
	return True

#-----------------------------------------------------------------------

# deletes meeting from database
def parseMeetingDelete(jpost):
	if not isValid_MeetingDelete(jpost):
		print "Meeting Deletion went wrong. Not deleted."
		return False

	mid = jpost["mid"]

	db.deleteMeeting(mid)
	return True

#-----------------------------------------------------------------------

# distinguishes between a meeting creation and a meeting response
def parse(jpost):
	if jpost["category"] == "creation":
		return parseCreation(jpost)
	elif jpost["category"] == "decision":
		return parseDecision(jpost)
	elif jpost["category"] == "updatePref":
		return parsePreference(jpost)
	elif jpost["category"] == "response":
		return parseResponse(jpost)
	elif jpost["category"] == "meetingDelete":
		return parseMeetingDelete(jpost)
	else:
		return False

#-----------------------------------------------------------------------

