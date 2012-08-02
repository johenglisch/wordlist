#!/usr/bin/env python2

#########################################################################
# programme	: textview.py                                           #
# description	: simple text viewer window                             #
# last edit	: 02-Aug-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import wx

class TextView(wx.Frame):
	'''simple text viewer window
	
	attributes:
		text		the text to be displayed
		textctrl	the control displaying the text
	'''

	def __init__(self, text, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.text = text
		self.init_ui()
		self.Show()
		self.update_text()

	def init_ui(self):
		'''initialise user interface'''
		self.SetTitle('View text')
		self.SetSize((300, 300))
		# menubar
		menubar = wx.MenuBar()
		menufile = wx.Menu()
		fileclose = menufile.Append(wx.ID_CLOSE, '&Close\tCtrl-W',
				'Close text view window')
		filequit = menufile.Append(wx.ID_EXIT, '&Quit\tCtrl-Q',
				'Quit the Wordlist programme')
		menubar.Append(menufile, '&File')
		self.SetMenuBar(menubar)
		self.Bind(wx.EVT_MENU, self.on_close, fileclose)
		self.Bind(wx.EVT_MENU, self.on_quit, filequit)
		# text view
		self.textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.textctrl.SetEditable(False)

	def on_close(self, event):
		'''close current frame'''
		self.Close()

	def on_quit(self, event):
		'''quit programme'''
		self.GetParent().Close()

	def update_text(self):
		'''update text field'''
		self.textctrl.SetValue(self.text)


