## Test data for checking if the database properly works (run after creating an empty db)
import database as db
# import ast

# Testing

# Sample time strings
randomPrefTime = "[{'day': 'Sat', 'time': '9am'}, {'day': 'Sun', 'time': '10am'}]"

thursFri = "[{'date': 'Thu', 'time': '8pm'}, {'date': 'Fri', 'time': '12pm'}]"
friLunch = "[{'date': 'Fri', 'time': '12pm'}]"
wholeWeek = "[{'date': 'Mon', 'time': '6pm'}, {'date': 'Tue', 'time': '12pm'}, {'date': 'Sat', 'time': '9pm'}]"
friNight = "[{'date': 'Fri', 'time': '12am'}]"
monMorn = "[{'date': 'Mon', 'time': '11pm'}]"
wedNoon = "[{'date': 'Wed', 'time': '3pm'}]"

## Create users and check that they were properly added ###########################################
db.createUser('hsolis', 'Hector', 'Solis', thursFri)
db.createUser('gwan', 'Gerry')
db.createUser('bargotta', unacceptableTimes=friLunch)
db.createUser('ksha', lastName='Sha', acceptableTimes=friLunch)
db.createUser('kl9', 'Katherine', 'Lee', randomPrefTime)

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
	katlee.lastName == 'Lee' and katlee.preferredTimes == randomPrefTime

## Create meetings and check that they were properly added ########################################

db.createMeeting('Colonial Lunch', hector.uid, "[2, 4]", "Thu")
db.createMeeting('Back Massage', hector.uid, "[2]", "Thu")
db.createMeeting('Charter Friday', gary.uid, "[4]", "Thu")
db.createMeeting('Code@Night', katlee.uid, "[6, 2, 1, 3, 4]", "Thu")

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


db.updateUser('hsolis', 'Tear', 'Swag', randomPrefTime, \
	monMorn, wedNoon)

hector = db.getUser('hsolis')

assert hector.uid == 1 and hector.firstName == 'Tear' and \
	hector.lastName == 'Swag' and hector.preferredTimes == randomPrefTime \
	and hector.acceptableTimes == monMorn and \
	hector.unacceptableTimes == wedNoon

db.updateUser(netid='hsolis', firstName='Hector', lastName='Solis')

hector = db.getUser('hsolis')

assert hector.uid == 1 and hector.firstName == 'Hector' and \
	hector.lastName == 'Solis' and hector.preferredTimes == randomPrefTime \
	and hector.acceptableTimes == monMorn and \
	hector.unacceptableTimes == wedNoon

## Update a meeting, check if it worked ###########################################################


db.updateMeeting(mid=1, allResponded=True, scheduledTime=friLunch)

colonial = db.getMeeting(1)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]" \
	and colonial.allResponded == True and colonial.scheduledTime == friLunch \
	and colonial.notified == False

db.updateMeeting(mid=1, notified=True)

colonial = db.getMeeting(1)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]" \
	and colonial.allResponded == True and colonial.scheduledTime == friLunch \
	and colonial.notified == True


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
	[[{'date': 'Thu', 'time': '8pm'}, {'date': 'Fri', 'time': '12pm'}], [{'date': 'Fri', 'time': '12pm'}], [{'date': 'Fri', 'time': '12pm'}]]))

## getUserPreferredTimes ##########################################################################
# Test getting the preferred times of a response given meetingid and netid
preferredTimes = db.getUserPreferredTimes(1, 'hsolis')
assert sorted(preferredTimes) == sorted([{'date': 'Thu', 'time': '8pm'}, {'date': 'Fri', 'time': '12pm'}])


## Extra data points for demo #####################################################################

db.createMeeting('333 Project Meeting', gary.uid, "[1, 3]", "Thu")
db.createMeeting('WeightLifting', gary.uid, "[1]", "Thu")
db.createMeeting('Group Crying', hector.uid, "[6]", "Thu")

db.updateMeeting(mid=7, allResponded=True, notified=True)


db.createMeeting('Smash 4', hector.uid, "[2, 3, 4, 5, 6]", "Thu")
db.createMeeting('Pitch Training', gary.uid, "[1, 3]", "Thu")


