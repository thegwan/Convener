# dash.py

import json
from database import *


#-----------------------------------------------------------------------
# temporary hardcoded test data
def getRespondedNetids(mid):
	if mid == 1:
		return ["hsolis","gwan","ksha","bargotta"]
	return ["bob","joe","mary"]

def getNotRespondedNetids(mid):
	if mid == 1:
		return ["jackvw"]
	return []

def getRespondedPreferredTimes(mid):
	if mid == 1:
		return [[{u"day": u"Fri", u"time": u"1pm"}],
				[{u"day": u"Mon", u"time": u"2am"}, {u"day": u"Sun", u"time": u"4am"}]]
	return [[{u'day': u'Sun', u'time': u'6pm'}, {u'day': u'Wed', u'time': u'7pm'}, {u'day': u'Fri', u'time': u'9pm'}, {u'day': u'Tue', u'time': u'9pm'}],
			[{u'day': u'Wed', u'time': u'7pm'}, {u'day': u'Fri', u'time': u'9pm'}]]

def getUserPreferredTimes(mid, netid):
	if mid == 1 and netid == "gwan":
		return [{u"day": u"Fri", u"time": u"1pm"}]			
	return [{u'day': u'Sun', u'time': u'6pm'}, {u'day': u'Wed', u'time': u'7pm'}, {u'day': u'Fri', u'time': u'9pm'}, {u'day': u'Tue', u'time': u'9pm'}],



# test meetings (used meeting.id here)

my_meetings = [1,2] 
my_requests = [3,4]
pending = [1]
confirmed = [2]


#-----------------------------------------------------------------------

# returns list of user created meetings with their fields
def myMeetings_toList(my_meetings):
	my_meetings_list = []
	for meeting in my_meetings:
		# title = meeting.title	
		# resp_netids  = getRespondedNetids(meeting.mid)
		# nresp_netids = getNotRespondedNetids(meeting.mid)
		# times = getRespondedPreferredTimes(meeting.mid)
		# all_responded = len(nresp_netids) == 0

		title = "title"+str(meeting)
		resp_netids  = getRespondedNetids(meeting)
		nresp_netids = getNotRespondedNetids(meeting)
		times = getRespondedPreferredTimes(meeting)
		all_responded = len(nresp_netids) == 0

		all_times = []
		for time in times:
			all_times += time

		my_meetings_list.append({
			"title":title,
			"all_responded":all_responded,
			"resp_netids":resp_netids,
			"nresp_netids":nresp_netids,
			"times":all_times
			})

	return my_meetings_list


#-----------------------------------------------------------------------

# returns list of requested meetings that require the user to respond
def myRequests_toList(my_requests):
	my_requests_list = []
	for meeting in my_requests:
		# title = meeting.title	
		# creator = getUserFromId(meeting.creatorId)

		title = "title"+str(meeting)
		creator = "creator"+str(meeting)

		my_requests_list.append({
			"title":title,
			"creator":creator
			})

	return my_requests_list


#-----------------------------------------------------------------------

# returns list of pending (not allResponded) meetings for the user
def pending_toList(pending, netid):
	pending_list = []
	for meeting in pending:
		# title = meeting.title	
		# creator = getUserFromId(meeting.creatorId)
		# times = getUserPreferredTimes(meeting.mid, netid)
		# mine = creator == netid

		title = "title"+str(meeting)
		creator = "creator"+str(meeting)
		times = getUserPreferredTimes(meeting, netid)
		mine = False

		pending_list.append({
			"title":title,
			"creator":creator,
			"times":times,
			"mine":mine
			})

	return pending_list


#-----------------------------------------------------------------------

# returns list of confirmed meetings for the user
def confirmed_toList(confirmed, netid):
	confirmed_list = []
	for meeting in confirmed:
		# title = meeting.title	
		# creator = getUserFromId(meeting.creatorId)
		# times = getUserPreferredTimes(meeting.mid, netid)
		# mine = creator == netid

		title = "title"+str(meeting)
		creator = "creator"+str(meeting)
		times = getUserPreferredTimes(meeting, netid)
		mine = False

		confirmed_list.append({
			"title":title,
			"creator":creator,
			"times":times,
			"mine":mine
			})

	return confirmed_list


def toJSON(netid):
	# get all pending and confirmed
	##meetings = getUserMeetings(netid)
	# get all user created
	#my_meetings = getUserCreatedMeetings(netid)
	# get all requests
	##my_requests = getUserRequested(netid)

	# meetings where everyone has responded
	##confirmed = [m for m in meetings if m.allResponded]
	##pending   = [m for m in meetings if not m.allResponded]

	my_meetings_list = myMeetings_toList(my_meetings)
	my_requests_list = myRequests_toList(my_requests)
	pending_list = pending_toList(pending, netid)
	confirmed_list = confirmed_toList(confirmed, netid)

	data = {
			"my_meetings": my_meetings_list,
			"my_requests": my_requests_list,
			"pending": pending_list,
			"confirmed": confirmed_list
			}
	return json.dumps(data)
