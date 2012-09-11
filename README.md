Wordlist
========


## Description ##

`Wordlist` is a python script that generates word list from a given plain text
file.

This wordlist then is sortable by the beginnings or the ends of the words, or
by their frequency.  The output can be saved as a tab-delimited textfile for
futher processing.  The script supports wordlist filtering using stop lists.

`Wordlist` comes with both a command-line interface and an optional GUI using
wxPython.

*Note:*  The script assumes the input file to use the UFT-8 encoding.


## Requirements ##

 *	The script requires at least Python 2.7.
 *	The graphical user interface requires wxPython (optional).


## Usage ##

    wordlist.py [options] file

	options:
	        -e, --sort-by-wordend   sort wordlist by word end
	        -f, --sort-by-freq      sort wordlist by frequency
	        -h, --help              show this message
	        -p, --print-table       print table to standard output
	        -s, --stoplist <file>   add stoplist file
	        -t, --tab-delimited     print tab-delimited text to standard output


## License ##

Copyright (c) 2012 Johannes Englisch

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
SOFTWARE.

