import json, sys

# GetMeetings object to parse json from backend and get meetings to 
# display on index page
class GetMeetings(object):

	def __init__(self, meetingJSON):
		parsedJSON = json.loads(meetingJSON)
		self.my_meetings = self.getMyMeetings(parsedJSON)
		self.confirmed = self.getConfirmed(parsedJSON)
		self.pending = self.getPending(parsedJSON)
		self.my_requests = self.getMyRequests(parsedJSON)

	# returns a string with my_meetings formatted 
	def getMyMeetings(self, parsedJSON):
		content = ""
		# iterated through my_meetings and format meeting details
		for meeting in parsedJSON.get("my_meetings"):
			# title
			content += "title: " + meeting.get("title")
			# people who have responded
			content += "<br/>responded:"
			for responded in meeting.get("resp_netids"):
				content += " " + responded
			# has everyone responded?
			content += "<br/>all responded: " + str(meeting.get("all_responded"))
			# who hasn't responded
			content += "<br/>not responded:"
			for notResponded in meeting.get("nresp_netids"):
				content += " " + notResponded
			# responded times
			content += "<br/>times:"
			for response in meeting.get("times"):
				content += "<br/>" + response.get("Day") + " " + response.get("Time")
			content += "<br/><br/>"
		return content

	def getConfirmed(self, parsedJSON):
		content = ""
		# iterated through my_requests and format meeting details
		for meeting in parsedJSON.get("confirmed"):
			# title
			content += "title: " + meeting.get("title")
			# creator
			content += "<br/>creator: " + meeting.get("creator")
			# mine
			content += "<br/>mine: " + str(meeting.get("mine"))
			# responded times so far
			content += "<br/>times:"
			for response in meeting.get("times"):
				content += "<br/>" + response.get("Day") + " " + response.get("Time")
			content += "<br/><br/>"
		return content

	def getPending(self, parsedJSON):
		content = ""
		# iterated through my_requests and format meeting details
		for meeting in parsedJSON.get("pending"):
			# title
			content += "title: " + meeting.get("title")
			# creator
			content += "<br/>creator: " + meeting.get("creator")
			# mine
			content += "<br/>mine: " + str(meeting.get("mine"))
			# responded times so far
			content += "<br/>times:"
			for response in meeting.get("times"):
				content += "<br/>" + response.get("Day") + " " + response.get("Time")
			content += "<br/><br/>"
		return content

	def getMyRequests(self, parsedJSON):
		content = ""
		# iterated through my_requests and format meeting details
		for meeting in parsedJSON.get("my_requests"):
			# title
			content += "title: " + meeting.get("title")
			# creator
			content += "<br/>creator: " + meeting.get("creator") + "<br/><br/>"
		return content

# ---------------------------------------- Testing -----------------------------------------

# test json data
init_data = json.dumps({"confirmed": [
						    {
						      "creator": "hsolis", 
						      "mine": True, 
						      "times": [
						          {
						            "Day": "Thu", 
						            "Time": "8:30"
						          }, 
						          {
						            "Day": "Fri", 
						            "Time": "12:00"
						          }
						      ], 
						      "title": "Colonial Lunch"
						    }
						  ], 
						  "my_meetings": [
						    {
						      "all_responded": False, 
						      "nresp_netids": [
						        "gwan"
						      ], 
						      "resp_netids": [
						        "hsolis"
						      ], 
						      "times": [
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }
						      ], 
						      "title": "Back Massage"
						    }, 
						    {
						      "all_responded": True, 
						      "nresp_netids": [], 
						      "resp_netids": [
						        "hsolis", 
						        "gwan", 
						        "ksha"
						      ], 
						      "times": [
						        {
						          "Day": "Thu", 
						          "Time": "8:30"
						        }, 
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }, 
						        {
						          "Day": "Thu", 
						          "Time": "8:30"
						        }, 
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }, 
						        {
						          "Day": "Fri", 
						          "Time": "12:00"
						        }
						      ], 
						      "title": "Colonial Lunch"
						    }
						  ], 
						  "my_requests": [
						    {
						      "creator": "gwan", 
						      "title": "Charter Friday"
						    }, 
						    {
						      "creator": "kl9", 
						      "title": "Code@Night"
						    }
						  ], 
						  "pending": [
						    {
						      "creator": "hsolis", 
						      "mine": True, 
						      "times": [
						          {
						            "Day": "Fri", 
						            "Time": "12:00"
						          }
						      ], 
						      "title": "Back Massage"
						    }, 
						    {
						      "creator": "kl9", 
						      "mine": False, 
						      "times": [
						          {
						            "Day": "Fri", 
						            "Time": "20:00"
						          }
						      ], 
						      "title": "Code@Night"
						    }
						  ]
						})

# test that GetMeetings works for json above
# test = GetMeetings(init_data)
# print "My Meetings:\n", test.my_meetings.replace("<br/>", "\n")
# print "Pending:\n", test.pending.replace("<br/>", "\n")
# print "My Requests:\n", test.my_requests.replace("<br/>", "\n")
# print "Confirmed:\n", test.confirmed.replace("<br/>", "\n")
