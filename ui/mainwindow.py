#!/usr/bin/env python2

'''mainwindow.py - the main window of the word list GUI'''

__all__ = ['MainWindow']

import os
import wx
from wl import Wordlist
from textview import TextView
from finddlg import FindDlg
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
		searchterm	term that is searched within the list
		lasthit		index of the last found item
		parent		the parent window
		wordlist	the wordlist to be displayed
	'''

	def __init__(self, parent, *args, **kwargs):
		wx.ListCtrl.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.wordlist = None
		self.sortbyend = False
		self.sortbyfreq = False
		self.searchterm = ''
		# drag'n'drop support
		droptarget = TableDND(self)
		self.SetDropTarget(droptarget)

	def find(self):
		'''search for first occurence of self.searchterm'''
		while True:
			sel = self.GetNextSelected(-1)
			if sel == -1:
				break
			self.Select(sel, False)
		self.lasthit = self.FindItem(-1, self.searchterm,
				partial = True)
		if self.lasthit == -1:
			self.parent.SetStatusText('Search term not found')
		else:
			self.Select(self.lasthit)
			self.Focus(self.lasthit)

	def find_next(self):
		'''show next occurence of self.searchterm'''
		newhit = self.FindItem(self.lasthit + 1, self.searchterm,
				partial = True)
		if newhit == -1:
			self.parent.SetStatusText('Search reached the end. Starting from the beginning.')
			self.find()
		else:
			self.Select(self.lasthit, False)
			self.Select(newhit)
			self.Focus(newhit)
			self.lasthit = newhit

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
			self.InsertColumn(0, 'word', align,
					width = 120)
			self.InsertColumn(1, 'frequency',
					wx.LIST_FORMAT_RIGHT,
					width = 90)
			for i in values:
				self.Append(i)
		self.parent.SetStatusText('Wordlist updated.')


class MainWindow(wx.Frame):
	'''main frame for wordlist programme
	
	attributes:
		dirname		directory of the text file
		filename	file name of the text file
		wordlist	the wordlist
		searchterm	the word currently searched for
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
		menufile.AppendSeparator()
		filequit = menufile.Append(wx.ID_EXIT,
				'&Quit\tCtrl-Q',
				'Quit the Wordlist programme')
		menubar.Append(menufile, '&File')
		menuedit = wx.Menu()
		self.editfind = menuedit.Append(wx.ID_FIND,
				'&Find...\tCtrl-F',
				'Search for a word in the wordlist')
		self.editfindnext = menuedit.Append(wx.ID_ANY,
				'Find ne&xt\tCtrl-G',
				'Show next result of the search')
		menubar.Append(menuedit, '&Edit')
		menuview = wx.Menu()
		self.viewbyword = menuview.AppendRadioItem(wx.ID_ANY,
				'Sort by beginning of &word\tCtrl-1',
				'Sort the wordlist by the beginning of the words')
		self.viewbyend = menuview.AppendRadioItem(wx.ID_ANY ,
				'Sort by &end of word\tCtrl-2',
				'Sort the wordlist by the end of the words')
		self.viewbyfreq = menuview.AppendRadioItem(wx.ID_ANY,
				'Sort by &frequency\tCtrl-3',
				'Sort the wordlist by the occurences of the words')
		menubar.Append(menuview, '&View')
		menutools = wx.Menu()
		self.toolsstoplist = menutools.Append(wx.ID_ANY,
				'Edit &Stoplist...\tCtrl-E',
				'Edit the stoplist')
		self.toolsview = menutools.Append(wx.ID_ANY,
				'&View text...\tCtrl-T',
				'View the text the wordlist was created from')
		menubar.Append(menutools, '&Tools') 
		self.SetMenuBar(menubar)
		# menu events
		self.Bind(wx.EVT_MENU, self.on_open, fileopen)
		self.Bind(wx.EVT_MENU, self.on_save, self.filesave)
		self.Bind(wx.EVT_MENU, self.on_quit, filequit)
		self.Bind(wx.EVT_MENU, self.on_find, self.editfind)
		self.Bind(wx.EVT_MENU, self.on_findnext, self.editfindnext)
		self.Bind(wx.EVT_MENU, self.on_sort, self.viewbyword)
		self.Bind(wx.EVT_MENU, self.on_sort, self.viewbyend)
		self.Bind(wx.EVT_MENU, self.on_sort, self.viewbyfreq)
		self.Bind(wx.EVT_MENU, self.on_viewtext, self.toolsview)
		self.Bind(wx.EVT_MENU, self.on_stoplist, self.toolsstoplist)
		# toolbar
		self.toolbar = self.CreateToolBar()
		tb_open = self.toolbar.AddLabelTool(wx.ID_OPEN,
				label='Open',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR),
				shortHelp='Open text file',
				longHelp='Open a text file and create a wordlist from it')
		tb_save = self.toolbar.AddLabelTool(wx.ID_SAVE, label='Save',
				bitmap=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR),
				shortHelp='Save wordlist',
				longHelp='Save the wordlist to a text file')
		self.toolbar.AddSeparator()
		self.tb_stoplist = self.toolbar.AddLabelTool(wx.ID_ANY,
				label = 'Edit stoplist',
				bitmap = wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR),
				shortHelp = 'Edit stoplist',
				longHelp = 'Edit the stop list in a new window')
		self.tb_viewtext = self.toolbar.AddLabelTool(wx.ID_ANY,
				label='View text',
				bitmap = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_TOOLBAR),
				shortHelp = 'View text',
				longHelp = 'View the text the wordlist was created from')
		self.Bind(wx.EVT_TOOL, self.on_open, tb_open)
		self.Bind(wx.EVT_TOOL, self.on_save, tb_save)
		self.Bind(wx.EVT_TOOL, self.on_stoplist, self.tb_stoplist)
		self.Bind(wx.EVT_TOOL, self.on_viewtext, self.tb_viewtext)
		self.toolbar.Realize()
		# statusbar
		self.CreateStatusBar()
		# table
		self.table = WordlistTable(self, wx.ID_ANY, style=wx.LC_REPORT)

	def disable_controls(self):
		'''disable controls'''
		self.filesave.Enable(False)
		self.editfind.Enable(False)
		self.editfindnext.Enable(False)
		self.viewbyword.Check(True)
		self.viewbyword.Enable(False)
		self.viewbyend.Enable(False)
		self.viewbyfreq.Enable(False)
		self.toolsstoplist.Enable(False)
		self.toolsview.Enable(False)
		self.toolbar.EnableTool(wx.ID_SAVE, False)
		self.toolbar.EnableTool(self.tb_stoplist.GetId(), False)
		self.toolbar.EnableTool(self.tb_viewtext.GetId(), False)

	def enable_controls(self):
		'''enable controls'''
		self.filesave.Enable(True)
		self.editfind.Enable(True)
		self.viewbyword.Enable(True)
		self.viewbyend.Enable(True)
		self.viewbyfreq.Enable(True)
		self.toolsstoplist.Enable(True)
		self.toolsview.Enable(True)
		self.toolbar.EnableTool(wx.ID_SAVE, True)
		self.toolbar.EnableTool(self.tb_stoplist.GetId(), True)
		self.toolbar.EnableTool(self.tb_viewtext.GetId(), True)

	def load_wordlist(self, filename):
		'''load wordlist from file'''
		filename = os.path.abspath(filename)
		self.SetStatusText('Reading data from file...')
		try:
			with open(filename, 'r') as f:
				text = unicode(f.read(), 'utf-8')
		except Exception as e:
			wx.MessageBox(str(e), '', wx.OK | wx.ICON_ERROR)
			self.SetStatusText('Could not read data.')
		else:
			self.wordlist = Wordlist(text)
			self.SetStatusText('Data read.')
			self.SetTitle(os.path.basename(filename))
			self.dirname = os.path.dirname(filename)
			self.filename = os.path.basename(filename)
		self.enable_controls()

	def on_find(self, event):
		'''search for word in wordlist'''
		dlg = FindDlg(self, wx.ID_ANY)
		response = dlg.ShowModal()
		if response == wx.ID_OK:
			self.table.searchterm = dlg.searchterm
			self.table.find()
			self.editfindnext.Enable(True)
		dlg.Destroy()

	def on_findnext(self, event):
		'''search for next occurence of the search term'''
		self.table.find_next()

	def on_open(self, event):
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
			try:
				with open(filename, 'w') as f:
					f.writelines(tab)
			except Exception as e:
				wx.MessageBox(str(e), '', wx.OK
						| wx.ICON_ERROR)
				self.SetStatusText('Could not save file.')
			else:
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
			self.wordlist = Wordlist(self.wordlist.text, dialog.stoplist)
			self.table.update(self.wordlist)
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


