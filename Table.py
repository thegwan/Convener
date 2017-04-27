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
		index = 0
		for day in self.inOrderDayArray:
			if index == 6:
				html += '<th id="%s" class="bold_col">%s</th>' % (self.idHeaderArray[index], day)
			else:
				html += '<th id="%s">%s</th>' % (self.idHeaderArray[index], day)
			index += 1
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
				# am
				if row < 12:
					if not incr_hour:
						html += self.formatCell(col, hour, '00', 'am')
					else:
						html += self.formatCell(col, hour, '30', 'am')
				# pm
				else:
					if not incr_hour:
						html += self.formatCell(col, hour, '00', 'pm')
					else:
						html += self.formatCell(col, hour, '30', 'pm')
			html += "</tr>"
			if incr_hour:
				hour += 1
			incr_hour = not incr_hour
		return html

	# adds the correct id, classes, and text to each cell
	def formatCell(self, col, hour, minute, am_pm):
		html = ""
		# bold_col: put a bold line to separate each week
		if col == 6:
			html += "<td id ='%s_%d:%s%s' class='cell selectable bold_col'>%d:%s</td>" % (self.idArray[col], hour, minute, am_pm, hour, minute)
		else:
			html += "<td id ='%s_%d:%s%s' class='cell selectable'>%d:%s</td>" % (self.idArray[col], hour, minute, am_pm, hour, minute)
		return html