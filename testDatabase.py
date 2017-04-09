## Test data for checking if the database properly works (run after creating an empty db)
import database as db
# import ast

# Testing

# Sample time strings
thursFri = "[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]"
friLunch = "[{'Day': 'Fri', 'Time': '12:00'}]"
wholeWeek = "[{'Day': 'Mon', 'Time': '18:00'}, {'Day': 'Tue', 'Time': '12:00'}, {'Day': 'Sat', 'Time': '9:00'}]"
friNight = "[{'Day': 'Fri', 'Time': '20:00'}]"
monMorn = "[{'Day': 'Mon', 'Time': '11:00'}]"
wedNoon = "[{'Day': 'Wed', 'Time': '3:00'}]"

## Create users and check that they were properly added ###########################################
db.createUser('hsolis', 'Hector', 'Solis', thursFri)
db.createUser('gwan', 'Gerry')
db.createUser('bargotta', unacceptableTimes=friLunch)
db.createUser('ksha', lastName='Sha', acceptableTimes=friLunch)
db.createUser('kl9', 'Katherine', 'Lee', wholeWeek)

hector = db.getUser('hsolis')
gary = db.getUser('gwan')
aaron = db.getUser('bargotta')
kim = db.getUserFromId(4)
katlee = db.getUserFromId(5)

assert hector.uid == 1 and hector.firstName == 'Hector' and \
	hector.lastName == 'Solis' and hector.preferredTimes == thursFri

assert gary.uid == 2 and gary.firstName == 'Gerry' and \
	gary.lastName == None and gary.preferredTimes == None

assert aaron.uid == 3 and aaron.firstName == None and \
	aaron.lastName == None and aaron.unacceptableTimes == friLunch

assert kim.uid == 4 and kim.firstName == None and \
	kim.lastName == 'Sha' and kim.acceptableTimes == friLunch

assert katlee.uid == 5 and katlee.firstName == 'Katherine' and \
	katlee.lastName == 'Lee' and katlee.preferredTimes == wholeWeek

## Create meetings and check that they were properly added ########################################

db.createMeeting('Colonial Lunch', hector.uid, "[2, 4]")
db.createMeeting('Back Massage', hector.uid, "[2]")
db.createMeeting('Charter Friday', gary.uid, "[4]")
db.createMeeting('Code@Night', katlee.uid, "[6, 2, 1, 3, 4]")

colonial = db.getMeeting(1)
massage = db.getMeeting(2)
charter = db.getMeeting(3)
code = db.getMeeting(4)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]"

assert massage.mid == 2 and massage.title == 'Back Massage' and \
	massage.creatorId == hector.uid and massage.respondingId == "[2]"

assert charter.mid == 3 and charter.title == 'Charter Friday' and \
	charter.creatorId == gary.uid and charter.respondingId == "[4]"

assert code.mid == 4 and code.title == 'Code@Night' and \
	code.creatorId == katlee.uid and code.respondingId == "[6, 2, 1, 3, 4]"


## Create responses and check them ################################################################


db.createResponse(1, 1, thursFri)
db.createResponse(1, 2, thursFri)
db.createResponse(1, 4, friLunch)

db.createResponse(2, 1,  friLunch)
db.createResponse(3, 2,  friLunch)

db.createResponse(4, 5,  friNight)
db.createResponse(4, 1,  friNight)
db.createResponse(4, 3,  friNight)

rsp1 = db.getResponse(1, 1)
rsp2 = db.getResponse(1, 2)
rsp3 = db.getResponse(1, 4)
rsp4 = db.getResponse(2, 1)
rsp5 = db.getResponse(3, 2)
rsp6 = db.getResponse(4, 5)
rsp7 = db.getResponse(4, 1)
rsp8 = db.getResponse(4, 3)

assert rsp1.preferredTimes == thursFri
assert rsp2.preferredTimes == thursFri
assert rsp3.preferredTimes == friLunch

assert rsp4.preferredTimes == friLunch
assert rsp5.preferredTimes == friLunch

assert rsp6.preferredTimes == friNight
assert rsp7.preferredTimes == friNight
assert rsp8.preferredTimes == friNight

## Update a user, check if it worked ##############################################################


db.updateUser('hsolis', 'Tear', 'Swag', friLunch, \
	monMorn, wedNoon)

hector = db.getUser('hsolis')

assert hector.uid == 1 and hector.firstName == 'Tear' and \
	hector.lastName == 'Swag' and hector.preferredTimes == friLunch \
	and hector.acceptableTimes == monMorn and \
	hector.unacceptableTimes == wedNoon

## Update a meeting, check if it worked ###########################################################


db.updateMeeting(1, True, friLunch)

colonial = db.getMeeting(1)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]" \
	and colonial.allResponded == True and colonial.scheduledTime == friLunch

