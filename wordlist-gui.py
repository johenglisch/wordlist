#!/usr/bin/env python2

#########################################################################
# programme	: wordlist-gui.py                                       #
# description	: wxpython interface for wordlist                       #
# last edit	: 30-Jul-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import os
import sys
import wx
from wx.lib.mixins.listctrl import ColumnSorterMixin
from wordlist import WordList

class ViewText(wx.Frame):
	'''text viewer'''

	def __init__(self, wordlist, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.wordlist = wordlist
		self.init_ui()
		self.Show()
		self.update_text()

	def init_ui(self):
		'''initialise user interface'''
		self.SetTitle('View text')
		self.SetSize((250, 200))
		# text view
		self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.text.SetEditable(False)

	def update_text(self):
		'''update text field'''
		if self.wordlist:
			self.text.SetValue(self.wordlist.raw_text)


class MainWindow(wx.Frame):
	'''main window for wordlist programme'''

	def __init__(self, wordlist, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.wordlist = wordlist
		self.filename = ''
		self.dirname = ''
		self.textview = None
		self.init_ui()
		self.Show()
		self.update_table()

	def init_ui(self):
		'''initialise user interface'''
		self.SetSize((350, 400))
		self.SetTitle('Wordlist')
		# menubar
		menubar = wx.MenuBar()
		menufile = wx.Menu()
		fileopen = menufile.Append(wx.ID_OPEN, '&Open\tCtrl-O',
				'Open a text file and create a wordlist from it')
		filequit = menufile.Append(wx.ID_EXIT, '&Quit\tCtrl-Q',
				'Quit the Wordlist programme')
		menubar.Append(menufile, '&File')
		menuview = wx.Menu()
		viewbyword = menuview.AppendRadioItem(-1, 'Sort by beginning of &word\tCtrl-1',
				'Sort the wordlist by the beginning of the words')
		viewbyend = menuview.AppendRadioItem(-1 , 'Sort by &end of word\tCtrl-2',
				'Sort the wordlist by the end of the words')
		viewbyfreq = menuview.AppendRadioItem(-1, 'Sort by &frequency\tCtrl-3',
				'Sort the wordlist by the occurences of the words')
		menubar.Append(menuview, '&View')
		menutools = wx.Menu()
		toolsview = menutools.Append(-1, '&View text\tCtrl-T',
				'View the text the wordlist was created from')
		menubar.Append(menutools, '&Tools') 
		self.SetMenuBar(menubar)
		# menu events
		self.Bind(wx.EVT_MENU, self.on_open, fileopen)
		self.Bind(wx.EVT_MENU, self.on_quit, filequit)
		self.Bind(wx.EVT_MENU, self.on_viewtext, toolsview)
		# menu accelerators
		accelerators = wx.AcceleratorTable([
			(wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN),
			(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
			(wx.ACCEL_CTRL, ord('1'), viewbyword.GetId()),
			(wx.ACCEL_CTRL, ord('2'), viewbyend.GetId()),
			(wx.ACCEL_CTRL, ord('3'), viewbyfreq.GetId()),
			(wx.ACCEL_CTRL, ord('T'), toolsview.GetId()),
			])
		self.SetAcceleratorTable(accelerators)
		# toolbar
		toolbar = self.CreateToolBar()
		tb_open = toolbar.AddLabelTool(wx.ID_OPEN, label='Open',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN),
				shortHelp='Open text file',
				longHelp='Open a text file and create a wordlist from it')
		self.Bind(wx.EVT_TOOL, self.on_open, tb_open)
		tb_viewtext = toolbar.AddLabelTool(wx.ID_ANY, label='View text',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE),
				shortHelp='View text',
				longHelp='View the text the wordlist was created from')
		self.Bind(wx.EVT_TOOL, self.on_viewtext, tb_viewtext)
		toolbar.Realize()
		# statusbar
		self.statusbar = self.CreateStatusBar()
		# table
		self.table = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
		self.table.InsertColumn(0, 'word')
		self.table.InsertColumn(1, 'frequency')

	def on_quit(self, event):
		'''quit programme'''
		self.Close()

	def on_open(self, event):
		'''open a text file'''
		dialog = wx.FileDialog(self, message='', defaultDir=self.dirname,
				defaultFile=self.filename, wildcard='*', style=wx.OPEN)
		answer = dialog.ShowModal()
		if answer == wx.ID_OK:
			chosen = dialog.GetPath()
			with open(chosen, 'r') as f:
				text = unicode(f.read(), 'utf-8')
			self.wordlist = WordList(text)
			self.dirname = os.path.dirname(chosen)
			self.filename = os.path.basename(chosen)
			self.update_table()
		dialog.Destroy()

	def on_viewtext(self, event):
		'''view the text'''
		if self.textview:
			self.textview.wordlist = self.wordlist
			self.textview.update_text()
			self.textview.SetFocus()
		else:
			self.textview = ViewText(self.wordlist, self)

	def update_table(self):
		'''refill the table with the content of the wordlist'''
		self.statusbar.SetStatusText('Updating wordlist...')
		self.table.DeleteAllItems()
		if self.wordlist:
			for i in sorted(self.wordlist.words):
				self.table.Append(i)
		self.statusbar.SetStatusText('Wordlist updated.')


def main(args):
	wordlist = None
	if len(args) > 1:
		with open(args[1], 'r') as f:
			text = unicode(f.read(), 'utf-8')
			wordlist = WordList(text)
	app = wx.App()
	MainWindow(wordlist, None)
	app.MainLoop()


if __name__ == "__main__":
	main(sys.argv)


