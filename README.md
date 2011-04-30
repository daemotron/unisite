UniSite Website Backend
=======================

About UniSite
-------------

UniSite is the software running my website (http://www.my-universe.com).
It is currently subject to a (partial) rewrite to fix some little devilries
still hidden in the code.

UniSite is written in Python and uses the [Django](http://www.djangoproject.com)
Framework.

Requirements
------------

You need at least the following software to run UniSite on your computer:

*   [Python](http://www.python.org/) >= 2.6 (but < 3.x)
*   [Django](http://www.djangoproject.com) >= 1.3
*   [Docutils](http://docutils.sourceforge.net/) >= 0.7
*   [Universal Feed Parser](http://feedparser.org/) >= 5.0
*   [Pygments](http://pygments.org/) >= 1.4

Installation Instructions
-------------------------

Check out the UniSite sources from GitHub:

    git clone git://github.com/daemotron/unisite.git

Now you can create a settings file:

    cp unisite/src/unisite/settings.py.dist unisite/src/unisite/settings.py

Edit the freshly created `settings.py` to meet your needs (particularly in terms
of the relational database management system you intend to use, and of course
regarding path specifications).

When you are done, you can synchronize the database:

    cd unisite/src/unisite
    python manage.py syncdb

If this went smooth and without error messages, you can start the built-in webserver
(only for development and testing purposes):

    python manage.db runserver

If not, you should check your `settings.py`. Most probably, there's something wrong
with your database configuration.

Resources
---------

The UniSite code is hosted at [GitHub](https://github.com/daemotron/unisite). There
is a second project site at http://projects.my-universe.com/projects/unisite where
you may find other sources of information, like a bug tracker and a wiki. 