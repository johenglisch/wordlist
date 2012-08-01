#!/usr/bin/env python2

#########################################################################
# programme	: main.py                                               #
# description	: execute wordlist generator                            #
# last edit	: 01-Aug-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import os
import sys
import wx

import wlcli
import wlwx

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
	print '        -p, --print-table       print result as a table'
	print '        -s, --stoplist <file>   add stoplist file'
	print '        -t, --tab-delimited     print result as tab-delimited text'


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
	if printtable or tabdelimited:
		if not filename:
			print 'No text file given'
			usage()
			return
		cli = wlcli.CLI(filename, stoplistfiles, freqsort, endsort)
		if printtable:
			cli.print_table()
		else:
			cli.print_tabdelimited()
	else:
		wxapp = wx.App()
		wlwx.MainWindow(filename, stoplistfiles, None)
		wxapp.MainLoop()


if __name__ == '__main__':
	main(sys.argv)


