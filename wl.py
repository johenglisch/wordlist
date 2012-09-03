#!/usr/bin/env python2

'''wl.py - implementation of the word list itself'''

import re
from collections import Counter


class Wordlist(Counter):
	'''Counter subclass for creating a wordlist
	
	attributes:
		text		unmodified text
		stoplist	stoplist for the wordlist
	'''

	def __init__(self, text, stoplist=None):
		super(Counter, self).__init__()
		self.text = text
		self.stoplist = []
		if stoplist:
			self.stoplist = stoplist
		words = re.findall('(?u)\w+', text.lower())
		words = [s for s in words if s not in self.stoplist]
		self.update(words)

	def items_by_wordend(self):
		'''return wordlist sorted by the ends of the words'''
		L = [(w[::-1], f) for w, f in self.items()]
		L.sort()
		return [(w[::-1], f) for w, f in L]


