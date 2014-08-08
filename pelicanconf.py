#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eric Gustafson'
SITENAME = u'Stuff I\'ve Figured Out'
SITEURL = ''
SITESUBTITLE = u'A catalog of technical solutions, or hackery -- you decide.'

PATH = 'content'

TIMEZONE = 'US/Mountain'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('IPv6 Check', 'http://ipv6-address.eu/'),)

# Social widget
SOCIAL = ( ('twitter', 'http://twitter.com/elfwerks'),
           ('delicious', 'http://delicious.com/elfwerks'),
           ('linkedin', 'http://www.linkedin.com/in/ericggustafson/'),
           ('github', 'https://github.com/egustafson'), )

DEFAULT_PAGINATION = 4

TYPOGRIFY = True

TWITTER_USERNAME = 'elfwerks'
#GITHUB_URL = 'https://github.com/egustafson/egustafson.github.com'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
