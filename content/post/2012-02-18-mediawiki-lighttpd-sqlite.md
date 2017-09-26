---
title:      MediaWiki with Lighttpd & SQLite on Ubuntu
author:     Eric Gustafson
date:       2012-02-18
slug:       mediawiki-lighttpd-sqlite
aliases:    ["mediawiki-lighttpd-sqlite.html"]
tags:       [lighttpd, sqlite, mediawiki, wiki]
categories: "HowTo"
---

In rebuilding an old, and rarely used server that runs [MediaWiki](https://www.mediawiki.org/) I
reconsidered how to install all of the dependencies that MediaWiki
sits on top of. My goal was to choose lightweight components. The only
thing that would run on this web server would be MediaWiki, and the
wiki would be lightly used. I concluded the following components were
likely more suitable choices than the defaults MediaWiki and/or
Ubuntu’s package system used.

* [Lighttpd](http://www.lighttpd.net/)
* [SQLite](https://www.sqlite.org)

The second goal was, based on my preference for Ubuntu as a
distribution, build MediaWiki on top of Ubuntu using just Ubuntu
packages, no source installation. The principal value in this is that
over time the components in use can be simply upgraded using the stock
Ubuntu package mechanisms (i.e. `apt-get upgrade`).

The following is the sequence I used to install MediaWiki. This
installation guide is based on Ubuntu Oneiric (11.10).

# Install Prerequisites

(note, `sudo` is generally required, but dropped from the commands
below)

```sh
# apt-get install lighttpd
# apt-get install php5-cgi php5
```

next, edit ``/etc/php5/cgi/php.ini`` to enable php5 in lighttpd and
uncomment the line:

```
cgi.fix_pathinfo=1
```

Then enable the fastcgi configuration in lighttpd:

```sh
# lighttpd-enable-mod fastcgi
# lighttpd-enable-mod fastcgi-php
# service lighttpd force-reload
```

Install php5-sqlite:

```sh
# apt-get install php5-sqlite
# service lighttpd restart
```

Install optional extras that MediaWiki will take advantage of:

```sh
# apt-get install imagemagick php5-gd php5-cli
# service lighttpd restart
```

# Install MediaWiki

Note: The MediaWiki package in Ubuntu (Oneiric) has 'mysql-server’
listed as a *recommends* dependency. This has the implication that
unless explicitly forced to **NOT** include the dependency, it will be
included as part of the package install. This is accomplished with the
``--no-install-recommends``.

```sh
# apt-get --no-install-recommends install mediawiki
# apt-get install mediawiki-math
```

# Configure MediaWiki

Add the following to lighttpd's configuration:

```apache
alias.url += ( "/wiki" => "/var/lib/mediawiki/" )
```

restart lighttpd to effect the configuration change:

```sh
# service lighttpd restart
```

Create a data directory for MediaWiki to store the SQLite database in:

```sh
# mkdir /var/lib/mediawiki-data
# chown www-data.www-data /var/lib/mediawiki-data
```

Browse to the wiki root: ``http://hostname/wiki`` and complete
configuration through the web browser.

>
>  \.\.\.
>

Following browser configuration, copy the generated configuration to
the permanent location, as specified on the final browser page:

```sh
# cp /var/lib/mediawiki/config/LocalSettings.php \
     /etc/mediawiki/LocalSettings.php
# chown www-data /etc/mediawiki/LocalSettings.php
# chmod 600 /etc/mediawiki/LocalSettings.php
# rm -rf /var/lib/mediawiki/config
```

Done.
