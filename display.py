#!/usr/bin/python

import os
import wx

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

class MainFrame(wx.Frame):
	def __init__(self, parent, id, title):
		self.cwd = os.getcwd()

		# Initialize main frame	
		DEFAULT_WIDTH = 650 
		DEFAULT_HEIGHT = 550 
		MIN_WIDTH = 450 
		MIN_HEIGHT = 550 
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(DEFAULT_WIDTH, DEFAULT_HEIGHT))
		vbox = wx.BoxSizer(wx.VERTICAL)	# vertical box sizer for panels

		# Controls for adding or removing files from list
		filesPanel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
		filesBoxSizer = wx.BoxSizer(wx.HORIZONTAL)	# horizontal box sizer for buttons
		addFilesButton = wx.BitmapButton(filesPanel, 1, wx.Bitmap('/home/agonzales/Documents/asl-sensorloc/resources/icons/add.png'), name='Add Files')
		emptySpace = wx.StaticText(filesPanel, -1, '')	
		removeSelectedButton = wx.BitmapButton(filesPanel, 2, wx.Bitmap('/home/agonzales/Documents/asl-sensorloc/resources/icons/remove.png'), name='Remove Selected')	
		filesBoxSizer.Add(addFilesButton, 0, wx.EXPAND)
		filesBoxSizer.Add(emptySpace, 0, wx.EXPAND)
		filesBoxSizer.Add(removeSelectedButton, 0, wx.EXPAND)
		vbox.Add(filesBoxSizer, 1, wx.EXPAND)	
		filesPanel.SetSizer(vbox)

class MyApp(wx.App):
	def OnInit(self):
		frame = MainFrame(None, -1, 'Collect Azimuth Files')
		frame.Show(True)
		return True

app = MyApp(0)
app.MainLoop()

