.. |...| unicode:: U+2026 .. ldots

Running the server locally
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is not for the faint-hearted.

Please use Python 2.7.x

#. ``$ git clone https://github.com/SXibolet/controversy``
#. ``$ cd controversy/controversy``
#. get an academic SentiStrength license by sending an email to `the address listed here`_, move the ``jar`` and data into ``sentistrength`` with names ``SentiStrengthCom.jar`` and ``data-11`` respectively. You'll need to be in academia to get a free license.
#. ``$ mv config.py.default config.py``, and change credentials where marked as ``REQUIRED``. You'll need to register for NYTimes' `Article Search`_ and `Community`_ APIs and `Twitter's API`_.
#. create a MySQL database called "controversy" with ``source schema.sql``.
#. install MongoDB and start the server with the default port. Leave with ``<Ctrl>+C`` only if on Debian/Ubuntu. Otherwise, keep ``sudo mongod`` open, and continue in a new shell. NoSQL is ideal for how we do training. We'll soon create a simple way of downloading our data, which, once downloaded, can be loaded into MongoDB with a script we'll also make shortly |...|
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


.. _API spec: https://sxibolet.github.io/docs.html
.. _dependencies: http://www.scipy.org/install.html
.. _Article Search: http://developer.nytimes.com/apps/mykeys
.. _Community: http://developer.nytimes.com/apps/mykeys
.. _Twitter's API: https://apps.twitter.com/
.. _the address listed here: http://sentistrength.wlv.ac.uk
