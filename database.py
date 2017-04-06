from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_#, in_
from main import app
import ast

# Allows connection to database via password
with open('secrets', 'r') as s:
	secrets = s.readlines()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + secrets[1].replace('\n','') + '@localhost/Convener'
db = SQLAlchemy(app)

###### DB Schema ################################################################################

class User(db.Model):
	uid = db.Column(db.Integer, primary_key=True)
	netid = db.Column(db.String(80), nullable=False, unique=True)
	firstName = db.Column(db.String(80))
	lastName = db.Column(db.String(80))
	preferredTimes = db.Column(db.String())
	acceptableTimes = db.Column(db.String())
	unacceptableTimes = db.Column(db.String())

	def __init__(self, netid, firstName, lastName, preferredTimes, acceptableTimes, unacceptableTimes):
		self.netid = netid
		self.firstName = firstName
		self.lastName = lastName
		self.preferredTimes = preferredTimes
		self.acceptableTimes = acceptableTimes
		self.unacceptableTimes = unacceptableTimes
		
	def __repr__(self):
		return '<User %r>' % self.netid

class Meeting(db.Model):
	mid = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), nullable=False)
	creatorId = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
	respondingId = db.Column(db.String(), nullable=False)
	allResponded = db.Column(db.Boolean(), nullable=False)
	scheduledTime = db.Column(db.String())
	notified = db.Column(db.Boolean(), nullable=False)

	def __init__(self, title, creatorId, respondingId):
		self.creatorId = creatorId
		self.title = title
		self.respondingId = respondingId
		self.allResponded = False
		self.scheduledTime = None
		self.notified = False
		
	def __repr__(self):
		return '<Meeting %r>' % self.mid

class Response(db.Model):
	rid = db.Column(db.Integer, primary_key=True)
	meetingId = db.Column(db.Integer, db.ForeignKey('meeting.mid'), nullable=False)
	responderId = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
	preferredTimes = db.Column(db.String())
	acceptableTimes = db.Column(db.String())
	unacceptableTimes = db.Column(db.String())

	def __init__(self, meetingId, responderId, preferredTimes, acceptableTimes, unacceptableTimes):
		self.meetingId = meetingId
		self.responderId = responderId
		self.preferredTimes = preferredTimes
		self.acceptableTimes = acceptableTimes
		self.unacceptableTimes = unacceptableTimes
		
	def __repr__(self):
		return '<Response %r>' % self.rid

### Database modifying functions #############################################################################################

## Create Functions: Add new rows to the database ############################################################################


# Adds a new user with a netid and other optional arguments and returns the user
def createUser(netid, firstName=None, lastName=None, preferredTimes=None, acceptableTimes=None, unacceptableTimes=None):
	return updateUser(netid, firstName, lastName, preferredTimes, acceptableTimes, unacceptableTimes)

# Creates a new meeting with a responderId, creatorId, and list in string format of preferredTimes returns the meeting
def createMeeting(title, creatorId, respondingId):
	meeting = Meeting(title, creatorId, respondingId)
	db.session.add(meeting)
	db.session.commit()
	return meeting

# Creates a new response for a meeting with meetingId and responder responderId, returns the response
def createResponse(meetingId, responderId, preferredTimes=None, acceptableTimes=None, unacceptableTimes=None):
	response = Response(meetingId, responderId, preferredTimes, acceptableTimes, unacceptableTimes)
	db.session.add(response)
	db.session.commit()
	return response

## Update Functions: Edit existing rows in the database ######################################################################

# Updates the values saved to a user's profile
def updateUser(netid, firstName=None, lastName=None, preferredTimes=None, acceptableTimes=None, unacceptableTimes=None):
	# Queries the db for the user
	upd = (db.session.query(User).\
		filter(User.netid==netid))

	# Assuming every user has a unique netid
	updatedUser = upd.one_or_none()
	if updatedUser is None:
		user = User(netid, firstName, lastName, preferredTimes, acceptableTimes, unacceptableTimes)
		db.session.add(user)
		db.session.commit()
		return user

	# Might need to change this in case this will overwrite the user's old values
	updatedUser.firstName = firstName
	updatedUser.lastName = lastName
	updatedUser.preferredTimes= preferredTimes
	updatedUser.acceptableTimes = acceptableTimes
	updatedUser.unacceptableTimes = unacceptableTimes

	db.session.commit()
	return updatedUser

