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
from stoplistdlg import StoplistDlg


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
		self.window.parent.load_wordlist(filenames[0])
		self.window.update(self.window.parent.wordlist)


class WordlistTable(wx.ListCtrl):
	'''table for displaying the wordlist

	attributes:
		sortbyend	sort wordlist by word ends?
		sortbyfreq	sort wordlist by frequency?
		parent		the parent window
		wordlist	the wordlist to be displayed
	'''

	def __init__(self, parent, *args, **kwargs):
		wx.ListCtrl.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.wordlist = None
		self.sortbyend = False
		self.sortbyfreq = False
		# drag'n'drop support
		droptarget = TableDND(self)
		self.SetDropTarget(droptarget)

	def get_sorted(self):
		'''return sorted content of the wordlist'''
		if self.sortbyfreq:
			return self.wordlist.most_common()
		if self.sortbyend:
			return self.wordlist.items_by_wordend()
		return sorted(self.wordlist.items())

	def update(self, wordlist = None):
		'''refill the table with the content of the wordlist'''
		if wordlist:
			self.wordlist = wordlist
		self.parent.SetStatusText('Updating wordlist...')
		self.ClearAll()
		if self.wordlist:
			values = self.get_sorted()
			align = wx.LIST_FORMAT_LEFT
			if self.sortbyend:
				align = wx.LIST_FORMAT_RIGHT
			self.InsertColumn(0, 'word', align)
			self.InsertColumn(1, 'frequency')
			for i in values:
				self.Append(i)
		self.parent.SetStatusText('Wordlist updated.')


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
		textview	the TextView window
	'''

	def __init__(self, filename, stoplists=None, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)
		self.dirname = ''
		self.filename = ''
		self.textview = None
		self.init_ui()
		self.wordlist = None
		if filename:
			self.load_wordlist(filename)
		else:
			self.disable_controls()
		self.Show()
		self.table.update(self.wordlist)

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
		self.CreateStatusBar()
		# table
		self.table = WordlistTable(self, -1, style=wx.LC_REPORT)

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

	def load_wordlist(self, filename):
		'''load wordlist from file'''
		filename = os.path.abspath(filename)
		self.SetStatusText('Reading data from file...')
		with open(filename, 'r') as f:
			text = unicode(f.read(), 'utf-8')
		self.wordlist = Wordlist(text)
		self.SetStatusText('Data read.')
		self.dirname = os.path.dirname(filename)
		self.filename = os.path.basename(filename)
		self.enable_controls()

	def on_open(self, event, filename=''):
		'''open a text file and generate wordlist'''
		dialog = wx.FileDialog(self, message='', defaultDir=self.dirname,
				defaultFile=self.filename, wildcard='*', style=wx.OPEN)
		answer = dialog.ShowModal()
		if answer == wx.ID_OK:
			self.load_wordlist(dialog.GetPath())
			self.table.update(self.wordlist)
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
			self.SetStatusText('Saving file...')
			tab = ['{0}\t{1}\r\n'.format(w.encode('utf-8'), f)
					for w, f in self.table.get_sorted()]
			with open(filename, 'w') as f:
				f.writelines(tab)
			self.SetStatusText('File saved.')

	def on_sort(self, event):
		'''sort wordlist'''
		self.table.sortbyend = self.viewbyend.IsChecked()
		self.table.sortbyfreq = self.viewbyfreq.IsChecked()
		self.table.update()

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


