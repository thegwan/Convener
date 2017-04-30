## Test data for checking if the database properly works (run after creating an empty db)
import database as db

# Testing

# Sample time strings
pref1 = "[{'day': 'Sat', 'time': '9:00am'}, {'day': 'Sun', 'time': '10:30am'}]"
pref2 = "[{'day': 'Fri', 'time': '8:00pm'}, {'day': 'Mon', 'time': '10:30am'}]"

sample1 = "[{'date': '04-29-17', 'time': '5:00pm'}, {'date': '04-30-17', 'time': '5:30pm'}]"
sample2 = "[{'date': '04-12-17', 'time': '4:30pm'}]"
sample3 = "[{'date': '04-29-17', 'time': '4:30pm'}, {'date': '04-19-17', 'time': '8:00am'}, {'date': '04-29-17', 'time': '6:00pm'}]"
sample4 = "[{'date': '04-30-17', 'time': '8:00pm'}]"
sample5 = "[{'date': '04-12-17', 'time': '2:00pm'}]"
sample6 = "[{'date': '04-19-17', 'time': '8:00am'}]"

## Create users and check that they were properly added ###########################################
db.createUser('hsolis', 'Hector', 'Solis', pref1)
db.createUser('gwan', 'Gerry')
db.createUser('bargotta', unacceptableTimes=sample2)
db.createUser('ksha', lastName='Sha', acceptableTimes=sample3)
db.createUser('kl9', 'Katherine', 'Lee', pref1)

hector = db.getUser('hsolis')
gary = db.getUser('gwan')
aaron = db.getUser('bargotta')
kim = db.getUserFromId(4)
katlee = db.getUserFromId(5)

assert hector.uid == 1 and hector.firstName == 'Hector' and \
	hector.lastName == 'Solis' and hector.preferredTimes == pref1

assert gary.uid == 2 and gary.firstName == 'Gerry' and \
	gary.lastName == None and gary.preferredTimes == None

assert aaron.uid == 3 and aaron.firstName == None and \
	aaron.lastName == None and aaron.unacceptableTimes == sample2

assert kim.uid == 4 and kim.firstName == None and \
	kim.lastName == 'Sha' and kim.acceptableTimes == sample3

assert katlee.uid == 5 and katlee.firstName == 'Katherine' and \
	katlee.lastName == 'Lee' and katlee.preferredTimes == pref1

## Create meetings and check that they were properly added ########################################

db.createMeeting('Colonial Lunch', hector.uid, "[2, 4]", "04-21-17")
db.createMeeting('Back Massage', hector.uid, "[2]", "04-21-17")
db.createMeeting('Charter Friday', gary.uid, "[4]", "04-20-17")
db.createMeeting('Code@Night', katlee.uid, "[6, 2, 1, 3, 4]", "04-19-17")

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


db.createResponse(1, 1, sample1)
db.createResponse(1, 2, sample1)
db.createResponse(1, 4, sample2)

db.createResponse(2, 1,  sample2)
db.createResponse(3, 2,  sample2)

db.createResponse(4, 5,  sample3)
db.createResponse(4, 1,  sample3)
db.createResponse(4, 3,  sample3)

rsp1 = db.getResponse(1, 1)
rsp2 = db.getResponse(1, 2)
rsp3 = db.getResponse(1, 4)
rsp4 = db.getResponse(2, 1)
rsp5 = db.getResponse(3, 2)
rsp6 = db.getResponse(4, 5)
rsp7 = db.getResponse(4, 1)
rsp8 = db.getResponse(4, 3)

assert rsp1.preferredTimes == sample1
assert rsp2.preferredTimes == sample1
assert rsp3.preferredTimes == sample2

assert rsp4.preferredTimes == sample2
assert rsp5.preferredTimes == sample2

assert rsp6.preferredTimes == sample3
assert rsp7.preferredTimes == sample3
assert rsp8.preferredTimes == sample3

## Update a user, check if it worked ##############################################################


db.updateUser('hsolis', 'Tear', 'Swag', pref2, \
	sample3, sample4)

hector = db.getUser('hsolis')

assert hector.uid == 1 and hector.firstName == 'Tear' and \
	hector.lastName == 'Swag' and hector.preferredTimes == pref2 \
	and hector.acceptableTimes == sample3 and \
	hector.unacceptableTimes == sample4

db.updateUser(netid='hsolis', firstName='Hector', lastName='Solis')

hector = db.getUser('hsolis')

assert hector.uid == 1 and hector.firstName == 'Hector' and \
	hector.lastName == 'Solis' and hector.preferredTimes == pref2 \
	and hector.acceptableTimes == sample3 and \
	hector.unacceptableTimes == sample4

## Update a meeting, check if it worked ###########################################################


db.updateMeeting(mid=1, allResponded=True, scheduledTime=sample5)

colonial = db.getMeeting(1)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]" \
	and colonial.allResponded == True and colonial.scheduledTime == sample5 \
	and colonial.notified == False

db.updateMeeting(mid=1, notified=True)

colonial = db.getMeeting(1)

assert colonial.mid == 1 and colonial.title == 'Colonial Lunch' and \
	colonial.creatorId == hector.uid and colonial.respondingId == "[2, 4]" \
	and colonial.allResponded == True and colonial.scheduledTime == sample5 \
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
