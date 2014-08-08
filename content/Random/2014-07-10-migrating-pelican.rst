:title:      Migrating to Pelican
:date:       2014-07-10
:slug:       migrating-pelican
:author:     Eric Gustafson
:tags:       pelican, blog, python
:status:     draft

After a 2 year hiatus, I'm working towards writing more about work and
technology.  I gave Octopress_ a try, but in the end concluded that I
wanted a Python_ solution.  I evaluated a few packages:  Hyde_,
Nikola_, and Pelican_.  There were two other Python based static site
generators that I did not look at, but should probably take a look at
-- both got positive mentions in the blogosphere:  Acrylamid_ and mynt_.

.. _Octopress:  http://octopres.org
.. _Python:     http://python.org
.. _Hyde:       http://hyde.github.io/
.. _Nikola:     http://getnikola.com/
.. _Pelican:    http://blog.getpelican.com/
.. _mynt:       http://mynt.uhnomoli.com/
.. _Acrylamid:  http://posativ.org/acrylamid/index.html

Why did I choose what I chose?  Everyone has different motivations and
I find understanding peoples motivations in more insightful than
debating "what's better" -- to that end, here were my motivations and
conclusions:

Static Site
  My motivations are the standard and obvious.  This is a simple site
  that I'm blogging to.  I'm a software developer so I have greater
  mastery of emacs than Word as well as a hard time keeping files in a
  folder when there's version control.  GitHub has turned common
  development tool into a social movement and to that end `GitHub
  Pages`_ is an awesome advancement to the "state of the art" and a
  key aspect of the `Social` in Social Coding.

.. _`GitHub Pages`:  https://pages.github.com

Python
  \.\.\. why I chose Python

.. a comment to get better spacing between items in the def-list

reStructuredText
  \.\.\. why I'm giving reStructuredText_ a try (include a reference
  to the rst-cheetsheet_)

.. _reStructuredText:  http://docutils.sourceforge.net/rst.html
.. _rst-cheetsheet: https://github.com/ralsina/rst-cheatsheet/blob/dfaf3e283ee5df9d4c4b50ff9be2fa7db93c0427/rst-cheatsheet.pdf?raw=true

Pelican
  \.\.\. why I chose Pelican

Migration Process
-----------------

So that I have a (reproducible) record of how I to where I am, the
following is what I did to setup the site, including migrating the
old, Octopress content.

1. Get up and running under Pelican

  1. Install Pelican from pip (use GitHub source)
  2. Port old articles from Markdown to reStructuredText
  3. Tweak basic configuration to align with existing GH-Pages site.

2. Move things under git and commit

  1. Clone a new copy of the GH repo.
  2. Create an archival branch and push the old source to it.
  3. Stomp the 'source' branch with the new, Pelican source.
  4. Generate the production site into a local directory.
  5. ?? use :code:``ghp-import`` to commit to the 'gh-pages' branch.
  6. git-push from 'gh-pages' to the 'master' branch on GitHub.





Todo(s)
-------

Further exploration and refinement I'd like to undertake -- in no
particular order:

Cleanup blogroll
  The blogroll and social links at the bottom of each page could use
  some tweaking.

Tweak the Theme
  I used the example theme from the getting started by `Smashing
  Magazine`_ and it's a pretty good starting point.  There are
  certainly a few tweaks that may or may not be doable through the
  config.  I'd also like to change the color scheme which I'm sure
  will require tweaking the theme.

.. _`Smashing Magazine`: http://coding.smashingmagazine.com/2009/08/04/designing-a-html-5-layout-from-scratch/ 

(re)Theme
  I've let my HTML / CSS skills dwindle; I don't use them much, but
  being able to craft an HTML page for some evil purpose is a good
  skill for any software person to have in their back pocket.  It
  looks like the Bootstrap_ project has gained a reasonable reputation
  in this space and creating a Bootstrap_ derived theme would
  certainly blow the dust off of my web page-ie skills.

.. _Bootstrap:  http://getbootstrap.com

