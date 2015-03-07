:title: Pelican Site Generator - HowTo's
:date: 2015-03-06
:slug: pelican-examples
:author: Eric Gustafson
:tags: Pelican, Python, RestructuredText
:status: draft

This (draft) article is simple a place to capture examples of common, or not so,
tasks and markup in Pelican_.

.. _Pelican: http://docs.getpelican.com/

A link to another blog posting: `IPv6 Tunneling over IPv6 Networks`_, 

.. _`IPv6 Tunneling over IPv6 Networks`: {filename}2015-02-25-ipv6-tunneling.rst


And, a figure, which is clickable and opens an SVG:

.. figure:: {filename}/images/voyeur.png
   :align: right
   :width: 100px
   :target: {filename}/images/voyeur.svg
   :alt: voyeur svg

   The Voyeur Image - Caption

Note that I the SVG does not open properly.  I believe because the HTML markup
is not set properly to indicate to the browser how to handle the item.  I
haven't tried this from my github page, but in the python SimpleHTTPServer it
does not come through properly, even though it's mime type appears to be sent as
SVG.  ... currently a mystery.



.. Local Variables:
.. fill-column: 80
.. End:
