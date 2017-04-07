## Test data for checking if the database properly works (run after creating an empty db)
from database import *
# import ast

# Testing

## Create users and check that they were properly added ###########################################
createUser('hsolis', 'Hector', 'Solis', "[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]")
createUser('gwan', 'Gerry')
createUser('bargotta', unacceptableTimes="[{'Day': 'Fri', 'Time': '12:00'}]")
createUser('ksha', lastName='Sha', acceptableTimes="[{'Day': 'Fri', 'Time': '12:00'}]")
createUser('kl9', 'Katherine', 'Lee', "[{'Day': 'Mon', 'Time': '18:00'}, {'Day': 'Tue', 'Time': '12:00'}, {'Day': 'Sat', 'Time': '9:00'}]")

hector = getUser('hsolis')
gary = getUser('gwan')
aaron = getUser('bargotta')
kim = getUserFromId(4)
katlee = getUserFromId(5)

assert hector.uid == 1 and hector.firstName == 'Hector' and \
	hector.lastName == 'Solis' and hector.preferredTimes == "[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]"

assert gary.uid == 2 and gary.firstName == 'Gerry' and \
	gary.lastName == None and gary.preferredTimes == None

assert aaron.uid == 3 and aaron.firstName == None and \
	aaron.lastName == None and aaron.unacceptableTimes == "[{'Day': 'Fri', 'Time': '12:00'}]"

assert kim.uid == 4 and kim.firstName == None and \
	kim.lastName == 'Sha' and kim.acceptableTimes == "[{'Day': 'Fri', 'Time': '12:00'}]"

assert katlee.uid == 5 and katlee.firstName == 'Katherine' and \
	katlee.lastName == 'Lee' and katlee.preferredTimes == "[{'Day': 'Mon', 'Time': '18:00'}, {'Day': 'Tue', 'Time': '12:00'}, {'Day': 'Sat', 'Time': '9:00'}]"

## Create meetings and check that they were properly added ########################################

createMeeting('Colonial Lunch', hector.uid, "[2, 4]")
createMeeting('Back Massage', hector.uid, "[2]")
createMeeting('Charter Friday', gary.uid, "[4]")
createMeeting('Code@Night', katlee.uid, "[6, 2, 1, 3, 4]")

colonial = getMeeting(1)
massage = getMeeting(2)
charter = getMeeting(3)
code = getMeeting(4)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]"

assert massage.mid == 2 and massage.title == 'Back Massage' and \
	massage.creatorId == hector.uid and massage.respondingId == "[2]"

assert charter.mid == 3 and charter.title == 'Charter Friday' and \
	charter.creatorId == gary.uid and charter.respondingId == "[4]"

assert code.mid == 4 and code.title == 'Code@Night' and \
	code.creatorId == katlee.uid and code.respondingId == "[6, 2, 1, 3, 4]"


## Create responses and check them ################################################################


createResponse(1, 1, "[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]")
createResponse(1, 2, "[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]")
createResponse(1, 4,  "[{ 'Day': 'Fri', 'Time': '12:00' } ]")

createResponse(2, 1,  "[{'Day': 'Fri', 'Time': '12:00'}]")
createResponse(3, 2,  "[{'Day': 'Fri', 'Time': '12:00'}]")

createResponse(4, 5,  "[{'Day': 'Fri', 'Time': '20:00'}]")
createResponse(4, 1,  "[{'Day': 'Fri', 'Time': '20:00'}]")
createResponse(4, 3,  "[{'Day': 'Fri', 'Time': '20:00'}]")

rsp1 = getResponse(1, 1)
rsp4 = getResponse(2, 1)
rsp6 = getResponse(4, 5)

assert rsp1.preferredTimes == "[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]"

assert rsp4.preferredTimes == "[{'Day': 'Fri', 'Time': '12:00'}]"

assert rsp6.preferredTimes == "[{'Day': 'Fri', 'Time': '20:00'}]"

## Update a user, check if it worked ##############################################################


updateUser('hsolis', 'Tear', 'Swag', "[{'Day': 'Fri', 'Time': '12:00'}]", \
	"[{'Day': 'Mon', 'Time': '11:00'}]", "[{'Day': 'Wed', 'Time': '3:00'}]")

hector = getUser('hsolis')

assert hector.uid == 1 and hector.firstName == 'Tear' and \
	hector.lastName == 'Swag' and hector.preferredTimes == "[{'Day': 'Fri', 'Time': '12:00'}]" \
	and hector.acceptableTimes == "[{'Day': 'Mon', 'Time': '11:00'}]" and \
	hector.unacceptableTimes == "[{'Day': 'Wed', 'Time': '3:00'}]"

## Update a meeting, check if it worked ###########################################################


updateMeeting(1, True, "[{'Day': 'Fri', 'Time': '12:00'}]")

colonial = getMeeting(1)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]" \
	and colonial.allResponded == True and colonial.scheduledTime == "[{'Day': 'Fri', 'Time': '12:00'}]"

## Make sure you can still add users who are late to the party ####################################

createUser('jackvw', 'Jack', 'Wolfgramm')


## Extraneous function testing ####################################################################

## getUserCreatedMeetings
meetings = [m.title for m in getUserCreatedMeetings('hsolis')]

# Check that the meetings in meetings are the same as the ones by hector
assert not(filter(lambda x: x not in meetings, ['Colonial Lunch', 'Back Massage']))

## getUserMeetings
meetings = [m.title for m in getUserMeetings('ksha')]

assert not(filter(lambda x: x not in meetings, ['Colonial Lunch']))

## getUserRequestedMeetings
# Test getting the meetings where a user with netid has not yet responded
meetings = [m.title for m in getUserRequestedMeetings('gwan')]

assert not(filter(lambda x: x not in meetings, ['Back Massage', 'Code@Night']))

## getRespondedNetids
# Test getting the netids of those who have responded to meeting mid
netids = getRespondedNetids(1)
assert not(filter(lambda x: x not in netids, ['hsolis', 'gwan']))

netids = getRespondedNetids(2)
assert not(filter(lambda x: x not in netids, ['hsolis']))

netids = getRespondedNetids(4)
assert not(filter(lambda x: x not in netids, ['hsolis', 'bargotta', 'kl9']))

## getNotRespondedNetids
# Test getting the netids of those who have not yet responded
netids = getNotRespondedNetids(2)
assert not(filter(lambda x: x not in netids, ['gwan']))

netids = getNotRespondedNetids(4)
assert not(filter(lambda x: x not in netids, ['gwan', 'ksha', 'jackvw']))

## getRespondedPreferredTimes
# Test getting the preferred times of those who have responded
preferredTimes = getRespondedPreferredTimes(1)

assert not(filter(lambda x: x not in preferredTimes, \
	[[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}], [{'Day': 'Fri', 'Time': '12:00'}], [{'Day': 'Fri', 'Time': '12:00'}]]))

## getUserPreferredTimes
# Test getting the preferred times of a response given meetingid and netid
preferredTimes = getUserPreferredTimes(1, 'hsolis')

assert not(filter(lambda x: x not in preferredTimes, \
	[[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]]))