# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

# Sends an email to all the responders by appending a @princeton.edu
def sendCreationEmail(title, netid, responders):
	for respondee in responders:
		sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
		from_email = Email("Convener@convener.herokuapp.com")
		to_email = Email(respondee + "@princeton.edu")
		subject = "Convener Meeting Request - " + title
		content = Content("text/html", "<p>Requested Meeting Title: <b>" + title + "</b></p> \
			<p>You have a new Convener meeting request from <b>" + netid + "</b> </p> \
			<p>Check it out at convener.herokuapp.com </p>")
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())

# Sends an email to creator when all responders have responded
def sendAllRespondedEmail(title, netid):
	sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	from_email = Email("Convener@convener.herokuapp.com")
	to_email = Email(netid + "@princeton.edu")
	subject = "Convener All Responded - " + title
	content = Content("text/html", "<p>Everyone has responded with a meeting time for your meeting: <b>" + title + "</b></p> \
		<p>Check it out at convener.herokuapp.com </p>")
	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

# Sends an email to all responders when a final meeting time has been selected
def sendFinalTimeEmail(title, netid, responders, time):
	for respondee in responders:
		sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
		from_email = Email("Convener@convener.herokuapp.com")
		to_email = Email(respondee + "@princeton.edu")
		subject = "Meeting Time Confirmed - " + title
		content = Content("text/html", "<p>The meeting: <b>" + title + "</b> created by \
			" + netid + " has been scheduled.</p> \
			The meeting date is on " + time['date'] + " at " + time['time'] + " \
			<p>Check it out at convener.herokuapp.com </p>")
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())