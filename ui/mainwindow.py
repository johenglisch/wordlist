#!/usr/bin/env python2

#########################################################################
# programme	: mainwindow.py                                         #
# description	: main window of the wordlist gui                       #
# last edit	: 02-Aug-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

__all__ = ['MainWindow']

import os
import wx
from wordlist import Wordlist
from textview import TextView

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


class TableDND(wx.FileDropTarget):
	'''make wordlist table a target for file drag'n'drop

	attributes:
		self.window	drop target
	'''

	def __init__(self, window):
		wx.FileDropTarget.__init__(self)
		self.window = window

	def OnDropFiles(self, x, y, filenames):
		'''load wordlist on file drop'''
		if len(filenames) > 1:
			return
		self.window.GetParent().load_wordlist(filenames[0])
		self.window.GetParent().update_table()


class MainWindow(wx.Frame):
	'''main frame for wordlist programme
	
	attributes:
		dirname		directory of the text file
		filename	file name of the text file
		wordlist	the wordlist
	widgets:
		filesave	menu entry: File -> Save...
		viewbyword	menu entry: View -> Sort by beginning of word
		viewbyend	menu entry: View -> Sort by end of word
		viewbyfreq	menu entry: View -> Sort by frequency
		toolsview	menu entry: Tools -> View text...
		toolbar		the toolbar of the frame
		tb_viewtext	toolbar button: view text
		table		the table showing the wordlist
		statusbar	the statusbar widget
		textview	the TextView window
	'''

	def __init__(self, filename, stoplists=None, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.dirname = ''
		self.filename = ''
		self.statusbar = None
		self.textview = None
		self.init_ui()
		self.wordlist = None
		if filename:
			self.load_wordlist(filename)
		else:
			self.disable_controls()
		self.Show()
		self.update_table()

	def init_ui(self):
		'''initialise user interface'''
		self.SetSize((350, 400))
		self.SetTitle('Wordlist')
		# menubar
		menubar = wx.MenuBar()
		menufile = wx.Menu()
		fileopen = menufile.Append(wx.ID_OPEN,
				'&Open...\tCtrl-O',
				'Open a text file and create a wordlist from it')
		self.filesave = menufile.Append(wx.ID_SAVE,
				'&Save...\tCtrl-S',
				'Save the wordlist to a text file')
		filequit = menufile.Append(wx.ID_EXIT,
				'&Quit\tCtrl-Q',
				'Quit the Wordlist programme')
		menubar.Append(menufile, '&File')
		menuview = wx.Menu()
		self.viewbyword = menuview.AppendRadioItem(-1,
				'Sort by beginning of &word\tCtrl-1',
				'Sort the wordlist by the beginning of the words')
		self.viewbyend = menuview.AppendRadioItem(-1 ,
				'Sort by &end of word\tCtrl-2',
				'Sort the wordlist by the end of the words')
		self.viewbyfreq = menuview.AppendRadioItem(-1,
				'Sort by &frequency\tCtrl-3',
				'Sort the wordlist by the occurences of the words')
		menubar.Append(menuview, '&View')
		menutools = wx.Menu()
		self.toolsstoplist = menutools.Append(-1,
				'Edit &Stoplist...\tCtrl-E',
				'Edit the stoplist')
		self.toolsview = menutools.Append(-1,
				'&View text...\tCtrl-T',
				'View the text the wordlist was created from')
		menubar.Append(menutools, '&Tools') 
		self.SetMenuBar(menubar)
		# menu events
		self.Bind(wx.EVT_MENU, self.on_open, fileopen)
		self.Bind(wx.EVT_MENU, self.on_save, self.filesave)
		self.Bind(wx.EVT_MENU, self.on_quit, filequit)
		self.Bind(wx.EVT_MENU, self.on_sort, self.viewbyword)
		self.Bind(wx.EVT_MENU, self.on_sort, self.viewbyend)
		self.Bind(wx.EVT_MENU, self.on_sort, self.viewbyfreq)
		self.Bind(wx.EVT_MENU, self.on_viewtext, self.toolsview)
		self.Bind(wx.EVT_MENU, self.on_stoplist, self.toolsstoplist)
		# toolbar
		self.toolbar = self.CreateToolBar()
		tb_open = self.toolbar.AddLabelTool(wx.ID_OPEN, label='Open',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN),
				shortHelp='Open text file',
				longHelp='Open a text file and create a wordlist from it')
		tb_save = self.toolbar.AddLabelTool(wx.ID_SAVE, label='Save',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE),
				shortHelp='Save wordlist',
				longHelp='Save the wordlist to a text file')
		self.tb_viewtext = self.toolbar.AddLabelTool(wx.ID_ANY, label='View text',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE),
				shortHelp='View text',
				longHelp='View the text the wordlist was created from')
		self.Bind(wx.EVT_TOOL, self.on_open, tb_open)
		self.Bind(wx.EVT_TOOL, self.on_save, tb_save)
		self.Bind(wx.EVT_TOOL, self.on_viewtext, self.tb_viewtext)
		self.toolbar.Realize()
		# statusbar
		self.statusbar = self.CreateStatusBar()
		# table
		self.table = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
		# table drag'n'drop
		droptarget = TableDND(self.table)
		self.table.SetDropTarget(droptarget)

	def disable_controls(self):
		'''disable controls'''
		self.filesave.Enable(False)
		self.viewbyword.Check(True)
		self.viewbyword.Enable(False)
		self.viewbyend.Enable(False)
		self.viewbyfreq.Enable(False)
		self.toolsstoplist.Enable(False)
		self.toolsview.Enable(False)
		self.toolbar.EnableTool(wx.ID_SAVE, False)
		self.toolbar.EnableTool(self.tb_viewtext.GetId(), False)

	def enable_controls(self):
		'''enable controls'''
		self.filesave.Enable(True)
		self.viewbyword.Enable(True)
		self.viewbyend.Enable(True)
		self.viewbyfreq.Enable(True)
		self.toolsstoplist.Enable(True)
		self.toolsview.Enable(True)
		self.toolbar.EnableTool(wx.ID_SAVE, True)
		self.toolbar.EnableTool(self.tb_viewtext.GetId(), True)

	def get_sorted(self):
		'''return sorted word list'''
		if self.viewbyend.IsChecked():
			return self.wordlist.items_by_wordend()
		if self.viewbyfreq.IsChecked():
			return self.wordlist.most_common()
		return sorted(self.wordlist.items())

	def load_wordlist(self, filename):
		'''load wordlist from file'''
		filename = os.path.abspath(filename)
		if self.statusbar:
			self.statusbar.SetStatusText('Reading data from file...')
		with open(filename, 'r') as f:
			text = unicode(f.read(), 'utf-8')
		self.wordlist = Wordlist(text)
		if self.statusbar:
			self.statusbar.SetStatusText('Data read.')
		self.dirname = os.path.dirname(filename)
		self.filename = os.path.basename(filename)
		self.enable_controls()

	def on_open(self, event):
		'''open a text file and generate wordlist'''
		dialog = wx.FileDialog(self, message='', defaultDir=self.dirname,
				defaultFile=self.filename, wildcard='*', style=wx.OPEN)
		answer = dialog.ShowModal()
		if answer == wx.ID_OK:
			self.load_wordlist(dialog.GetPath())
			self.update_table()
		dialog.Destroy()

	def on_save(self, event):
		'''save wordlist to text file'''
		dialog = wx.FileDialog(self, message='', defaultDir=self.dirname,
				defaultFile='', wildcard='*', style=wx.SAVE)
		answer = dialog.ShowModal()
		filename = dialog.GetPath()
		dialog.Destroy()
		if answer == wx.ID_OK:
			if os.path.isfile(filename):
				msg = wx.MessageDialog(self,
						message = 'The file \'{0}\' already exists. Overwrite?'.format(filename),
						style = wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
				confirm = msg.ShowModal()
				msg.Destroy()
				if confirm != wx.ID_YES:
					return
			self.statusbar.SetStatusText('Saving file...')
			tab = ['{0}\t{1}\r\n'.format(w.encode('utf-8'), f)
					for w, f in self.get_sorted()]
			with open(filename, 'w') as f:
				f.writelines(tab)
			self.statusbar.SetStatusText('File saved.')

	def on_sort(self, event):
		'''sort wordlist'''
		self.update_table()

	def on_stoplist(self, event):
		'''open 'edit stoplist' dialogue'''
		dialog = StoplistDlg(self.wordlist.stoplist, self)
		response = dialog.ShowModal()
		if response == wx.ID_OK:
			print 'OK'
		if response == wx.ID_CANCEL:
			print 'Close'
		dialog.Destroy()

	def on_quit(self, event):
		'''quit programme'''
		self.Close()

	def on_viewtext(self, event):
		'''view the text'''
		if self.textview:
			self.textview.text = self.wordlist.text
			self.textview.update_text()
			self.textview.SetFocus()
		else:
			self.textview = TextView(self.wordlist.text, self)

	def update_table(self, sortbyend=False, sortbyfreq=False):
		'''refill the table with the content of the wordlist'''
		self.statusbar.SetStatusText('Updating wordlist...')
		self.table.ClearAll()
		if self.wordlist:
			values = self.get_sorted()
			align = wx.LIST_FORMAT_LEFT
			if self.viewbyend.IsChecked():
				align = wx.LIST_FORMAT_RIGHT
			self.table.InsertColumn(0, 'word', align)
			self.table.InsertColumn(1, 'frequency')
			for i in values:
				self.table.Append(i)
		self.statusbar.SetStatusText('Wordlist updated.')

