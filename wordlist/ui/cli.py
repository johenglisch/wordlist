#!/usr/bin/env python2

'''cli.py - the command-line user interface of the word list'''


from wl import Wordlist, RE_WORD


class CLI():
    '''command line interface for the wordlist'''

    def __init__(self, filename, stoplists=None,
                 freqsort=False, endsort=False):
        '''command line interface constructor'''
        self.stoplists = list()
        if stoplists:
            for stopfile in stoplists:
                with open(stopfile, 'r') as inputfile:
                    stoplist = unicode(inputfile.read(), 'utf-8')
                stoplist = RE_WORD.findall(stoplist.lower())
                self.stoplists.extend(stoplist)
        with open(filename, 'r') as inputfile:
            self.wordlist = Wordlist(unicode(inputfile.read(), 'utf-8'),
                                     self.stoplists)
        self.endsort = endsort
        self.freqsort = freqsort

    def get_sorted(self):
        '''return sorted wordlist'''
        if self.endsort:
            return self.wordlist.items_by_wordend()
        if self.freqsort:
            return self.wordlist.items_by_frequency()
        return sorted(self.wordlist.items_by_wordbeginning())

    def print_table(self):
        '''print wordlist as a table'''
        values = self.get_sorted()
        llen = max([len(s) for s, i in values])
        rlen = max([len(str(i)) for s, i in values])
        align = '<'
        if self.endsort:
            align = '>'
        print '+-{0}-+-{1}-+'.format(llen * '-', rlen * '-').encode('utf-8')
        for word, freq in values:
            print u'| {0:{align}{llen}} | {1:>{rlen}} |'.format(word, freq,
                                                                align=align,
                                                                llen=llen,
                                                                rlen=rlen
                                                                ).encode('utf-8')
        print '+-{0}-+-{1}-+'.format(llen * '-', rlen * '-').encode('utf-8')

    def print_tabdelimited(self):
        '''print wordlist as tab-delimited text'''
        values = self.get_sorted()
        for word, freq in values:
            print u'{0}\t{1}'.format(word, freq).encode('utf-8')
