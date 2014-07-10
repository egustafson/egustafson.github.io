Eric Gustafson's personal blog site.
====================================

Instructions to self
--------------------

How-to update & publish:

.. code-block:: tcsh

   make html     ## ensure it compiles properl
   ## (optional) pull the page up iin a browser
   make publish
   ghp-import -b master output
   git push origin master


References
----------

- `Pelican Tips <http://docs.getpelican.com/en/3.4.0/tips.html>`
- `ghp-import <https://github.com/davisp/ghp-import>`
