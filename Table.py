import time
from datetime import datetime, timedelta

# Table object for Convener: html attribute contains the html
# to construct the table
class Table(object):

	# constants
	HOURS_IN_DAY = 18 # starting from 6am
	DAYS_IN_WEEK = 7
	# array of days with today's day at index 0
	inOrderDayArray = []
	
	def __init__(self):
		# fill inOrderDayArray with dates for the next two weeks
		for i in range(2 * self.DAYS_IN_WEEK):
			self.inOrderDayArray.append((datetime.now() + timedelta(i)).strftime('%B<br/>%d'))

		# print table
		self.html = "<table id='mainTable' class='table table-bordered table-condensed overwrite_table'>"
		self.html += self.printHeader()
		self.html += self.printCells()
		self.html += "</table>"

	# print the days of the week as headers, starting from today
	def printHeader(self):
		html = "<tr>"
		# to determine where to put the vertical line (divider)
		index = 0
		for day in self.inOrderDayArray:
			if index == 6:
				html += '<th class="bold_col">%s</th>' % day
			else:
				html += "<th>%s</th>" % day
			index += 1
		html += "</tr>"
		return html

	# print each individual cell of the table
	def printCells(self):
		html = ""
		# to determine where to put the vertical line
		for row in range(6, self.HOURS_IN_DAY + 6):
			index = 0
			if row == 12:
				html += "<tr id='bold_row'>"
			else:
				html += "<tr>"
			for i in range(2):
				for col in range(self.DAYS_IN_WEEK):
					hour = row % 13
					# so it says 12am instead of 0am
					if hour == 0 and row < 12:
						hour = 12
					if row < 12:
						if index == 6:
							html += "<td id ='%s_%dam' class='cell bold_col'>%d</td>" % (self.inOrderDayArray[col], hour, hour)
						else:
							html += "<td id ='%s_%dam' class='cell'>%d</td>" % (self.inOrderDayArray[col], hour, hour)
					else:
						if row > 12:
							hour += 1
						if index == 6:
							html += "<td id ='%s_%dpm' class='cell bold_col'>%d</td>" % (self.inOrderDayArray[col], hour, hour)
						else:
							html += "<td id ='%s_%dpm' class='cell'>%d</td>" % (self.inOrderDayArray[col], hour, hour)
					index += 1
			html += "</tr>"
		return html