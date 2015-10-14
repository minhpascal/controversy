.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots
.. |ui| image:: http://ocha.2pitau.org/img/biography/ui.jpg

Controversy
~~~~~~~~~~~~

Joint mining of news text and social media to discover controversial points in news.

+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+
| Live demo                             | Publications                  | Authors                                                                               |
+=======================================+===============================+=======================================================================================+
| `controversy.2pitau.org`_             | `IEEE Big Data 2015`_         | Ismini Lourentzou |ui|, Graham Dyer |ui|, Abhishek Sharma |ui|, ChengXiang Zhai |ui|  |
+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+
| `controversy.web.engr.illinois.edu`_  | `UIUC PURE Conference 2015`_  | Graham Dyer |ui| (mentee), Ismini Lourentzou |ui| (mentor)                            |
+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+
|  `controversy.2pitau.org`_            | (full paper in progress)      | ?                                                                                     |
+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+

Pending
--------

We're currently preparing this server for a demo during **IEEE Big Data 2015 on October 29th**.

Scoring todo
============

Switch to conditional probability for linguistic features:
  
Recall :math:`p(X_sent = X_i) = \frac{P(x_i) \in C_i^'}{\sum_{i=1}^{z} f(x_i) \in C_i^'}` is equivalent to the number of comments (tweets) with sentiment :math:`x_i` divided by the total number of comments. Therefore, :math:`p(X_caps = x_i) = p(X_sent = x_i | C_i^' \in Caps) = \frac{p(X_sent = x_i \cap C_i^' \in Caps}{p(C_i^' \in Caps)` where :math:`Caps`` is the set of comments that have capitalized terms. This works similarly for the extreme lexicon.


Demo todo
=========

* all-caps scoring variable
* show user their graphs 
* average same-day points in matplotlib
* tokenizer needs to remove acronyms
* (more than NYTimes, Reuters, and AP. CNN is next)


Running for development
-----------------------

If you'd like to reproduce our results, we encourage you to use the demo or look at our `API spec`_ for raw ``json`` results. Alternatively, you can clone this repository and run the server yourself.

Please use Python 2.7.x

If you're on a fresh machine or don't use git, Python, or MySQL much, read the two paragraphs below before proceeding.

#. ``$ git clone https://github.com/gdyer/controversy``
#. ``$ cd controversy/controversy``
#. ``$ mv config.py.default config.py``, and change credentials where marked as ``REQUIRED``. You'll need to register for NYTimes' `Article Search API`_ and `Twitter's API`_.
#. create a MySQL database called "controversy" with ``source schema.sql``
#. install redis, run ``redis-server``. Leave with ``<Ctrl>+C`` only if on Debian/Ubuntu. Otherwise, keep ``redis-server`` open, and continue in a new shell.
#. satisfy SciPy `dependencies`_
#. ``$ pip install virtualenv``
#. ``$ virtualenv venv``
#. ``$ . venv/bin/activate``
#. ``$ pip install -r requirements.txt`` will install requirements into the virtual environment to limit bloat on your actual machine
#. ``$ python``
        - ``>>> import nltk``
        - ``>>> nltk.download('stopwords', 'punkt')``
	- ``<Ctrl>+D``
#. ``$ python app.py``
#. navigate to ``localhost:4040`` in your browser. See `API spec`_ for routes.

This should would out of the box on Debian-based machines. There, MySQL is ``mysql-server``, redis is ``redis-server`` and the SciPy packages are ``python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose``.

Apple changed permissions in El Capitan. We recommend using the ``brew`` package manager to try to get around these. Install with ``$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"``. Ensure you have XCode CLI tools installed (install XCode for the Mac App Store and ``$ xcode-select --install``). ``brew`` packages of interest include ``redis``, ``mysql`` (then do ``$ mysql.server start``). You should also have ``pip`` to install the Python-specific dependencies: ``sudo easy_install pip``. El Capitan users may need to reinstall Python to get around strange "permission denied" errors: ``brew reinstall python``.


------


.. image:: http://ocha.2pitau.org/img/biography/uiuc.gif
	:target: http://cs.illinois.edu

.. _IEEE Big Data 2015: http://ocha.2pitau.org/pdf/big-data-2015.pdf
.. _UIUC PURE Conference 2015: http://ocha.2pitau.org/pdf/pure.pdf
.. _controversy.2pitau.org: http://controversy.2pitau.org
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
.. _API spec: controversy/README.rst
.. _dependencies: http://www.scipy.org/install.html
.. _Article Search API: http://developer.nytimes.com/docs/read/article_search_api_v2
.. _Twitter's API: https://apps.twitter.com/
