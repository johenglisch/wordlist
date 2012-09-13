#!/usr/bin/env python2

'''wl.py - implementation of the word list itself'''

import re
from collections import Counter


#re_word = re.compile('\w+', re.UNICODE)
re_word = re.compile('[^\d\W_]+', re.UNICODE)


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
		words = re_word.findall(text.lower())
		words = [s for s in words if s not in self.stoplist]
		self.update(words)

	def items_by_wordend(self):
		'''return wordlist sorted by the ends of the words'''
		L = [(w[::-1], f) for w, f in self.items()]
		L.sort()
		return [(w[::-1], f) for w, f in L]

	def items_by_wordbeginning(self):
		'''return wordlist sorted by the beginnings of the words'''
		return self.items()

	def items_by_frequency(self):
		'''return wordlist sorted by word frequency'''
		return self.most_common()


