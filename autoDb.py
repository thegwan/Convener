# autoDb.py

from datetime import datetime, timedelta
import database as db

# automatically deletes meeting if it is at least numDays old
def auto_delete_meeting(meeting, numDays):
	creation_date = meeting.creationDate
	creation_dt = datetime.strptime(creation_date, '%m-%d-%Y')
	delete_dt = creation_dt + timedelta(days=numDays)
	if datetime.now() > delete_dt:
		db.deleteMeeting(meeting.mid)

# deletes all expired meetings in database
def delete_expired_meetings():
	meetings = db.getAllMeetings()
	for meeting in meetings:
		auto_delete_meeting(meeting, 10)