## Make sure you can still add users who are late to the party ####################################

db.createUser('jackvw', 'Jack', 'Wolfgramm')


## Extraneous function testing ####################################################################

## getUserCreatedMeetings #########################################################################

meetings = [m.title for m in db.getUserCreatedMeetings('hsolis')]
# Check that the meetings in meetings are the same as the ones by hector
assert sorted(meetings) == sorted(['Colonial Lunch', 'Back Massage'])

meetings = [m.title for m in db.getUserCreatedMeetings('gwan')]
assert sorted(meetings) == sorted(['Charter Friday'])

meetings = [m.title for m in db.getUserCreatedMeetings('bargotta')]
assert sorted(meetings) == sorted([])

meetings = [m.title for m in db.getUserCreatedMeetings('ksha')]
assert sorted(meetings) == sorted([])

meetings = [m.title for m in db.getUserCreatedMeetings('kl9')]
assert sorted(meetings) == sorted(['Code@Night'])

meetings = [m.title for m in db.getUserCreatedMeetings('jackvw')]
assert sorted(meetings) == sorted([])


## getUserMeetings ################################################################################

meetings = [m.title for m in db.getUserMeetings('hsolis')]
assert sorted(meetings) == sorted(['Colonial Lunch','Back Massage', 'Code@Night'])

meetings = [m.title for m in db.getUserMeetings('gwan')]
assert sorted(meetings) == sorted(['Colonial Lunch', 'Charter Friday'])

meetings = [m.title for m in db.getUserMeetings('bargotta')]
assert sorted(meetings) == sorted(['Code@Night'])

meetings = [m.title for m in db.getUserMeetings('ksha')]
assert sorted(meetings) == sorted(['Colonial Lunch'])

meetings = [m.title for m in db.getUserMeetings('kl9')]
assert sorted(meetings) == sorted(['Code@Night'])

meetings = [m.title for m in db.getUserMeetings('jackvw')]
assert sorted(meetings) == sorted([])

## getUserRequestedMeetings #######################################################################

# Test getting the meetings where a user with netid has not yet responded
meetings = [m.title for m in db.getUserRequestedMeetings('hsolis')]
assert sorted(meetings) == sorted([])

meetings = [m.title for m in db.getUserRequestedMeetings('gwan')]
assert sorted(meetings) == sorted(['Back Massage', 'Code@Night'])

meetings = [m.title for m in db.getUserRequestedMeetings('bargotta')]
assert sorted(meetings) == sorted([])

meetings = [m.title for m in db.getUserRequestedMeetings('ksha')]
assert sorted(meetings) == sorted(['Code@Night', 'Charter Friday'])

meetings = [m.title for m in db.getUserRequestedMeetings('kl9')]
assert sorted(meetings) == sorted([])

meetings = [m.title for m in db.getUserRequestedMeetings('jackvw')]
assert sorted(meetings) == sorted(['Code@Night'])

## getRespondedNetids #############################################################################

# Test getting the netids of those who have responded to meeting mid
netids = db.getRespondedNetids(1)
assert sorted(netids) == sorted(['hsolis', 'gwan', 'ksha'])

netids = db.getRespondedNetids(2)
assert sorted(netids) == sorted(['hsolis'])

netids = db.getRespondedNetids(3)
assert sorted(netids) == sorted(['gwan'])

netids = db.getRespondedNetids(4)
assert sorted(netids) == sorted(['hsolis', 'bargotta', 'kl9'])

## getNotRespondedNetids ##########################################################################

# Test getting the netids of those who have not yet responded
netids = db.getNotRespondedNetids(1)
assert sorted(netids) == sorted([])

netids = db.getNotRespondedNetids(2)
assert sorted(netids) == sorted(['gwan'])

netids = db.getNotRespondedNetids(3)
assert sorted(netids) == sorted(['ksha'])

netids = db.getNotRespondedNetids(4)
assert sorted(netids) == sorted(['gwan', 'ksha', 'jackvw'])

## getRespondedPreferredTimes #####################################################################

# Test getting the preferred times of those who have responded to meeting with mid
preferredTimes = db.getRespondedPreferredTimes(1)

assert not(filter(lambda x: x not in preferredTimes, \
	[[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}], [{'Day': 'Fri', 'Time': '12:00'}], [{'Day': 'Fri', 'Time': '12:00'}]]))

## getUserPreferredTimes ##########################################################################
# Test getting the preferred times of a response given meetingid and netid
preferredTimes = db.getUserPreferredTimes(1, 'hsolis')

assert not(filter(lambda x: x not in preferredTimes, \
	[[{'Day': 'Thu', 'Time': '8:30'}, {'Day': 'Fri', 'Time': '12:00'}]]))