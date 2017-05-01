# run after runninng python sampleDatabase.py
import json, db2server, server2db, database

#-------------------------------------------------------------------------------
# tests if db2server gives the correct initial data

init_data_gwan = db2server.init_protocol("gwan")
with open('test_initgwan.json') as data_file:
	gwan_init = json.load(data_file)
print sorted(init_data_gwan.items()) == sorted(gwan_init.items())

init_data_hsolis = db2server.init_protocol("hsolis")
with open('test_inithsolis.json') as data_file:
	hsolis_init = json.load(data_file)
print sorted(init_data_hsolis.items()) == sorted(hsolis_init.items())

#-------------------------------------------------------------------------------
# tests if server2db inputs information into the database correctly

# sample creation
jpost1 = {u'category': 'creation', u'title': 'The Olympics', u'response': [{u'date': u'04-18-2017', u'time': u'4:00pm'}], u'netid': u'gwan', u'responders': [u'hsolis'], u'creationDate': '04-17-2017'}
# sample response
jpost2 = {u'category': 'response', u'mid': 5, u'response': [{'date': '04-22-2017', 'time': '9:00am'}], u'netid': u'gwan'}
# sample decision
jpost3 = {u'category': 'decision', u'mid': 5, u'finalTime': [{'date': '04-22-2017', 'time': '9:00am'}], u'netid': u'bargotta'}
# sample update preferred times
jpost4 = {u'category': 'updatePref', u'preferredTimes': [{'day': 'Sat', 'time': '9:00am'}, {'day': 'Sun', 'time': '10:30am'}], u'netid': u'hsolis'}
# sample meeting deletion
jpost5 = {u'category': 'meetingDelete', u'mid': 3, u'netid': 'gwan'}


#----------------------------------------------------------
# creation

status = server2db.parse(jpost1)
print status == True

olympics = database.getMeeting(6)
print olympics.mid == 6
print olympics.title == 'The Olympics'
print olympics.creatorId == 2
print olympics.respondingId == "[1]"
print olympics.creationDate == '04-17-2017'

#----------------------------------------------------------
# response

status = server2db.parse(jpost2)
print status == True

rsp = database.getResponse(5, 2)
print rsp.meetingId == 5
print rsp.responderId == 2
print rsp.preferredTimes == "[{'date': '04-22-2017', 'time': '9:00am'}]"
print rsp.rid == 15

#----------------------------------------------------------
# decision

status = server2db.parse(jpost3)
print status == True

test5 = database.getMeeting(5)
print test5.mid == 5
print test5.allResponded == True
print test5.scheduledTime == "[{'date': '04-22-2017', 'time': '9:00am'}]"
print test5.creatorId == 3

#----------------------------------------------------------
# update pref times

hector = database.getUser('hsolis')
print hector.preferredTimes == ""

status = server2db.parse(jpost4)
print status == True

print hector.preferredTimes == "[{'day': 'Sat', 'time': '9:00am'}, {'day': 'Sun', 'time': '10:30am'}]"

#----------------------------------------------------------
# delete meeting

test3 = database.getMeeting(3)
print test3.title == 'test3'

status = server2db.parse(jpost5)
print status == True

print database.getMeeting(3) == None

#-------------------------------------------------------------------------------
# tests to make sure bad information is not stored into database

def db_state_unchanged():
	return database.getMeeting(7) == None and \
		   database.getResponse(6, 1) == None and \
		   database.getMeeting(5).scheduledTime == "[{'date': '04-22-2017', 'time': '9:00am'}]" and \
		   database.getUser('hsolis').preferredTimes == "[{'day': 'Sat', 'time': '9:00am'}, {'day': 'Sun', 'time': '10:30am'}]" and \
		   database.getMeeting(2).title == 'test2'



#----------------------------------------------------------
# wrong category 

