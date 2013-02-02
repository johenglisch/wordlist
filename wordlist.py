#!/usr/bin/env python

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
import ui.cli


forcecli = False
try:
	import wx
except ImportError:
	sys.stderr.write('Warning: wxPython not found. Falling back to CLI\n');
	forcecli = True
else:
	import ui.mainwindow

progname = os.path.basename(sys.argv[0])


def usage():
	'''print usage message'''
	print 'usage: {0} [options] file'.format(progname)
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
				sys.stderr.write('Error: No stoplist file given\n')
				return
			if s == '-h' or s == '--help':
				usage()
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
			sys.stderr.write('Error: Unknown option: {0}\n'.format(s))
			return
		if stoplist:
			stoplistfiles.append(s)
			stoplist = False
			continue
		if filename:
			sys.stderr.write('Error: Only one text file allowed\n')
			return
		filename = s
	if stoplist:
		sys.stderr.write('Error: Missing stop list file\n')
		return
	if freqsort and endsort:
		sys.stderr.write('Error: Conflicting sort order options\n')
		return
	if printtable or tabdelimited or forcecli:
		if not filename:
			sys.stderr('Error: Missing text file\n')
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


