import time
from datetime import datetime, timedelta

# Table object for Convener: html attribute contains the html
# to construct the table
class Table(object):

	# constants
	STARTING_TIME = 6 # starting from 6am
	HALF_HOURS_IN_DAY = 36 # half hours from 6am - midnight
	DAYS_IN_WEEK = 7
	# array of days with today's day at index 0
	inOrderDayArray = []
	# used to create id for cells (stores date of each cell in mm-dd-yyyy)
	idArray = []
	# used to create id for header cells (store ids as day-month-date)
	idHeaderArray = []

	def __init__(self):
		# fill inOrderDayArray with dates for the next two weeks
		for i in range(2 * self.DAYS_IN_WEEK):
			month = (datetime.now() + timedelta(i)).strftime('%b')
			date = (datetime.now() + timedelta(i)).strftime('%d')
			day = (datetime.now() + timedelta(i)).strftime('%a')
			self.inOrderDayArray.append(day + "<br/>" + month + "<br/>" + date)
			self.idHeaderArray.append(day + "-" + month + "-" + date)
			self.idArray.append((datetime.now() + timedelta(i)).strftime('%m-%d-%Y'))

		# print table
		self.html = "<table id='mainTable' class='table table-bordered table-condensed overwrite_table'>"
		self.html += self.printHeader()
		self.html += self.printCells()
		self.html += "</table>"

	# print the days of the week as headers, starting from today
	def printHeader(self):
		html = "<tr>"
		# to determine where to put the vertical line (divider)
		col = 0
		for day in self.inOrderDayArray:
			if day[:3] == 'Sun':
				html += '<th id="%s" class="bold_col" data-column="%d">%s</th>' % (self.idHeaderArray[col], col, day)
			else:
				html += '<th id="%s" data-column="%d">%s</th>' % (self.idHeaderArray[col], col, day)
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
			if hour == 12 and not incr_hour:
				html += "<tr id='bold_row'>"
			else:
				html += "<tr>"
			for col in range(2 * self.DAYS_IN_WEEK):
				if row < 12:
					html += self.formatCell(col, incr_hour, hour, 'am')
				else:
					html += self.formatCell(col, incr_hour, hour, 'pm')
			html += "</tr>"
			if incr_hour:
				hour += 1
			incr_hour = not incr_hour
		return html

	# adds the correct id, classes, and text to each cell
	def formatCell(self, col, incr_hour, hour, am_pm):
		html = ""
		if not incr_hour:
			html += self.addBoldCol(col, hour, am_pm, True)
		else:
			html += self.addBoldCol(col, hour, am_pm, False)
		return html

	# add bold vertical line (bold_col class) to separate each week
	def addBoldCol(self, col, hour, am_pm, isStartOfHour):
		html = ""
		# bold_col: put a bold line to separate each week
		if self.inOrderDayArray[col][:3] == 'Sun':
			if isStartOfHour:
				html += "<td id ='%s_%d:00%s' class='cell selectable bold_col' data-column='%d'><b>%d:00</b></td>" % (self.idArray[col], hour, am_pm, col, hour)
			else:
				html += "<td id ='%s_%d:30%s' class='cell selectable bold_col' data-column='%d'>30</td>" % (self.idArray[col], hour, am_pm, col)
		else:
			if isStartOfHour:
				html += "<td id ='%s_%d:00%s' class='cell selectable' data-column='%d'><b>%d:00</b></td>" % (self.idArray[col], hour, am_pm, col, hour)
			else:
				html += "<td id ='%s_%d:30%s' class='cell selectable' data-column='%d'>30</td>" % (self.idArray[col], hour, am_pm, col)
		return html
