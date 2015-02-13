#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Eric Gustafson'
SITENAME = u'Stuff I\'ve Figured Out'
SITEURL = ''
SITESUBTITLE = u'A catalog of technical solutions, or hackery -- you decide.'

PATH = 'content'

# default STATIC_PATHS is ['images']
#STATIC_PATHS = ['images']

TIMEZONE = 'US/Mountain'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social widget
SOCIAL = ( ('twitter', 'http://twitter.com/elfwerks'),
           ('delicious', 'http://delicious.com/elfwerks'),
           ('linkedin', 'http://www.linkedin.com/in/ericggustafson/'),
           ('github', 'https://github.com/egustafson'), )

DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('IPv6 Check', 'http://ipv6-address.eu/'),)
LINKS = (('Brian Aker', 'http://krow.net/'),
         ('Andrew Hutchings', 'http://linuxjedi.co.uk/'),
         ('Patrick Galbraith', 'http://patg.net/'),
         ('Yazz Atlas', 'http://askyazz.com/'),)

DEFAULT_PAGINATION = 5

TYPOGRIFY = True

TWITTER_USERNAME = 'elfwerks'
#GITHUB_URL = 'https://github.com/egustafson/egustafson.github.com'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

######################################################################
## Comments - Disqus

## enabled in the publishconf.py
#DISQUS_SITENAME = "egustafson"

######################################################################
## Theme specific -- pelican-bootstrap3
##
THEME = '/home/gustafer/scm/pelican-bootstrap3'

BOOTSTRAP_THEME = 'flatly'
BOOTSTRAP_FLUID = True

