#!/usr/bin/env python2

'''cli.py - the command-line user interface of the word list'''

import re
from wl import Wordlist

class CLI():
	'''command line interface for the wordlist'''

	def __init__(self, filename, stoplists = None,
			freqsort = False, endsort = False):
		self.stoplist = []
		if stoplists:
			for s in stoplists:
				with open(s, 'r') as f:
					L = unicode(f.read(), 'utf-8')
					L = re.findall(u'(?u)\w+',
							L.lower())
					self.stoplist.extend(L)
		with open(filename, 'r') as f:
			self.wordlist = Wordlist(unicode(f.read(), 'utf-8'),
					self.stoplist)
		self.endsort = endsort
		self.freqsort = freqsort

	def get_sorted(self):
		'''return sorted wordlist'''
		if self.endsort:
			return self.wordlist.items_by_wordend()
		if self.freqsort:
			return self.wordlist.most_common()
		return sorted(self.wordlist.items())

	def print_table(self):
		'''print wordlist as a table'''
		values = self.get_sorted()
		llen = max([len(s) for s, i in values])
		rlen = max([len(str(i)) for s, i in values])
		align = '<'
		if self.endsort:
			align = '>'
		print '+-{0}-+-{1}-+'.format(llen * '-', rlen * '-')
		for l, r in values:
			print u'| {0:{align}{llen}} | {1:<{rlen}} |'.format(
					l, r, align=align, llen=llen,
					rlen=rlen)
		print '+-{0}-+-{1}-+'.format(llen * '-', rlen * '-')

	def print_tabdelimited(self):
		'''print wordlist as tab-delimited text'''
		values = self.get_sorted()
		for l, r in values:
			print u'{0}\t{1}'.format(l, r)


