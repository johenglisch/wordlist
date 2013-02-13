#!/usr/bin/env python

'''Word list install script.

Sets meta data and installs Wordlist.

'''

from distutils.core import setup

DESCRIPTION = '''Simple word list generator.

This programme creates word lists out of plain text files.  Those word lists
can be saved as tab-delimited text files or passed on to other programmes for
further analysis.

This package comes with a graphical and a command-line user interface.

Running the graphical user interface requires wxPython.

'''                 


# TODO url, download_url
config = {'name': 'Wordlist',
          'version': '1.0',
          'author': 'Johannes Englisch',
          'author_email': 'cyberjoe0815@hotmail.com',
          'description': 'Simple word list creator',
          'long_description': DESCRIPTION,
          'classifiers': ['Development Status :: 4 - Beta',
                          'Environment :: Console',
                          'Environment :: MacOS X',
                          'Environment :: Win32 (MS Windows)',
                          'Environment :: X11 Applications :: GTK',
                          'Intended Audience :: Science/Research',
                          'License :: OSI Approved :: MIT License',
                          'Operating System :: OS Independent',
                          'Programming Language :: Python :: 2'
                          'Programming Language :: Python :: 2.7',
                          'Topic :: Text Processing :: Linguistic'],
          'packages': ['wordlist'],
          'scripts': ['wordlist.pyw', 'wordlist_cli.py']}


setup(**config)
