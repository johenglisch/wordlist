#!/usr/bin/env python2

#########################################################################
# programme	: stoplist.py                                           #
# description	: stoplist editor dialog for the Wordlist programme     #
# last edit	: 05-Aug-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import re
import wx

class StoplistDlg(wx.Dialog):
	'''dialogue for editing the stoplist
	
	attributes:
		parent		the parent window
		stoplist	the stoplist
		textctrl	the control displaying the stoplist
	'''

	def __init__(self, stoplist, parent, *args, **kwargs):
		wx.Dialog.__init__(self, parent, *args, **kwargs)
		self.stoplist = stoplist
		self.parent = parent
		self.init_ui()
		self.textctrl.SetValue('\n'.join(stoplist))
	
	def init_ui(self):
		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(wx.StaticText(self, id = -1, label = 'Edit stoplist:'))
		# text control
		self.textctrl = wx.TextCtrl(self, style = wx.TE_MULTILINE)
		vbox.Add(self.textctrl, flag = wx.EXPAND)
		# buttons
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		butopen = wx.Button(self, wx.ID_OPEN, 'O&pen...')
		butsave = wx.Button(self, wx.ID_SAVE, '&Save...')
		butok = wx.Button(self, wx.ID_OK, '&Ok')
		butcancel = wx.Button(self, wx.ID_CANCEL, '&Close')
		hbox.AddMany([butopen, butsave, butok, butcancel])
		vbox.Add(hbox, flag = wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT)
		self.SetSizer(vbox)
		self.SetSize(self.GetBestSize())
		# events
		butopen.Bind(wx.EVT_BUTTON, self.on_open)
		butsave.Bind(wx.EVT_BUTTON, self.on_save)
		butok.Bind(wx.EVT_BUTTON, self.on_ok)

	def on_ok(self, event):
		'''OK button applies stoplist changes and closes dialogue'''
		self.stoplist = re.findall('(?u)\w+',
				self.textctrl.GetValue())
		self.EndModal(wx.ID_OK)

	def on_open(self, event):
		'''Open button reads stoplist from file'''
		pass

	def on_save(self, event):
		'''Save button saves current stoplist to file'''
		pass


