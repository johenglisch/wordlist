#!/usr/bin/env python

from distutils.core import setup

PKG_NAME = 'Wordlist'
PKG_VERSION = '1.0'
PKG_AUTHOR = 'Johannes Englisch'
PKG_AUTHOR_EMAIL = 'cyberjoe0815@hotmail.com'
PKG_DESCRIPTION = 'Simple word list creator'
PKG_LONG_DESCRIPTION = '''\
Wordlist is a simple programme that creates word lists out of plain text files.
Those word lists can be saved as tab-delimited text files or passed on to other
programmes for further analysis.

This programme come with an command-line interface as well as with a wxPython
GUI.'''
PKG_CLASSIFIERS = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Environment :: MacOS X',
                   'Environment :: Win32 (MS Windows)',
                   'Environment :: X11 Applications :: GTK',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Text Processing :: Linguistic']
PKG_PACKAGES = ['wordlist']


# TODO url, download_url
setup(name=PKG_NAME,
      version=PKG_VERSION,
      author=PKG_AUTHOR,
      author_email=PKG_AUTHOR_EMAIL,
      description=PKG_DESCRIPTION,
      long_description=PKG_LONG_DESCRIPTION,
      classifiers=PKG_CLASSIFIERS,
      packages=PKG_PACKAGES)
