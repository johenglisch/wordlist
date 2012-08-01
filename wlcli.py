#!/usr/bin/env python2

#########################################################################
# programme	: wordlist-cli                                          #
# description	: command line word list programme                      #
# last edit	: 27-Jul-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import os
import sys
from wordlist import WordList

progname = os.path.basename(sys.argv[0])


def usage(longmsg=False):
	''' print usage message '''
	print 'usage: {0} [options] file'.format(progname)
	if not longmsg:
		print "Try '{0} -h' for more information".format(progname)
		return
	print
	print 'options:'
	print '        -e, --sort-by-wordend   sort wordlist by word end'
	print '        -f, --sort-by-freq      sort wordlist by frequency'
	print '        -h, --help              show this message'
	print '        -s, --stoplist file     add stoplist file'
	print '        -t, --tab-delimited     show result as tab-delimited text'


class CLI():
	'''command line interface for the wordlist'''

	def __init__(self, wordlist, freqsort=False, endsort=False):
		self.wordlist = wordlist
		self.endsort = endsort
		if endsort:
			self.wordlist.sort_by_wordend()
		self.freqsort = freqsort
		if freqsort:
			self.wordlist.sort_by_frequency()

	def print_table(self):
		'''print wordlist as a table'''
		llen = max([len(s) for s, i in self.wordlist.words])
		rlen = max([len(str(i)) for s, i in self.wordlist.words])
		align = '<'
		if self.endsort:
			align = '>'
		print '+-{0}-+-{1}-+'.format(llen * '-', rlen * '-')
		for l, r in self.wordlist.words:
			print u'| {0:{align}{llen}} | {1:<{rlen}} |'.format(
					l, r, align=align, llen=llen,
					rlen=rlen)
		print '+-{0}-+-{1}-+'.format(llen * '-', rlen * '-')

	def print_tabdelimited(self):
		'''print wordlist as tab-delimited text'''
		for l, r in self.wordlist.words:
			print u'{0}\t{1}'.format(l, r)



def main(args):
	# argument handling
	if len(args) == 1:
		usage()
		return
	filename = ''
	freqsort = False
	endsort = False
	stoplist = False
	tablim = False
	stoplistfiles = []
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
			if s == '-t' or s == '--tab-delimited':
				tablim = True
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
	if not filename:
		print 'No text file given'
		usage()
		return
	if stoplist:
		print 'No stoplist file given'
		usage()
		return
	if freqsort and endsort:
		print 'Conflicting sort orders given'
		return
	# create stoplist
	stoplist = []
	for s in stoplistfiles:
		with open(s) as f:
			lst = unicode(f.read(), 'utf-8').split()
			stoplist.extend(lst)
	# load wordlist
	with open(filename) as f:
		text = unicode(f.read(), 'utf-8')
	cli = CLI(WordList(text, stoplist), freqsort=freqsort,
			endsort=endsort)
	# print
	if tablim:
		cli.print_tabdelimited()
	else:
		cli.print_table()


if __name__ == '__main__':
	main(sys.argv)


