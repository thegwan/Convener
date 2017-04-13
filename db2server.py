# db2server.py
# parses data from database to a json

import json
import database as db

#-----------------------------------------------------------------------

# returns list of user created meetings with their fields
def myMeetings_toList(my_meetings):
	my_meetings_list = []
	for meeting in my_meetings:
		title = meeting.title
		mid = meeting.mid	
		resp_netids  = db.getRespondedNetids(meeting.mid)
		nresp_netids = db.getNotRespondedNetids(meeting.mid)
		times = db.getRespondedPreferredTimes(meeting.mid)
		all_responded = len(nresp_netids) == 0

		# title = "title"+str(meeting)
		# resp_netids  = getRespondedNetids(meeting)
		# nresp_netids = getNotRespondedNetids(meeting)
		# times = getRespondedPreferredTimes(meeting)
		# all_responded = len(nresp_netids) == 0

		all_times = []
		for time in times:
			all_times += time

		my_meetings_list.append({
			"mid":mid,
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
		title = meeting.title
		mid = meeting.mid	
		creator = db.getUserFromId(meeting.creatorId).netid
		times = db.getUserPreferredTimes(mid, creator)

		# title = "title"+str(meeting)
		# creator = "creator"+str(meeting)

		my_requests_list.append({
			"mid":mid,
			"title":title,
			"creator":creator,
			"times":times
			})

	return my_requests_list


#-----------------------------------------------------------------------

# returns list of pending (not allResponded) meetings for the user
def pending_toList(pending, netid):
	pending_list = []
	for meeting in pending:
		title = meeting.title	
		mid = meeting.mid
		creator = db.getUserFromId(meeting.creatorId).netid
		times = db.getUserPreferredTimes(meeting.mid, netid)
		mine = creator == netid

		# title = "title"+str(meeting)
		# creator = "creator"+str(meeting)
		# times = getUserPreferredTimes(meeting, netid)
		# mine = False

		pending_list.append({
			"mid":mid,
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
		mid = meeting.mid
		title = meeting.title	
		creator = db.getUserFromId(meeting.creatorId).netid
		times = db.getUserPreferredTimes(meeting.mid, netid)
		mine = creator == netid
		# if meeting.scheduledTime is not None:
		# 	finaltime = meeting.scheduledTime
		# else:
		# 	finaltime = "hello"

		# title = "title"+str(meeting)
		# creator = "creator"+str(meeting)
		# times = getUserPreferredTimes(meeting, netid)
		# mine = False

		confirmed_list.append({
			"mid":mid,
			"title":title,
			"creator":creator,
			"times":times,
			"mine":mine
			#"finaltime":finaltime
			})

	return confirmed_list


#-----------------------------------------------------------------------


def init_protocol(netid):
	# get all pending and confirmed
	meetings = db.getUserMeetings(netid)
	# get all user created
	my_meetings = db.getUserCreatedMeetings(netid)
	# get all requests
	my_requests = db.getUserRequestedMeetings(netid)
	# meetings where everyone has responded
	confirmed = [m for m in meetings if m.allResponded]
	pending   = [m for m in meetings if not m.allResponded]
	
	# my_meetings = [1,2] 
	# my_requests = [3,4]
	# pending = [1]
	# confirmed = [2]
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

	return data
