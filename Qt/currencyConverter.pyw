import sys
import urllib2

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Form(QDialog):

	def __init__(self, parent=None):
		super(Form, self).__init__(parent) ## inherits from parent

		# get some class variables
		date  = self.getdata()				#only to be used within class
		rates = sorted(self.rates.keys())	#no need to self.-	'em

		# Date Label
		dateLabel = QLabel(date)

		# FROM combo box
		self.fromComboBox = QComboBox()
		self.fromComboBox.addItems(rates)

		# FROM spin box
		self.fromSpinBox = QDoubleSpinBox()
		self.fromSpinBox.setRange(0.01, 10000000.00)
		self.fromSpinBox.setValue(1.00)

		# TO combo box
		self.toComboBox = QComboBox()
		self.toComboBox.addItems(rates)

		# TO label
		self.toLabel = QLabel("1.00")

		# put everything into place
		grid = QGridLayout()
		grid.addWidget(dateLabel, 0, 0)
		grid.addWidget(self.fromComboBox, 1, 0)
		grid.addWidget(self.fromSpinBox, 1, 1)
		grid.addWidget(self.toComboBox, 2, 0)
		grid.addWidget(self.toLabel, 2, 1)
		self.setLayout(grid)

		# SIGNAL-SLOT connects
		self.connect(self.fromComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
		self.connect(self.toComboBox, SIGNAL("currentIndexChanged(int)"), self.updateUi)
		self.connect(self.fromSpinBox, SIGNAL("valueChanged(double)"), self.updateUi)

		# window title
		self.setWindowTitle("Currency")


	# get the text from "from box" and "to box"
	# read the values in the dictionary and calculate
	# the rate and multiply by the amount
	# update the text of "toLabel"
	def updateUi(self):
		to = unicode(self.toComboBox.currentText())
		from_ = unicode(self.fromComboBox.currentText())
		amount = (self.rates[from_] / self.rates[to])*self.fromSpinBox.value()
		self.toLabel.setText("%0.2f" % amount )

	def getdata(self): # Idea taken from the Python Cookbook self.rates = {}

		# create a dictonary for book-keeping and
		# make it member variable
		self.rates = {}
		
		# try to download the csv 
		try:
			date = "Unknown"
			fh = urllib2.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")
			
			# read all lines, appart from comments
			for line in fh:
				if not line or line.startswith(("#", "Closing ")):
					continue
				fields = line.split(",")  # split by ',' as it is csv
				
				if line.startswith("Date "):
					date = fields[-1]  # if you're looking at the date (latest)
				else:
					try:
						value = float(fields[-1])  # value for exchange is the latest (last) column
						self.rates[unicode(fields[0])] = value # get the 1st field of the line in unic
					except ValueError:
						pass
			return "Exchange Rates Date: " + date
		except Exception, e:
			return "Failed to download:\n%s" % e

if __name__ == '__main__':
	app = QApplication(sys.argv)
	form = Form()
	form.show()
	app.exec_()