db.createResponse(5, 1, "[{'date': 'Fri', 'time':  '12pm'},{'date': 'Fri', 'time':  '1pm'},{'date': 'Fri', 'time':  '2pm'},{'date': 'Fri', 'time':  '3pm'},{'date': 'Fri', 'time':  '4pm'},{'date': 'Fri', 'time':  '5pm'},{'date': 'Fri', 'time':  '6pm'},{'date': 'Thu', 'time':  '2pm'},{'date': 'Thu', 'time':  '3pm'},{'date': 'Thu', 'time':  '4pm'},{'date': 'Thu', 'time':  '5pm'},{'date': 'Thu', 'time':  '6pm'},{'date': 'Wed', 'time':  '2pm'},{'date': 'Wed', 'time':  '3pm'}]")
db.createResponse(5, 2, "[{'date': 'Sat', 'time':  '6pm'},{'date': 'Sat', 'time':  '2pm'},{'date': 'Sat', 'time':  '1pm'},{'date': 'Fri', 'time':  '2pm'},{'date': 'Fri', 'time':  '3pm'}]")
db.createResponse(5, 4, "[{'date': 'Tue', 'time': '3pm'},{'date': 'Fri', 'time':  '2pm'},{'date': 'Fri', 'time':  '3pm'},{'date': 'Sat', 'time':  '2pm'}]")

db.createResponse(6, 2,  "[{'date': 'Mon', 'time': '3pm'}, {'date': 'Mon', 'time': '9am'}, {'date': 'Tue', 'time': '11am'}, {'date': 'Wed', 'time': '12pm'}, {'date': 'Thu', 'time': '10am'}, {'date': 'Fri', 'time': '11am'}, {'date': 'Sat', 'time': '11am'}]")

db.createResponse(7, 1,  "[{'date': 'Sun', 'time': '2am'}, {'date': 'Mon', 'time': '2am'}, {'date': 'Tue', 'time': '2am'}, {'date': 'Wed', 'time': '2am'}, {'date': 'Thu', 'time': '2am'}, {'date': 'Fri', 'time': '2am'}]")
db.createResponse(7, 6,  "[{'date': 'Sun', 'time': '2am'}, {'date': 'Mon', 'time': '2am'}, {'date': 'Tue', 'time': '2am'}, {'date': 'Wed', 'time': '2am'}, {'date': 'Thu', 'time': '2am'}, {'date': 'Fri', 'time': '2am'}]")


