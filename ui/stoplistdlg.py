#!/usr/bin/env python2

#########################################################################
# programme	: stoplist.py                                           #
# description	: stoplist editor dialog for the Wordlist programme     #
# last edit	: 05-Aug-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import os
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
		butopen = wx.Button(self, wx.ID_OPEN, '&Add from file...')
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
		dialog = wx.FileDialog(self,
				message = '',
				defaultDir = self.parent.dirname,
				defaultFile = '',
				wildcard = '*',
				style = wx.OPEN)
		response = dialog.ShowModal()
		path = dialog.GetPath()
		dialog.Destroy()
		if response == wx.ID_OK:
			with open(path, 'r') as f:
				content = unicode(f.read(), 'utf-8')
				content = re.findall('(?u)\w+', content)
				self.textctrl.WriteText('\n'.join(content))
		dialog.Destroy()

	def on_save(self, event):
		'''Save button saves current stoplist to file'''
		dialog = wx.FileDialog(self,
				message='',
				defaultDir = self.parent.dirname,
				defaultFile = '',
				wildcard = '*',
				style = wx.SAVE)
		response = dialog.ShowModal()
		path = dialog.GetPath()
		dialog.Destroy()
		if response == wx.ID_OK:
			if os.path.isfile(path):
				msg = wx.MessageDialog(self,
						message = 'The file {0} already exists. Overwrite?'.format(path),
						style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				confirm = msg.ShowModal()
				msg.Destroy()
				if confirm != wx.ID_YES:
					return
			content = re.findall('(?u)\w+', self.textctrl.GetValue())
			content = ['{0}\r\n'.format(s) for s in content]
			with open(path, 'w') as f:
				f.writelines(content)


