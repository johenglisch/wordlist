#!/usr/bin/env python2

'''stoplist.py - a dialogue for editing stoplists'''

import os
import re
regex = re.compile('\w+', re.UNICODE)
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
		self.textctrl.SetMinSize((250, 160))
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
		self.Fit()
		# events
		butopen.Bind(wx.EVT_BUTTON, self.on_open)
		butsave.Bind(wx.EVT_BUTTON, self.on_save)
		butok.Bind(wx.EVT_BUTTON, self.on_ok)

	def on_ok(self, event):
		'''OK button applies stoplist changes and closes dialogue'''
		self.stoplist = regex.findall(self.textctrl.GetValue())
		self.stoplist = [s.lower() for s in self.stoplist]
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
			try:
				with open(path, 'r') as f:
					content = unicode(f.read(), 'utf-8')
					content = regex.findall(content)
					self.textctrl.WriteText('\n'.join(content))
			except Exception as e:
				wx.MessageBox(str(e), '', wx.OK
						| wx.ICON_ERROR)
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
			content = regex.findall(self.textctrl.GetValue())
			content = ['{0}\r\n'.format(s.encode('utf-8'))
					for s in content]
			try:
				with open(path, 'w') as f:
					f.writelines(content)
			except Exception as e:
				wx.MessageBox(str(e), '', wx.OK
						| wx.ICON_ERROR)


