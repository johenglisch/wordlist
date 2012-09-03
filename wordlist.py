#!/usr/bin/env python2

'''wordlist.py - a simple word list generator

This script generates a wordlist from any plain text file.
'''

__author__ = 'Johannes Englisch'
__license__ = '''Copyright (c) 2012 Johannes Englisch

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''


import os
import sys

forcecli = False
try:
	import wx
except ImportError, error:
	print 'Could not import wxPython. Forcing command-line mode'
	forcecli = True

import ui.cli
if not forcecli:
	import ui.mainwindow

progname = os.path.basename(sys.argv[0])


def usage(longmsg=False):
	'''print usage message'''
	print 'usage: {0} [options] file'.format(progname)
	if not longmsg:
		print "Try '{0} -h' for more information".format(progname)
		return
	print
	print 'options:'
	print '        -e, --sort-by-wordend   sort wordlist by word end'
	print '        -f, --sort-by-freq      sort wordlist by frequency'
	print '        -h, --help              show this message'
	print '        -p, --print-table       print table to standard output'
	print '        -s, --stoplist <file>   add stoplist file'
	print '        -t, --tab-delimited     print tab-delimited text to standard output'


def main(args):
	# argument handling
	filename = ''
	stoplist = False
	stoplistfiles = []
	printtable = False
	tabdelimited = False
	freqsort = False
	endsort = False
	for s in args[1:]:
		if s.startswith('-'):
			if stoplist:
				print 'No stoplist file given'
				usage()
				return
			if s == '-h' or s == '--help':
				usage(True)
				return
			if s == '-e' or s == '--sort-by-wordend':
				endsort = True
				continue
			if s == '-f' or s == '--sort-by-freq':
				freqsort = True
				continue
			if s == '-s' or s == '--stoplist':
				stoplist = True
				continue
			if s == '-p' or s == '--print-table':
				printtable = True
				continue
			if s == '-t' or s == '--tab-delimited':
				tabdelimited = True
				continue
			print 'Unknown option: {0}'.format(s)
			usage()
			return
		if stoplist:
			stoplistfiles.append(s)
			stoplist = False
			continue
		if filename:
			print 'Only one file allowed'
			usage()
			return
		filename = s
	if stoplist:
		print 'No stoplist file given'
		usage()
		return
	if freqsort and endsort:
		print 'Conflicting sort orders given'
		return
	if printtable or tabdelimited or forcecli:
		if not filename:
			print 'No text file given'
			usage()
			return
		cli = ui.cli.CLI(filename, stoplistfiles, freqsort, endsort)
		if tabdelimited:
			cli.print_tabdelimited()
		else:
			cli.print_table()
	else:
		wxapp = wx.App()
		ui.mainwindow.MainWindow(filename, stoplistfiles, None)
		wxapp.MainLoop()


if __name__ == '__main__':
	main(sys.argv)


