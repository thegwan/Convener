# db2server.py
# parses data from database to a json

import json, re
import database as db

# sample data

jpost1 = {u'title': 'The Olympics', u'response': [{u'date': u'04-18-17', u'time': u'4pm'}], u'netid': u'gwan', u'responders': [u'hsolis'], u'creationDate': '04-17-17'}
jpost2 = {u'mid': 1, u'response': [{u'date': u'04-19-17', u'time': u'7am'}, {u'date': u'04-20-17', u'time': u'7am'}], u'netid': u'gwan'}
jpost3 = {u'mid': 3, u'finalTime': [{u'date': u'04-22-17', u'time': u'10am'}], u'netid': u'gwan'}
jpost4 = {u'preferredTimes': [{u'date': u'03-19-17', u'time': u'10am'}, {u'date': u'03-20-17', u'time': u'11am'}], u'netid': u'gwan'}


#-----------------------------------------------------------------------

# checks if a date is in the right mm-dd-yy format
def date_isValid(date):
	if not isinstance(date, basestring):
		return False
	r = re.compile('^\d{2}-\d{2}-\d{2}$')
	if r.match(date) is not None:
		return True
	return False

#-----------------------------------------------------------------------

# checks if a time is in the right __[ap]m or _[ap]m format
def time_isValid(time):
	if not isinstance(time, basestring):
		return False
	r = re.compile('^\d{1,2}[a,p]m$')
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

# checks if a list of responder netids is valid
def responders_isValid(responders):
	if responders is None or []:
		return False

	for netid in responders:
		if not isinstance(netid, basestring):
			return False
	return True


#-----------------------------------------------------------------------

# checks if creation jpost is valid
def isValid_Creation(jpost):
	creationFields   = ["title", "netid", "response", "responders", "creationDate"]

	for key in jpost:
		if key not in creationFields:
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
	responseFields   = ["mid", "netid", "response"]

	for key in jpost:
		if key not in responseFields:
			return False

	if not isinstance(jpost["mid"], int):
		return False
	if not isinstance(jpost["netid"], basestring):
		return False
	if not datetimes_isValid(jpost["response"]):
		return False
		
	print "response ok"
	return True

#-----------------------------------------------------------------------

# checks if decision jpost is valid
def isValid_Decision(jpost):
	decisionFields   = ["mid", "netid", "finalTime"]

	for key in jpost:
		if key not in decisionFields:
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
	preferenceFields = ["netid", "preferredTimes"]

	for key in jpost:
		print key
		if key not in preferenceFields:
			return False

	if not isinstance(jpost["netid"], basestring):
		return False
	if not datetimes_isValid(jpost["preferredTimes"]):
		return False
		
	print "preference ok"
	return True

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
		return

	responders = jpost["responders"]
	# make sure all responders exist in database
	inviteUsers(responders)

	netid = jpost["netid"]
	title = jpost["title"]
	creatorId = db.getUser(netid).uid
	respondingIds = str([db.getUser(responder).uid for responder in responders])
	creationDate = jpost["creationDate"]

	meeting = db.createMeeting(title, creatorId, respondingIds, creationDate)
	db.createResponse(meeting.mid, creatorId, str(jpost["response"]))
	if db.getNotRespondedNetids(meeting.mid) == []:
		db.updateMeeting(meeting.mid, allResponded=True)

#-----------------------------------------------------------------------

# updates database for a meeting response
def parseResponse(jpost):
	if not isValid_Response(jpost):
		print "Response update went wrong. Not updated."
		return

	mid = jpost["mid"]

	netid = jpost["netid"]
	creatorId = db.getUser(netid).uid

	db.createResponse(mid, creatorId, str(jpost["response"]))
	if db.getNotRespondedNetids(mid) == []:
		db.updateMeeting(mid, allResponded=True)


#-----------------------------------------------------------------------

# updates database for a meeting time decision
def parseDecision(jpost):
	if not isValid_Decision(jpost):
		print "Final Time update went wrong. Not updated."
		return

	mid = jpost["mid"]

	netid = jpost["netid"]
	creatorId = db.getUser(netid).uid
	finalTime = str(jpost["finalTime"])

	if db.getNotRespondedNetids(mid) == []:
		db.updateMeeting(mid, allResponded=True, scheduledTime=finalTime)
	else:
		db.updateMeeting(mid, scheduledTime=finalTime)


#-----------------------------------------------------------------------

# updates database with user preferred times
def parsePreference(jpost):
	if not isValid_Preference(jpost):
		print "Preferred Times update went wrong. Not updated."
		return

	netid = jpost["netid"]
	preferredTimes = str(jpost["preferredTimes"])

	db.updateUser(netid, preferredTimes=preferredTimes)

#-----------------------------------------------------------------------

# distinguishes between a meeting creation and a meeting response
def parse(jpost):
	if "responders" in jpost:
		parseCreation(jpost)
	elif "finalTime" in jpost:
		parseDecision(jpost)
	elif "preferredTimes" in jpost:
		parsePreference(jpost)
	elif "mid" in jpost:
		parseResponse(jpost)
	else:
		return

#-----------------------------------------------------------------------

