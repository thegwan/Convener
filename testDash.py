# testDash.py

# Testing database server connection and initial protocol
# data creation (run after creating an empty db)

import dash, database, json

print json.dumps(dash.toJSON("hsolis"), indent=2, sort_keys=True)
print json.dumps(dash.toJSON("gwan"), indent=2, sort_keys=True)
print json.dumps(dash.toJSON("ksha"), indent=2, sort_keys=True)
print json.dumps(dash.toJSON("jackvw"), indent=2, sort_keys=True)
print json.dumps(dash.toJSON("bargotta"), indent=2, sort_keys=True)
print json.dumps(dash.toJSON("kl9"), indent=2, sort_keys=True)


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