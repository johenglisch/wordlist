#!/usr/bin/env python2

#########################################################################
# programme	: stoplist.py                                           #
# description	: stoplist editor dialog for the Wordlist programme     #
# last edit	: 02-Aug-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import wx

class StoplistDlg(wx.Dialog):
	'''dialogue for editing the stoplist
	
	attributes:
		stoplist	the stoplist
		textctrl	the control displaying the stoplist
	'''

	def __init__(self, stoplist, *args, **kwargs):
		wx.Dialog.__init__(self, *args, **kwargs)
		self.init_ui()
	
	def init_ui(self):
		self.textctrl = wx.TextCtrl(self, style = wx.TE_MULTILINE)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(wx.Button(self, wx.ID_OPEN, '&Open from file...'))
		hbox.Add(wx.Button(self, wx.ID_OK, 'O&k'))
		hbox.Add(wx.Button(self, wx.ID_CANCEL, '&Close'))
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(wx.StaticText(self, id = -1, label = 'Edit stoplist:'))
		vbox.Add(self.textctrl, flag = wx.EXPAND)
		vbox.Add(hbox, flag = wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
		self.SetSizer(vbox)
		self.SetSize(self.GetBestSize())


