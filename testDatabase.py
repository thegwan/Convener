## Test data for checking if the database properly works
from database import *
# import ast

# # Testing
# createUser('hsolis', 'Hector', 'Solis', "[{'Day':'Fri', 'Time': '12:00'}]")
# createUser('gwan', 'Gerry')
# createUser('bargotta', unacceptableTimes="[{'Day':'Fri', 'Time': '12:00'}]")
# createUser('ksha', 'Sha', acceptableTimes="[{'Day':'Fri', 'Time': '12:00'}]")
# createUser('kl9', 'Katherine', 'Lee', "[{'Day':'Mon', 'Time': '18:00'}]}, {[{'Day':'Tue', 'Time': '12:00'}]}, {[{'Day':'Sat', 'Time': '9:00'}]")

# hector = getUser('hsolis')
# gary = getUser('gwan')

# createMeeting('Colonial Dinner', 1, '[2, 4]')
# createMeeting('Back Massage', hector.uid, "[2]")
# createMeeting('Charter Friday', gary.uid, "[4]")

# createResponse(1, 1, "[ { 'Day': 'Thu', 'Time': '8:30' }, { 'Day': 'Fri', 'Time': '12:00' } ]")
# createResponse(1, 2, "[ { 'Day': 'Thu', 'Time': '8:30' }, { 'Day': 'Fri', 'Time': '12:00' } ]")
# createResponse(1, 4,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")

# createResponse(2, 1,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")
# createResponse(3, 2,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")


# updateUser('hsolis', 'Hector', 'Solis', "[{'Day':'Fri', 'Time': '12:00'}]", "[{'Day':'Mon', 'Time': '11:00'}]", "[{'Day':'Wed', 'Time': '3:00'}]")

# updateMeeting(1, True, "[{'Day': 'Fri', 'Time': '18:00'}]")

# createUser('jackvw', 'Jack', 'Wolfgramm')

# # meetings = getUserCreatedMeetings('hsolis')
# # print meetings

# # kim = getUser('ksha')
# # meet = getUserMeetings('ksha')
# # for i in meet:
# # 	print i.title

# # Test getting the netids of those who have responded
# for i in getRespondedNetids(1): 
# 	print i

# # Test getting the netids of those who have responded
# for i in getRespondedNetids(2): 
# 	print "responded " + i

# # Test getting the netids of those who have not yet responded
# for i in getNotRespondedNetids(2): 
# 	print "not responded " + i

# # Test getting the preferred times of those who have responded
# for i in getRespondedPreferredTimes(1): 
# 	print i

# # Test getting the preferred times of a response given meetingid and netid
# for i in getUserPreferredTimes(1, 'hsolis'): 
# 	print i

# Test getting the meetings where a user with netid has already responded
for i in getUserMeetings('ksha'): 
	print i.title