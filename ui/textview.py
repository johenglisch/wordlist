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
		# text view
		self.textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.textctrl.SetEditable(False)

	def update_text(self):
		'''update text field'''
		self.textctrl.SetValue(self.text)


