import time

# Table object for preferred times
class Table_Pref(object):

	# constants
	HOURS_IN_DAY = 24
	DAYS_IN_WEEK = 7
	# array of days
	inOrderDayArray = ["Sun", "Mon","Tue","Wed","Thu","Fri","Sat"]
	
	def __init__(self):
		# print table
		self.html = "<table id='mainTable' class='table table-bordered table-condensed overwrite_table'>"
		self.html += self.printHeader()
		self.html += self.printCells()
		self.html += "</table>"

	# print the days of the week as headers, starting from today
	def printHeader(self):
		html = "<tr>"
		for day in self.inOrderDayArray:
			html += "<th>%s</th>" % day
		html += "</tr>"
		return html

	# print each individual cell of the table
	def printCells(self):
		html = ""
		for row in range(self.HOURS_IN_DAY):
			html += "<tr>"
			for col in range(self.DAYS_IN_WEEK):
				hour = row % 13
				# so it says 12am instead of 0am
				if hour == 0 and row < 12:
					hour = 12
				if row < 12:
					html += "<td id ='%s_%dam' class='cell'>%dam</td>" % (self.inOrderDayArray[col], hour, hour)
				else:
					if row > 12:
						hour += 1
					html += "<td id ='%s_%dpm' class='cell'>%dpm</td>" % (self.inOrderDayArray[col], hour, hour)
			html += "</tr>"
		return html