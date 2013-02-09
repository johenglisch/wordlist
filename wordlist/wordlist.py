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


NO_WX = False
try:
    import wx
except ImportError:
    sys.stderr.write('Warning: wxPython not found. Falling back to CLI\n')
    NO_WX = True
else:
    import ui.mainframe

PROG_NAME = os.path.basename(sys.argv[0])


def usage():
    '''print usage message'''
    print 'usage: {0} [options] file'.format(PROG_NAME)
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
    for arg in args[1:]:
        if arg.startswith('-'):
            if stoplist:
                sys.stderr.write('Error: No stoplist file given\n')
                return
            if arg == '-h' or arg == '--help':
                usage()
                return
            if arg == '-e' or arg == '--sort-by-wordend':
                endsort = True
                continue
            if arg == '-f' or arg == '--sort-by-freq':
                freqsort = True
                continue
            if arg == '-s' or arg == '--stoplist':
                stoplist = True
                continue
            if arg == '-p' or arg == '--print-table':
                printtable = True
                continue
            if arg == '-t' or arg == '--tab-delimited':
                tabdelimited = True
                continue
            sys.stderr.write('Error: Unknown option: {0}\n'.format(arg))
            return
        if stoplist:
            stoplistfiles.append(arg)
            stoplist = False
            continue
        if filename:
            sys.stderr.write('Error: Only one text file allowed\n')
            return
        filename = arg
    if stoplist:
        sys.stderr.write('Error: Missing stop list file\n')
        return
    if freqsort and endsort:
        sys.stderr.write('Error: Conflicting sort order options\n')
        return
    if printtable or tabdelimited or NO_WX:
        if not filename:
            sys.stderr.write('Error: Missing text file\n')
            return
        cli = ui.cli.CLI(filename, stoplistfiles, freqsort, endsort)
        if tabdelimited:
            cli.print_tabdelimited()
        else:
            cli.print_table()
    else:
        wxapp = wx.App()
        ui.mainframe.MainFrame(filename, None)
        wxapp.MainLoop()


if __name__ == '__main__':
    main(sys.argv)
