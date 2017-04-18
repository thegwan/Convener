# db2server.py
# parses data from database to a json

import json
import database as db

# sample data
jpost1 = {u'mid': u'1', u'response': [{u'day': u'Tue', u'time': u'3am'}], u'netid': u'gwan'}
jpost2 = {u'title': 'The Olympics', u'response': [{u'day': u'Mon', u'time': u'4pm'}], u'netid': u'gwan', u'responders': [u'hsolis']}
jpost3 = {u'mid': u'3', u'response': [{u'day': u'Mon', u'time': u'5pm'}, {u'day': u'Mon', u'time': u'6pm'}], u'netid': u'gwan'}
jpost4 = {u'title': 'Arch Sing', u'response': [{u'day': u'Mon', u'time': u'4pm'}], u'netid': u'bargotta', u'responders': [u'ili', u'asdf']}
jpost5 = {u'mid': u'4', u'response': [{u'day': u'Wed', u'time': u'1am'}], u'netid': u'ksha'}
jpost6 = {u'title': 'Google Interview', u'response': [{u'day': u'Mon', u'time': u'1pm'}], u'netid': u'hsolis', u'responders': [u'joeshmoe']}
jpost7 = {u'title': 'Squad Meetup', u'response': [{u'day': u'Thu', u'time': u'12pm'}], u'netid': u'hsolis', u'responders': [u'joeshmoe', u'ecorless']}
jpost8 = {u'title': 'Friend hangout', u'response': [{u'day': u'Fri', u'time': u'12pm'}], u'netid': u'joeshmoe', u'responders': [u'ecorless', u'ecorless']}
jpost9 = {u'mid': u'12', u'response': [{u'day': u'Wed', u'time': u'1am'}], u'netid': u'ecorless'}


#-----------------------------------------------------------------------

# adds invited users to database if not already there
def inviteUsers(responders):
	for netid in responders:
		if db.getUser(netid) == None:
			db.createUser(netid)

#-----------------------------------------------------------------------

# updates database for a meeting creation
def parseCreation(jpost):
	responders = jpost["responders"]
	# make sure all responders exist in database
	inviteUsers(responders)

	netid = jpost["netid"]
	title = jpost["title"]
	creatorId = db.getUser(netid).uid
	respondingIds = str([db.getUser(responder).uid for responder in responders])

	meeting = db.createMeeting(title, creatorId, respondingIds)
	db.createResponse(meeting.mid, creatorId, str(jpost["response"]))
	if db.getNotRespondedNetids(meeting.mid) == []:
		db.updateMeeting(meeting.mid, allResponded=True)

#-----------------------------------------------------------------------

# updates database for a meeting response
def parseResponse(jpost):
	mid = jpost["mid"]

	netid = jpost["netid"]
	creatorId = db.getUser(netid).uid

	db.createResponse(mid, creatorId, str(jpost["response"]))
	if db.getNotRespondedNetids(mid) == []:
		db.updateMeeting(mid, allResponded=True)


#-----------------------------------------------------------------------

# updates database for a meeting time decision
def parseDecision(jpost):
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
	netid = jpost["netid"]
	preferredTimes = jpost["preferredTimes"]

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
	else:
		parseResponse(jpost)

#-----------------------------------------------------------------------


# sample database updating - watchout! will modify database

# parse(jpost1)
# parse(jpost2)
# parse(jpost3)
# parse(jpost4)
# parse(jpost5)
# parse(jpost6)
# parse(jpost7)
# parse(jpost8)
# parse(jpost9)