db.createResponse(8, 1,  "[{'date': 'Wed', 'time': '12am'},{'date': 'Mon', 'time': '1am'},{'date': 'Sat', 'time': '1am'},{'date': 'Tue', 'time': '2am'},{'date': 'Fri', 'time': '2am'},{'date': 'Sun', 'time': '3am'},{'date': 'Tue', 'time': '3am'},{'date': 'Thu', 'time': '3am'},{'date': 'Sat', 'time': '3am'},{'date': 'Wed', 'time': '5am'},{'date': 'Mon', 'time': '6am'},{'date': 'Tue', 'time': '7am'},{'date': 'Wed', 'time': '7am'},{'date': 'Fri', 'time': '7am'},{'date': 'Sat', 'time': '7am'},{'date': 'Tue', 'time': '8am'},{'date': 'Thu', 'time': '8am'},{'date': 'Sun', 'time': '9am'},{'date': 'Wed', 'time': '9am'},{'date': 'Fri', 'time': '9am'},{'date': 'Sun', 'time': '10am'},{'date': 'Sun', 'time': '11am'},{'date': 'Thu', 'time': '11am'},{'date': 'Sat', 'time': '11am'},{'date': 'Tue', 'time': '12pm'},{'date': 'Wed', 'time': '1pm'},{'date': 'Fri', 'time': '1pm'},{'date': 'Sun', 'time': '2pm'},{'date': 'Mon', 'time': '2pm'},{'date': 'Thu', 'time': '2pm'},{'date': 'Tue', 'time': '3pm'},{'date': 'Tue', 'time': '4pm'},{'date': 'Thu', 'time': '4pm'},{'date': 'Fri', 'time': '4pm'},{'date': 'Sat', 'time': '4pm'},{'date': 'Sun', 'time': '5pm'},{'date': 'Fri', 'time': '5pm'},{'date': 'Sun', 'time': '6pm'},{'date': 'Tue', 'time': '6pm'},{'date': 'Wed', 'time': '6pm'},{'date': 'Fri', 'time': '6pm'},{'date': 'Sun', 'time': '7pm'},{'date': 'Thu', 'time': '7pm'},{'date': 'Sat', 'time': '7pm'},{'date': 'Mon', 'time': '8pm'},{'date': 'Fri', 'time': '8pm'},{'date': 'Sun', 'time': '9pm'},{'date': 'Tue', 'time': '9pm'},{'date': 'Thu', 'time': '9pm'},{'date': 'Sat', 'time': '9pm'},{'date': 'Mon', 'time': '10pm'},{'date': 'Wed', 'time': '10pm'},{'date': 'Sun', 'time': '11pm'}]")
db.createResponse(8, 3,  "[{'date': 'Sun', 'time': '12am'},{'date': 'Wed', 'time': '12am'},{'date': 'Thu', 'time': '12am'},{'date': 'Mon', 'time': '1am'},{'date': 'Sat', 'time': '1am'},{'date': 'Tue', 'time': '2am'},{'date': 'Fri', 'time': '2am'},{'date': 'Sun', 'time': '3am'},{'date': 'Tue', 'time': '3am'},{'date': 'Thu', 'time': '3am'},{'date': 'Sat', 'time': '3am'},{'date': 'Sun', 'time': '5am'},{'date': 'Wed', 'time': '5am'},{'date': 'Sun', 'time': '6am'},{'date': 'Mon', 'time': '6am'},{'date': 'Thu', 'time': '6am'},{'date': 'Tue', 'time': '7am'},{'date': 'Wed', 'time': '7am'},{'date': 'Fri', 'time': '7am'},{'date': 'Sat', 'time': '7am'},{'date': 'Tue', 'time': '8am'},{'date': 'Thu', 'time': '8am'},{'date': 'Sun', 'time': '9am'},{'date': 'Wed', 'time': '9am'},{'date': 'Fri', 'time': '9am'},{'date': 'Sun', 'time': '10am'},{'date': 'Mon', 'time': '10am'},{'date': 'Wed', 'time': '10am'},{'date': 'Sun', 'time': '11am'},{'date': 'Wed', 'time': '11am'},{'date': 'Thu', 'time': '11am'},{'date': 'Sat', 'time': '11am'},{'date': 'Mon', 'time': '12pm'},{'date': 'Tue', 'time': '12pm'},{'date': 'Wed', 'time': '1pm'},{'date': 'Fri', 'time': '1pm'},{'date': 'Sun', 'time': '2pm'},{'date': 'Tue', 'time': '2pm'},{'date': 'Thu', 'time': '2pm'},{'date': 'Mon', 'time': '3pm'},{'date': 'Tue', 'time': '3pm'},{'date': 'Wed', 'time': '3pm'},{'date': 'Fri', 'time': '3pm'},{'date': 'Mon', 'time': '4pm'},{'date': 'Tue', 'time': '4pm'},{'date': 'Thu', 'time': '4pm'},{'date': 'Fri', 'time': '4pm'},{'date': 'Sat', 'time': '4pm'},{'date': 'Sun', 'time': '5pm'},{'date': 'Mon', 'time': '5pm'},{'date': 'Tue', 'time': '5pm'},{'date': 'Wed', 'time': '5pm'},{'date': 'Fri', 'time': '5pm'},{'date': 'Sun', 'time': '6pm'},{'date': 'Mon', 'time': '6pm'},{'date': 'Tue', 'time': '6pm'},{'date': 'Wed', 'time': '6pm'},{'date': 'Fri', 'time': '6pm'},{'date': 'Sun', 'time': '7pm'},{'date': 'Thu', 'time': '7pm'},{'date': 'Sat', 'time': '7pm'},{'date': 'Mon', 'time': '8pm'},{'date': 'Wed', 'time': '8pm'},{'date': 'Fri', 'time': '8pm'},{'date': 'Sat', 'time': '8pm'},{'date': 'Sun', 'time': '9pm'},{'date': 'Tue', 'time': '9pm'},{'date': 'Wed', 'time': '9pm'},{'date': 'Thu', 'time': '9pm'},{'date': 'Fri', 'time': '9pm'},{'date': 'Sat', 'time': '9pm'},{'date': 'Mon', 'time': '10pm'},{'date': 'Tue', 'time': '10pm'},{'date': 'Wed', 'time': '10pm'},{'date': 'Thu', 'time': '10pm'},{'date': 'Fri', 'time': '10pm'},{'date': 'Sat', 'time': '10pm'},{'date': 'Sun', 'time': '11pm'},{'date': 'Mon', 'time': '11pm'},{'date': 'Tue', 'time': '11pm'},{'date': 'Wed', 'time': '11pm'},{'date': 'Thu', 'time': '11pm'},{'date': 'Fri', 'time': '11pm'},{'date': 'Sat', 'time': '11pm'}]")
db.createResponse(8, 2,  "[{'date': 'Sat', 'time': '1am'},{'date': 'Sat', 'time': '3am'},{'date': 'Sat', 'time': '7am'},{'date': 'Thu', 'time': '8am'},{'date': 'Sun', 'time': '9am'},{'date': 'Wed', 'time': '9am'},{'date': 'Fri', 'time': '9am'},{'date': 'Sun', 'time': '10am'},{'date': 'Mon', 'time': '10am'},{'date': 'Wed', 'time': '10am'},{'date': 'Sun', 'time': '11am'},{'date': 'Wed', 'time': '11am'},{'date': 'Thu', 'time': '11am'},{'date': 'Sat', 'time': '11am'},{'date': 'Mon', 'time': '12pm'},{'date': 'Tue', 'time': '12pm'},{'date': 'Wed', 'time': '1pm'},{'date': 'Fri', 'time': '1pm'},{'date': 'Sun', 'time': '2pm'},{'date': 'Thu', 'time': '2pm'},{'date': 'Mon', 'time': '3pm'},{'date': 'Wed', 'time': '3pm'},{'date': 'Thu', 'time': '4pm'},{'date': 'Sat', 'time': '4pm'},{'date': 'Tue', 'time': '6pm'},{'date': 'Sun', 'time': '7pm'},{'date': 'Thu', 'time': '7pm'},{'date': 'Mon', 'time': '8pm'},{'date': 'Wed', 'time': '8pm'},{'date': 'Sun', 'time': '9pm'},{'date': 'Tue', 'time': '9pm'},{'date': 'Sun', 'time': '11pm'}]")
db.createResponse(8, 4,  "[{'date': 'Mon', 'time': '12am'},{'date': 'Wed', 'time': '12am'},{'date': 'Thu', 'time': '12am'},{'date': 'Fri', 'time': '12am'},{'date': 'Sun', 'time': '1am'},{'date': 'Mon', 'time': '1am'},{'date': 'Wed', 'time': '1am'},{'date': 'Thu', 'time': '1am'},{'date': 'Fri', 'time': '1am'},{'date': 'Sat', 'time': '1am'},{'date': 'Sun', 'time': '2am'},{'date': 'Fri', 'time': '2am'},{'date': 'Tue', 'time': '3am'},{'date': 'Wed', 'time': '3am'},{'date': 'Thu', 'time': '3am'},{'date': 'Sat', 'time': '3am'},{'date': 'Sun', 'time': '4am'},{'date': 'Tue', 'time': '4am'},{'date': 'Fri', 'time': '4am'},{'date': 'Sat', 'time': '4am'},{'date': 'Mon', 'time': '5am'},{'date': 'Thu', 'time': '5am'},{'date': 'Tue', 'time': '6am'},{'date': 'Wed', 'time': '6am'},{'date': 'Fri', 'time': '6am'},{'date': 'Sat', 'time': '6am'},{'date': 'Thu', 'time': '7am'},{'date': 'Wed', 'time': '9am'},{'date': 'Sun', 'time': '10am'},{'date': 'Sat', 'time': '10am'},{'date': 'Thu', 'time': '2pm'},{'date': 'Fri', 'time': '2pm'},{'date': 'Mon', 'time': '3pm'},{'date': 'Thu', 'time': '4pm'},{'date': 'Tue', 'time': '6pm'},{'date': 'Thu', 'time': '7pm'},{'date': 'Mon', 'time': '8pm'},{'date': 'Wed', 'time': '8pm'},{'date': 'Fri', 'time': '8pm'},{'date': 'Sun', 'time': '9pm'},{'date': 'Tue', 'time': '9pm'},{'date': 'Fri', 'time': '9pm'},{'date': 'Mon', 'time': '10pm'},{'date': 'Wed', 'time': '10pm'},{'date': 'Thu', 'time': '10pm'},{'date': 'Fri', 'time': '10pm'},{'date': 'Sat', 'time': '10pm'},{'date': 'Sun', 'time': '11pm'},{'date': 'Tue', 'time': '11pm'}]")
db.createResponse(8, 5,  "[{'date': 'Sun', 'time': '3am'},{'date': 'Tue', 'time': '3am'},{'date': 'Thu', 'time': '3am'},{'date': 'Fri', 'time': '3am'},{'date': 'Sun', 'time': '4am'},{'date': 'Tue', 'time': '4am'},{'date': 'Thu', 'time': '4am'},{'date': 'Fri', 'time': '4am'},{'date': 'Sun', 'time': '5am'},{'date': 'Tue', 'time': '5am'},{'date': 'Thu', 'time': '5am'},{'date': 'Fri', 'time': '5am'},{'date': 'Sun', 'time': '6am'},{'date': 'Tue', 'time': '6am'},{'date': 'Thu', 'time': '6am'},{'date': 'Fri', 'time': '6am'},{'date': 'Sun', 'time': '7am'},{'date': 'Tue', 'time': '7am'},{'date': 'Sun', 'time': '8am'},{'date': 'Tue', 'time': '8am'},{'date': 'Sun', 'time': '9am'},{'date': 'Mon', 'time': '9am'},{'date': 'Tue', 'time': '9am'},{'date': 'Wed', 'time': '9am'},{'date': 'Fri', 'time': '9am'},{'date': 'Sun', 'time': '10am'},{'date': 'Tue', 'time': '10am'},{'date': 'Thu', 'time': '10am'},{'date': 'Fri', 'time': '10am'},{'date': 'Sun', 'time': '11am'},{'date': 'Tue', 'time': '11am'},{'date': 'Thu', 'time': '11am'},{'date': 'Fri', 'time': '11am'},{'date': 'Sun', 'time': '12pm'},{'date': 'Tue', 'time': '12pm'},{'date': 'Thu', 'time': '12pm'},{'date': 'Sun', 'time': '1pm'},{'date': 'Tue', 'time': '1pm'},{'date': 'Thu', 'time': '1pm'},{'date': 'Fri', 'time': '1pm'},{'date': 'Sun', 'time': '2pm'},{'date': 'Tue', 'time': '2pm'},{'date': 'Thu', 'time': '2pm'},{'date': 'Fri', 'time': '2pm'},{'date': 'Sun', 'time': '3pm'},{'date': 'Tue', 'time': '3pm'},{'date': 'Thu', 'time': '3pm'},{'date': 'Fri', 'time': '3pm'},{'date': 'Sun', 'time': '4pm'},{'date': 'Tue', 'time': '4pm'},{'date': 'Thu', 'time': '4pm'},{'date': 'Fri', 'time': '4pm'},{'date': 'Sun', 'time': '5pm'},{'date': 'Tue', 'time': '5pm'},{'date': 'Thu', 'time': '5pm'},{'date': 'Fri', 'time': '5pm'}]")
db.createResponse(8, 6,  "[{'date': 'Wed', 'time': '3am'},{'date': 'Tue', 'time': '5am'},{'date': 'Thu', 'time': '6am'},{'date': 'Fri', 'time': '6am'},{'date': 'Mon', 'time': '8am'},{'date': 'Wed', 'time': '9am'},{'date': 'Mon', 'time': '12pm'},{'date': 'Thu', 'time': '1pm'},{'date': 'Wed', 'time': '2pm'},{'date': 'Fri', 'time': '5pm'},{'date': 'Mon', 'time': '7pm'}]")

db.createResponse(9, 2,  "[{'date': 'Wed', 'time': '3am'},{'date': 'Tue', 'time': '5am'},{'date': 'Thu', 'time': '6am'},{'date': 'Fri', 'time': '6am'},{'date': 'Mon', 'time': '8am'},{'date': 'Wed', 'time': '9am'},{'date': 'Mon', 'time': '12pm'},{'date': 'Thu', 'time': '1pm'},{'date': 'Wed', 'time': '2pm'},{'date': 'Fri', 'time': '5pm'},{'date': 'Mon', 'time': '7pm'}]")
