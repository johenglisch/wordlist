#!/usr/bin/env python2
# 

#########################################################################
# programme	: wordlist                                              #
# description	: class of a wordlist                                   #
# last edit	: 27-Jul-2012                                           #
#	by	: Johannes Englisch                                     #
#########################################################################

import re

class WordList():
	'''class of a word list

	attributes:
		raw_text:	umodified tex (unicode)
		text:		text without capitals or non-word chars
		words:		words and their frequencies (list of tupels)
		stoplist:	a list of words that should be ignored
	'''

	def __init__(self, text, stoplist=None):
		self.raw_text = text
		self.stoplist = []
		if stoplist:
			self.stoplist = stoplist
		self.text = re.sub('(?u)[\W\d]', ' ', self.raw_text.lower())
		self.words = [(s, self.text.count(s))
			for s in set(self.text.split())
			if not s in self.stoplist]
		self.sort_by_word()

	def sort_by_word(self):
		'''sort the wordlist by word beginnings'''
		self.words.sort()

	def sort_by_wordend(self):
		'''sort the wordlist by word endings'''
		L = [(w[::-1], f) for w, f in self.words]
		L.sort()
		self.words = [(w[::-1], f) for w, f in L]

	def sort_by_frequency(self):
		'''sort the wordlist by word frequency'''
		L = [(f, w) for w, f in self.words]
		L.sort()
		L.reverse()
		self.words = [(w, f) for f, w in L]


