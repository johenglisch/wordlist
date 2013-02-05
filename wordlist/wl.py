#!/usr/bin/env python2

'''wl.py - implementation of the word list itself'''

import re
from collections import Counter


#RE_WORD = re.compile('\w+', re.UNICODE)
RE_WORD = re.compile(r'[^\d\W_]+', re.UNICODE)


class Wordlist(Counter):
    '''Counter subclass for creating a wordlist

    attributes:
        text        unmodified text
        stoplist    stoplist for the wordlist
    '''

    def __init__(self, text, stoplist=None):
        '''Wordlist constructor'''
        super(Wordlist, self).__init__()
        self.text = text
        self.stoplist = []
        if stoplist:
            self.stoplist = stoplist
        words = RE_WORD.findall(text.lower())
        words = [s for s in words if s not in self.stoplist]
        self.update(words)

    def items_by_wordend(self):
        '''return wordlist sorted by the ends of the words'''
        item_list = sorted([(w[::-1], f) for w, f in self.items()])
        return [(w[::-1], f) for w, f in item_list]

    def items_by_wordbeginning(self):
        '''return wordlist sorted by the beginnings of the words'''
        return self.items()

    def items_by_frequency(self):
        '''return wordlist sorted by word frequency'''
        return self.most_common()
