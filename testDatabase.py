## Test data for checking if the database properly works (run after creating an empty db)
from database import *
# import ast

# Testing

## Create users and check that they were properly added ###########################################
createUser('hsolis', 'Hector', 'Solis', "[{'Day':'Fri', 'Time': '12:00'}]")
createUser('gwan', 'Gerry')
createUser('bargotta', unacceptableTimes="[{'Day':'Fri', 'Time': '12:00'}]")
createUser('ksha', lastName='Sha', acceptableTimes="[{'Day':'Fri', 'Time': '12:00'}]")
createUser('kl9', 'Katherine', 'Lee', "[{'Day':'Mon', 'Time': '18:00'}]}, {[{'Day':'Tue', 'Time': '12:00'}]}, {[{'Day':'Sat', 'Time': '9:00'}]")

hector = getUser('hsolis')
gary = getUser('gwan')
aaron = getUser('bargotta')
kim = getUserFromId(4)
katlee = getUserFromId(5)

assert hector.uid == 1 and hector.firstName == 'Hector' and \
	hector.lastName == 'Solis' and hector.preferredTimes == "[{'Day':'Fri', 'Time': '12:00'}]"

assert gary.uid == 2 and gary.firstName == 'Gerry' and \
	gary.lastName == None and gary.preferredTimes == None

assert aaron.uid == 3 and aaron.firstName == None and \
	aaron.lastName == None and aaron.unacceptableTimes == "[{'Day':'Fri', 'Time': '12:00'}]"

assert kim.uid == 4 and kim.firstName == None and \
	kim.lastName == 'Sha' and kim.acceptableTimes == "[{'Day':'Fri', 'Time': '12:00'}]"

assert katlee.uid == 5 and katlee.firstName == 'Katherine' and \
	katlee.lastName == 'Lee' and katlee.preferredTimes == "[{'Day':'Mon', 'Time': '18:00'}]}, {[{'Day':'Tue', 'Time': '12:00'}]}, {[{'Day':'Sat', 'Time': '9:00'}]"

## Create meetings and check that they were properly added ###########################################

createMeeting('Colonial Lunch', hector.uid, '[2, 4]')
createMeeting('Back Massage', hector.uid, "[2]")
createMeeting('Charter Friday', gary.uid, "[4]")
createMeeting('Code@Night', katlee.uid, "[6, 2, 1, 3, 4]")



createResponse(1, 1, "[ { 'Day': 'Thu', 'Time': '8:30' }, { 'Day': 'Fri', 'Time': '12:00' } ]")
createResponse(1, 2, "[ { 'Day': 'Thu', 'Time': '8:30' }, { 'Day': 'Fri', 'Time': '12:00' } ]")
createResponse(1, 4,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")

createResponse(2, 1,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")
createResponse(3, 2,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")

createResponse(4, 5,  "[{ 'Day': 'Fri', 'Time': '20:00' } ]")
createResponse(4, 1,  "[{ 'Day': 'Fri', 'Time': '20:00' } ]")
createResponse(4, 3,  "[{ 'Day': 'Fri', 'Time': '20:00' } ]")


# updateUser('hsolis', 'Hector', 'Solis', "[{'Day':'Fri', 'Time': '12:00'}]", "[{'Day':'Mon', 'Time': '11:00'}]", "[{'Day':'Wed', 'Time': '3:00'}]")

# updateMeeting(1, True, "[{'Day': 'Fri', 'Time': '12:00'}]")

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

# # Test getting the meetings where a user with netid has already responded
# for i in getUserMeetings('ksha'): 
# 	print i.title

# # Test getting the meetings where a user with netid has not yet responded
# for i in getUserRequestedMeetings('gwan'): 
# 	print i.title