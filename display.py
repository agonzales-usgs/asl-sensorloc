#!/usr/bin/python

import os
import wx
import sys
import subprocess
import signal
import glob, string, re
from obspy.core.utcdatetime import UTCDateTime
from obspy.core.stream import read
from obspy.signal.invsim import evalresp
from datetime import datetime, timedelta

class MainFrame(wx.Frame):
	def __init__(self, parent, id, title):
		self.dirname = os.getcwd()

		# Initialize main frame	
		DEFAULT_WIDTH = 650 
		DEFAULT_HEIGHT = 750 
		MIN_WIDTH = 450 
		MIN_HEIGHT = 550 
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(DEFAULT_WIDTH, DEFAULT_HEIGHT))

		# Buttons for adding or removing files from list
		filesPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
		filesHBox = wx.BoxSizer(wx.HORIZONTAL)	# horizontal box sizer for buttons
		self.addFilesButton = wx.Button(filesPanel, -1, 'Add Files')
		self.removeSelectedButton = wx.Button(filesPanel, -1, 'Remove Selected') 
		self.Bind(wx.EVT_BUTTON, self.AddFiles, self.addFilesButton)
		self.Bind(wx.EVT_BUTTON, self.RemoveSelected, self.removeSelectedButton)

		filesHBox.Add(self.addFilesButton, 0, wx.EXPAND | wx.ALL, 3)
		filesHBox.Add((300,-1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)	
		filesHBox.Add(self.removeSelectedButton, 0, wx.EXPAND | wx.ALL, 3)
		filesPanel.SetSizer(filesHBox)

		# Scrollable list control for inserting/removing files
		listPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
		listHBox = wx.BoxSizer(wx.HORIZONTAL)	# horizontal box sizer for lc	
		self.listControl = wx.ListCtrl(listPanel, size=(-1,150), style=wx.LC_REPORT)
		self.listControl.InsertColumn(0, 'File List')
		self.listControl.SetColumnWidth(0, 640)	
		
		listHBox.Add(self.listControl, 1, wx.EXPAND | wx.ALL, 5)	
		listPanel.SetSizer(listHBox)

		# Read in list of miniseed files
		readPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
		readHBox = wx.BoxSizer(wx.HORIZONTAL)	# horizontal box sizer for buttons
		self.readFilesButton = wx.Button(readPanel, -1, 'Read Files')
		self.cancelReadButton = wx.Button(readPanel, -1, 'Cancel Read')
		#self.Bind(wx.EVT_BUTTON, self.ReadFiles, self.readFilesButton)
		#self.Bind(wx.EVT_BUTTON, self.CancelRead, self.cancelReadButton)

		readHBox.Add(self.readFilesButton, 0, wx.EXPAND | wx.ALL, 3)
		readHBox.Add((300,-1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
		readHBox.Add(self.cancelReadButton, 0, wx.EXPAND | wx.ALL, 3)
		readPanel.SetSizer(readHBox)

		# Progress indicator for reading in files
		progressPanel = wx.Panel(self, -1, style=wx.SUNKEN_BORDER)
		progressHBox = wx.BoxSizer(wx.HORIZONTAL)	# horizontal boxsizer for progress
		self.gauge = wx.Gauge(progressPanel, -1, range=100, size=(600,10))
		
		progressHBox.Add(self.gauge, 1, wx.EXPAND | wx.ALL, 3)
		progressPanel.SetSizer(progressHBox)

		# Widget configuration (initialize enable/disable widgets)
		self.addFilesButton.Enable(True)	
		self.removeSelectedButton.Enable(False)
		self.readFilesButton.Enable(False)
		self.cancelReadButton.Enable(False)

		# Main frame vertical sizer (add panels)	
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(filesPanel, 0, wx.EXPAND | wx.ALL, 3)
		sizer.Add(listPanel, 0, wx.EXPAND | wx.ALL, 3) 
		sizer.Add(readPanel, 0, wx.EXPAND | wx.ALL, 3)	
		sizer.Add(progressPanel, 0, wx.EXPAND | wx.ALL, 3)	
		self.statusbar = self.CreateStatusBar()
		self.statusbar.SetStatusText('Add Sensorloc mini-SEED files')	
		self.SetSizer(sizer)
		self.Center()

	def AddFiles(self, event):
		# Open files for chopping
		dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.MULTIPLE)
		if dlg.ShowModal() == wx.ID_OK:
			self.filelist = dlg.GetPaths()
			num_files = len(self.filelist)
			for i in range(num_files):
				num_items = self.listControl.GetItemCount()	
				self.listControl.InsertStringItem(num_items, self.filelist[i]) 
			
			# Enable remove/read files buttons if files are present
			self.statusbar.SetStatusText('Sensorloc mini-SEED files inserted')	
			self.removeSelectedButton.Enable(True)		
			self.readFilesButton.Enable(True)	
		dlg.Destroy()

	def RemoveSelected(self, event):
		item = self.listControl.GetFirstSelected()
		print "first selected item index = " + str(item)
		while item != -1:
			item = self.listControl.GetNextSelected(item)
			print "next selected item = " + str(item)
			self.listControl.DeleteItem(item)
		'''	
		index = self.listControl.GetFocusedItem()
		filename = self.listControl.GetItemText(index)
		self.listControl.DeleteItem(index)
		self.statusbar.SetStatusText('Deleted file: ' + str(filename))
		'''
	'''	
	def ReadFiles(self, event):
		num_items = self.listControl.GetItemCount()
	'''

class MyApp(wx.App):
	def OnInit(self):
		frame = MainFrame(None, -1, 'Collect Azimuth Files')
		frame.Show(True)
		self.SetTopWindow(frame)	
		return True

app = MyApp(0)
app.MainLoop()

'''
Tab between text fields:
class ContactsPanel(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize,
					wx.RAISED_BORDER | wx.TAB_TRAVERSAL)

Tab order is set by order you add controls to panel or frame
Tab order is dependent on the order widgets are created
Tab order:
order = (control1, control2, control3, ...)
for i in xrange(len(order) - 1):
	order[i+1].MoveAfterInTabOrder(order[i])
'''
