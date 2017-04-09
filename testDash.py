# testDash.py

# Testing database server connection and initial protocol
# data creation (run after creating an empty db)

import db2server, json
import database as dbase

#-----------------------ok----------------------------

# netid = "hsolis"
# my_meetings = dbase.getUserCreatedMeetings(netid)
# my_requests = dbase.getUserRequestedMeetings(netid)

# #meetings = [meeting.mid for meeting in dbase.getUserMeetings(netid)]
# meetings = dbase.getUserMeetings(netid)
# confirmed = [m for m in meetings if m.allResponded]
# pending   = [m for m in meetings if not m.allResponded]

# assert(sorted([m.mid for m in my_meetings]) == sorted([1,2]))
# assert(sorted([m.mid for m in my_requests]) == sorted([4]))
# assert(sorted([m.creatorId for m in my_requests]) == "kl9")
# print my_meetings
# print my_requests
# print confirmed
# print pending

#-----------------------ok----------------------------


print json.dumps(db2server.init_protocol("hsolis"), indent=2, sort_keys=True)
#print json.dumps(dash.init_protocol("gwan"), indent=2, sort_keys=True)
#print json.dumps(dash.init_protocol("ksha"), indent=2, sort_keys=True)
#print json.dumps(dash.init_protocol("jackvw"), indent=2, sort_keys=True)
#print json.dumps(dash.init_protocol("bargotta"), indent=2, sort_keys=True)
#print json.dumps(dash.init_protocol("kl9"), indent=2, sort_keys=True)


#-----------------------------------------------------------------------
# temporary hardcoded test functions and data
# def getRespondedNetids(mid):
# 	if mid == 1:
# 		return ["hsolis","gwan","ksha","bargotta"]
# 	return ["bob","joe","mary"]

# def getNotRespondedNetids(mid):
# 	if mid == 1:
# 		return ["jackvw"]
# 	return []

# def getRespondedPreferredTimes(mid):
# 	if mid == 1:
# 		return [[{u"day": u"Fri", u"time": u"1pm"}],
# 				[{u"day": u"Mon", u"time": u"2am"},
# 				 {u"day": u"Sun", u"time": u"4am"}]]
# 	return [[{u'day': u'Sun', u'time': u'6pm'},
# 			 {u'day': u'Wed', u'time': u'7pm'},
# 			 {u'day': u'Fri', u'time': u'9pm'},
# 			 {u'day': u'Tue', u'time': u'9pm'}],
# 			[{u'day': u'Wed', u'time': u'7pm'},
# 			 {u'day': u'Fri', u'time': u'9pm'}]]

# def getUserPreferredTimes(mid, netid):
# 	if mid == 1 and netid == "gwan":
# 		return [{u"day": u"Fri", u"time": u"1pm"}]			
# 	return [{u'day': u'Sun', u'time': u'6pm'},
# 		 	{u'day': u'Wed', u'time': u'7pm'},
# 		 	{u'day': u'Fri', u'time': u'9pm'},
# 		 	{u'day': u'Tue', u'time': u'9pm'}]

# # test meetings (used meeting.id here)

# my_meetings = [1,2] 
# my_requests = [3,4]
# pending = [1]
# confirmed = [2]

# print dash.toJSON("gwan")

#-----------------------------------------------------------------------