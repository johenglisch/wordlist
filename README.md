Wordlist
========

#Description

`Wordlist` is a python script that generates word list from any given
plain text file.

This wordlist then is sortable by the beginnings or the ends of the words, or
by their frequency.
The output can be saved as a tab-delimited textfile for futher processing.

Also the script supports wordlist filtering using stoplists.

The script comes with a graphical user interface, but can also be used on the
command-line.

#Requirements

 * The script requires at least Python 2.7.
 * The graphical user interface requires wxPython (optional).

#Usage

    wordlist.py [options] file

	options:
	        -e, --sort-by-wordend   sort wordlist by word end
	        -f, --sort-by-freq      sort wordlist by frequency
	        -h, --help              show this message
	        -p, --print-table       print table to standard output
	        -s, --stoplist <file>   add stoplist file
	        -t, --tab-delimited     print tab-delimited text to standard output