# Updates the meeting values, returns the meeting if it is created or None if its not in the database
def updateMeeting(mid, allResponded=False, scheduledTime=None, notified=False):
	upd = (db.session.query(Meeting).\
		filter(Meeting.mid==mid))

	updatedMeeting = upd.one_or_none()
	if updatedMeeting is None:
		return None

	updatedMeeting.allResponded = allResponded
	updatedMeeting.scheduledTime = scheduledTime
	updatedMeeting.notified = notified

	db.session.commit()
	return updatedMeeting

## Get Functions: Retrieve data from the database ############################################################################


# Get a user from their netid, returns the user if they exist or None if they aren't in the database
def getUser(netid):
	usr = (db.session.query(User).\
		filter(User.netid==netid))

	# Assuming every user has a unique netid
	user = usr.one_or_none()
	if user is None:
		return None

	return user

# Get a user from their uid, returns the user if they exist or None if they aren't in the database
def getUserFromId(uid):
	usr = (db.session.query(User).\
		filter(User.uid==uid))

	# Assuming every user has a unique
	user = usr.one_or_none()
	if user is None:
		return None

	return user

# Get a meeting from its mid, returns the meeting if it exists or None if it does not
def getMeeting(mid):
	meet = (db.session.query(Meeting).\
		filter(Meeting.mid==mid))

	# Assuming every user has a unique netid
	meeting = meet.one_or_none()
	if meeting is None:
		return None

	return meeting

# Returns all the meetings where a user with id netid is the creator
def getUserCreatedMeetings(netid):
	user = getUser(netid)
	
	if user is None:
		return None

	meet = (db.session.query(Meeting).\
		filter(Meeting.creatorId==user.uid))

	return meet.all()

# Returns all the meetings where a user with id netid has already responded
def getUserMeetings(netid):
	user = getUser(netid)
	
	if user is None:
		return None

	userResponses = (db.session.query(Response).\
		filter(Response.responderId==user.uid))

	meetingIds = [response.meetingId for response in userResponses]

	meetings = (db.session.query(Meeting).\
		filter(Meeting.mid.in_(meetingIds)))

	return meetings

# Returns all the meetings where a user with id netid still needs to respond
def getUserRequestedMeetings(netid):
	user = getUser(netid)
	
	if user is None:
		return None

	# Note, this line is unique to Postgres, MySQL would need ('regexp') instead of ('~')
	allRequestedMeetings = (db.session.query(Meeting).\
		filter(Meeting.respondingId.op('~')('[\[|" "]' + str(user.uid) + '[,|\]]')))

	userResponses = (db.session.query(Response).\
		filter(Response.responderId==user.uid))

	respondedMeetingIds = [response.meetingId for response in userResponses]

	# Requested meeting ids that have not yet been responded to
	requestedMeetingIds = filter(lambda x: x not in respondedMeetingIds, [meeting.mid for meeting in allRequestedMeetings])

	meetings = filter(lambda x: x.mid in requestedMeetingIds, allRequestedMeetings)

	return meetings

# Returns a list of netids where all these netids respresent users who have responded to 
# meeting request mid
def getRespondedNetids(mid):
	responded = (db.session.query(Response).\
		filter(Response.meetingId==mid))

	uids = [response.responderId for response in responded]

	netids = []

	for u in uids:
		user = getUserFromId(u) 
		if user is not None:
			netids.append(user.netid)

	return netids

# Returns a list of netids where all these netids respresent users who have NOT responded to 
# meeting request mid
def getNotRespondedNetids(mid):
	responded = (db.session.query(Response).\
		filter(Response.meetingId==mid))

	respondedIds = [response.responderId for response in responded]

	netids = []
	meeting = getMeeting(mid)
	respondingId = meeting.respondingId

	stringIds = respondingId[1:len(respondingId)-1].split(",")
	numIds = [int(num) for num in stringIds]

	finalIds = filter(lambda x: x not in respondedIds, numIds)
	
	for u in finalIds:
		user = getUserFromId(u) 
		if user is not None:
			netids.append(user.netid)

	return netids

# Returns a list of lists of dicts where each list respresents one person's times response given a mid
def getRespondedPreferredTimes(mid):
	responded = (db.session.query(Response).\
		filter(Response.meetingId==mid))

	preferredTimes = [ast.literal_eval(response.preferredTimes) for response in responded]

	return preferredTimes

# Returns a list of dicts respresents one person's times response given a mid and a netid, or None if none exist
def getUserPreferredTimes(mid, netid):
	user = getUser(netid)

	if user is None:
		return None
	
	responses = (db.session.query(Response).\
		filter(and_(Response.meetingId==mid, Response.responderId==user.uid)))

	preferredTimes = [ast.literal_eval(response.preferredTimes) for response in responses]

	return preferredTimes