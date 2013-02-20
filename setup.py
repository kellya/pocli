#!/usr/bin/env python

from distutils.core import setup

setup (
    name = "pocli",
    version = '0.2.0',
    description = 'General-use pushover.net CLI',
    author= 'Alex Kelly',
    author_email = 'kellya@arachnitech.com',
    scripts=['pocli.py'],
    url = 'https://github.com/kellya/pocli',
    long_description = ''' This is a general use CLI for sending messages to 
    the pushover app via calls to pushover's API.  All calls as of 2012-12-14
    are supported''',
    license = 'GPL',
    #py_modules = ['pocli']
  )