# sample bad creation
jpost6 = {u'category': 'reation', u'title': 'The Olympics', u'response': [{u'date': u'04-18-2017', u'time': u'4:00pm'}], u'netid': u'gwan', u'responders': [u'hsolis'], u'creationDate': '04-17-2017'}
# sample bad response
jpost7 = {u'category': 'respone', u'mid': 6, u'response': [{'date': '04-18-2017', 'time': '4:00pm'}], u'netid': u'hsolis'}
# sample bad decision
jpost8 = {u'category': 'decisio', u'mid': 5, u'finalTime': [{'date': '04-21-2017', 'time': '8:00am'}], u'netid': u'bargotta'}
# sample bad update preferred times
jpost9 = {u'category': 'update Pref', u'preferredTimes': [{'day': 'Sun', 'time': '10:00pm'}, {'day': 'Mon', 'time': '10:30am'}], u'netid': u'hsolis'}
# sample bad meeting deletion
jpost10 = {u'category': 'MeetingDelete', u'mid': 2, u'netid': 'gwan'}

print server2db.parse(jpost6) == False
print server2db.parse(jpost7) == False
print server2db.parse(jpost8) == False
print server2db.parse(jpost9) == False
print server2db.parse(jpost10) == False

print db_state_unchanged()

#----------------------------------------------------------
# wrong types

# sample bad creation
jpost11 = {u'category': 'creation', u'title': 2, u'response': [{u'date': u'04-18-2017', u'time': u'4:00pm'}], u'netid': u'gwan', u'responders': [u'hsolis'], u'creationDate': '04-17-2017'}
# sample bad response
jpost12 = {u'category': 'response', u'mid': "hello", u'response': [{'day': '04-18-2017', 'time': '4:00pm'}], u'netid': u'hsolis'}
# sample bad decision
jpost13 = {u'category': 'decision', u'mid': 5, u'finalTime': [{'date': '04-21-2017', 'times': '8:00am'}], u'netid': 4}
# sample bad update preferred times
jpost14 = {u'category': 'updatePref', 5: [{'day': 'Sun', 'time': '10:00pm'}, {'day': 'Mon', 'time': '10:30am'}], u'netid': u'hsolis'}
# sample bad meeting deletion
jpost15 = {u'category': 'meetingDelete', 'hello': 2, u'netid': 'gwan'}

print server2db.parse(jpost11) == False
print server2db.parse(jpost12) == False
print server2db.parse(jpost13) == False
print server2db.parse(jpost14) == False
print server2db.parse(jpost15) == False

print db_state_unchanged()

#----------------------------------------------------------
# wrong formatting

# sample bad creation
jpost16 = {u'category': 'creation', u'title': 'The Olympics', u'response': [{u'date': u'04/18/2017', u'time': u'4:00pm'}], u'netid': u'gwan', u'responders': [u'hsolis'], u'creationDate': '04-17-2017'}
# sample bad response
jpost17 = {u'category': 'response', u'mid': 6, u'response': [{'date': '04-18-17', 'time': '4:00pm'}], u'netid': u'hsolis'}
# sample bad decision
jpost18 = {u'category': 'decision', u'mid': 5, u'finalTime': [{'date': '04-21-2017', 'time': '8am'}], u'netid': u'bargotta'}
# sample bad update preferred times
jpost19 = {u'category': 'updatePref', u'preferredTimes': [{'day': 'Sun', 'time': '10:00 pm'}, {'day': 'Mon', 'time': '10:30am'}], u'netid': u'hsolis'}
# sample bad meeting deletion
jpost20 = {u'category': 'meetingDelete', u'mid': 2, u'netid': 'gwan'}

print server2db.parse(jpost16) == False
print server2db.parse(jpost17) == False
print server2db.parse(jpost18) == False
print server2db.parse(jpost19) == False
print server2db.parse(jpost20) == False

print db_state_unchanged()

#----------------------------------------------------------
# deleting meeting you don't own

jpost21 = {u'category': 'meetingDelete', u'mid': 2, u'netid': 'bargotta'}
print server2db.parse(jpost21) == False
print database.getMeeting(2).title == 'test2'

#----------------------------------------------------------
# response when it already exists

jpost22 = {u'category': 'response', u'mid': 4, u'response': [{'date': '04-18-2017', 'time': '4:00pm'}], u'netid': u'hsolis'}
print server2db.parse(jpost22) == False
print database.getResponse(4,1) == 10