import time

# Table object for Convener: html attribute contains the html
# to construct the table
class Table(object):

	# constants
	HOURS_IN_DAY = 18 # starting from 6am
	DAYS_IN_WEEK = 7
	# array of days with today's day at index 0
	inOrderDayArray = []
	
	def __init__(self):
		# general array of days
		dayArray = ["Sun", "Mon","Tue","Wed","Thu","Fri","Sat"]
		# Today's day as a decimal number [0(Sun), 6]
		currDay = 0 # int(time.strftime("%w"))
		# fill inOrderDayArray
		for i in range(currDay, currDay + self.DAYS_IN_WEEK):
			day = i % self.DAYS_IN_WEEK
			self.inOrderDayArray.append(dayArray[day])
		# print table
		self.html = "<table id='mainTable' class='table table-bordered table-condensed overwrite_table'>"
		self.html += self.printHeader()
		self.html += self.printCells()
		self.html += "</table>"

	# print the days of the week as headers, starting from today
	def printHeader(self):
		html = "<tr>"
		# to determine where to put the vertical line
		index = 0
		# print 2 weeks
		for i in range(2):
			for day in self.inOrderDayArray:
				if index == 6:
					html += '<th class="bold_col">%s</th>' % day
					print html
				else:
					html += "<th>%s</th>" % day
				index += 1
				print index
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