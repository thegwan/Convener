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
		creation_date = meeting.creationDate	
		resp_netids  = db.getRespondedNetids(meeting.mid)
		nresp_netids = db.getNotRespondedNetids(meeting.mid)
		#times = db.getRespondedPreferredTimes(meeting.mid)
		all_responded = len(nresp_netids) == 0
		finaltime = db.getScheduledTime(mid)

		responder_times = {}
		for responder in resp_netids:
			times = db.getUserPreferredTimes(mid, responder)
			responder_times[responder] = times
		
		# all_times = []
		# for time in times:
		# 	all_times += time

		my_meetings_list.append({
			"mid":mid,
			"title":title,
			"creation_date":creation_date,
			"all_responded":all_responded,
			"resp_netids":resp_netids,
			"nresp_netids":nresp_netids,
			"responder_times":responder_times,
			"finaltime":finaltime
			})

	return my_meetings_list

#-----------------------------------------------------------------------

# returns list of requested meetings that require the user to respond
def myResponded_toList(my_responded, netid):
	my_responded_list = []
	for meeting in my_responded:
		title = meeting.title
		mid = meeting.mid
		creation_date = meeting.creationDate	
		creator = db.getUserFromId(meeting.creatorId).netid
		times = db.getUserPreferredTimes(mid, netid)
		creator_times = db.getUserPreferredTimes(mid, creator)
		finaltime = db.getScheduledTime(mid)
		mine = creator == netid

		my_responded_list.append({
			"mid":mid,
			"title":title,
			"creation_date":creation_date,
			"creator":creator,
			"times":times,
			"creator_times":creator_times
			"finaltime":finaltime,
			"mine":mine
			})

	return my_responded_list

#-----------------------------------------------------------------------

# returns list of requested meetings that require the user to respond
def myRequests_toList(my_requests):
	my_requests_list = []
	for meeting in my_requests:
		title = meeting.title
		mid = meeting.mid
		creation_date = meeting.creationDate	
		creator = db.getUserFromId(meeting.creatorId).netid
		times = db.getUserPreferredTimes(mid, creator)

		my_requests_list.append({
			"mid":mid,
			"title":title,
			"creation_date":creation_date,
			"creator":creator,
			"times":times
			})

	return my_requests_list

#-----------------------------------------------------------------------

# # returns list of pending (not allResponded) meetings for the user
# def pending_toList(pending, netid):
# 	pending_list = []
# 	for meeting in pending:
# 		title = meeting.title	
# 		mid = meeting.mid
# 		creator = db.getUserFromId(meeting.creatorId).netid
# 		times = db.getUserPreferredTimes(meeting.mid, netid)
# 		mine = creator == netid

# 		pending_list.append({
# 			"mid":mid,
# 			"title":title,
# 			"creator":creator,
# 			"times":times,
# 			"mine":mine
# 			})

# 	return pending_list


# #-----------------------------------------------------------------------

# # returns list of confirmed meetings for the user
# def confirmed_toList(confirmed, netid):
# 	confirmed_list = []
# 	for meeting in confirmed:
# 		mid = meeting.mid
# 		title = meeting.title	
# 		creator = db.getUserFromId(meeting.creatorId).netid
# 		times = db.getUserPreferredTimes(meeting.mid, netid)
# 		mine = creator == netid
# 		finaltime = db.getScheduledTime(mid)

# 		confirmed_list.append({
# 			"mid":mid,
# 			"title":title,
# 			"creator":creator,
# 			"times":times,
# 			"mine":mine,
# 			"finaltime":finaltime
# 			})

# 	return confirmed_list


#-----------------------------------------------------------------------


def init_protocol(netid):

	# get all meetings user created
	my_meetings = db.getUserCreatedMeetings(netid)
	# get all meetings user responded to
	my_responded = db.getUserMeetings(netid)
	# get all requests for user
	my_requests = db.getUserRequestedMeetings(netid)

	my_meetings_list = myMeetings_toList(my_meetings)
	my_responded_list = myResponded_toList(my_responded, netid)
	my_requests_list = myRequests_toList(my_requests)


	data = {
			"my_meetings": my_meetings_list,
			"my_responded": my_responded_list,
			"my_requests": my_requests_list,
			"my_preferred": db.getUserPreferences(netid)
			}

	return data
