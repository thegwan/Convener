import time

# Table object for preferred times
class Table_Pref(object):

	# constants
	STARTING_TIME = 6 # starting from 6am
	HALF_HOURS_IN_DAY = 36 # half hours from 6am - midnight
	DAYS_IN_WEEK = 7
	# array of days
	dayArray = ["Sun", "Mon","Tue","Wed","Thu","Fri","Sat"]
	
	def __init__(self):
		# print table
		self.html = "<table id='prefTable' class='table table-bordered table-condensed overwrite_table' style='display: none;'>"
		self.html += self.printHeader()
		self.html += self.printCells()
		self.html += "</table>"

	# print the days of the week as headers, starting from today
	def printHeader(self):
		html = "<tr>"
		col = 0
		for day in self.dayArray:
			html += '<th data-column="%d">%s</th>' % (col, day)
			col += 1
		html += "</tr>"
		return html

	# print each individual cell of the table
	def printCells(self):
		html = ""
		incr_hour = False
		hour = self.STARTING_TIME
		for row in range(self.HALF_HOURS_IN_DAY):
			if hour == 13:
				hour = 1
			# put a bold line to separate am and pm
			if row == 12 and not incr_hour:
				html += "<tr id='bold_row'>"
			else:
				html += "<tr>"
			for col in range(self.DAYS_IN_WEEK):
				# am
				if row < 12:
					html += self.formatCell(col, hour, 'am', incr_hour)
				# pm
				else:
					html += self.formatCell(col, hour, 'pm', incr_hour)
			html += "</tr>"
			if incr_hour:
				hour += 1
			incr_hour = not incr_hour
		return html

	# adds the correct id, classes, and text to each cell
	def formatCell(self, col, hour, am_pm, incr_hour):
		html = ""
		if not incr_hour:
			return "<td id ='%s_%d:00%s' class='cell selectable' data-column='%d'><b>%d:00</b></td>" % (self.dayArray[col], hour, am_pm, col, hour)
		else:
			return "<td id ='%s_%d:30%s' class='cell selectable' data-column='%d'>30</td>" % (self.dayArray[col], hour, am_pm, col)
