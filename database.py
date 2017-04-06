from flask_sqlalchemy import SQLAlchemy
from main import app

# Allows connection to database via password
with open('secrets', 'r') as s:
	secrets = s.readlines()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + secrets[1].replace('\n','') + '@localhost/Convener'
db = SQLAlchemy(app)

###### DB Schema ################################################################################

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
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
	creatorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	respondingId = db.Column(db.String(), nullable=False)
	isScheduled = db.Column(db.Boolean(), nullable=False)
	scheduledTime = db.Column(db.String())
	notified = db.Column(db.Boolean(), nullable=False)

	def __init__(self, title, creatorId, respondingId):
		self.creatorId = creatorId
		self.title = title
		self.respondingId = respondingId
		self.isScheduled = False
		self.scheduledTime = None
		self.notified = False
		
	def __repr__(self):
		return '<Meeting %r>' % self.mid

class Response(db.Model):
	rid = db.Column(db.Integer, primary_key=True)
	meetingId = db.Column(db.Integer, db.ForeignKey('meeting.mid'), nullable=False)
	responderId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
	return user

# Updates the meeting values, returns the meeting if it is created or None if its not in the database
def updateMeeting(mid, isScheduled=False, scheduledTime=None, notified=False):
	upd = (db.session.query(Meeting).\
		filter(Meeting.mid==mid))

	updatedMeeting = upd.one_or_none()
	if updatedMeeting is None:
		return None

	updatedMeeting.isScheduled = isScheduled
	updatedMeeting.scheduledTime = scheduledTime
	updatedMeeting.notified = notified

	db.session.commit()
	return meeting

# Get a user from their netid, returns the user if they exist or None if they aren't in the database
def getUser(netid):
	usr = (db.session.query(User).\
		filter(User.netid==netid))

	# Assuming every user has a unique netid
	user = usr.one_or_none()
	if user is None:
		return None

	return user

