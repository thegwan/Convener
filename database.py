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

### Database modifying functions

# Adds a new user with a netid and other optional arguments
def createUser(netid, firstName=None, lastName=None, preferredTimes=None, acceptableTimes=None, unacceptableTimes=None):
	user = User(netid, firstName, lastName, preferredTimes, acceptableTimes, unacceptableTimes)
	db.session.add(user)
	db.session.commit()

# Creates a new meeting with a responderId, creatorId, and list in string format of preferredTimes
def createMeeting(title, creatorId, respondingId):
	meeting = Meeting(title, creatorId, respondingId)
	db.session.add(meeting)
	db.session.commit()

# Creates a new response for a meeting with meetingId
def createResponse(meetingId, responderId, preferredTimes=None, acceptableTimes=None, unacceptableTimes=None):
	response = Response(meetingId, responderId, preferredTimes, acceptableTimes, unacceptableTimes)
	db.session.add(response)
	db.session.commit()

# Updates the values saved to a user's profile
def updateUser(netid, firstName=None, lastName=None, preferredTimes=None, acceptableTimes=None, unacceptableTimes=None):
	# Queries the db for the user
	upd = (db.session.query(User).\
		filter(User.netid==netid))

	# Assuming every user has a unique netid
	updatedUser = upd.one_or_none()
	if updatedUser is None:
		return "Failed to updateUser"

	updatedUser.firstName = firstName
	updatedUser.lastName = lastName
	updatedUser.preferredTimes= preferredTimes
	updatedUser.acceptableTimes = acceptableTimes
	updatedUser.unacceptableTimes = unacceptableTimes

	db.session.commit()