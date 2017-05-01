# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *

def sendCreationEmail(title, netid, responders):
	# print("hear")
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
