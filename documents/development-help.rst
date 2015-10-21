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

These steps should would out of the box on Debian-based machines. There, MySQL is ``mysql-server``, redis is ``redis-server`` and the SciPy packages are ``python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose``.

Apple changed permissions in El Capitan. We recommend using the ``brew`` package-manager to try to get around these. Install with ``$ ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"``. Ensure you have XCode CLI tools installed (install XCode for the Mac App Store and ``$ xcode-select --install``). ``brew`` packages of interest include ``redis``, ``mysql`` (then do ``$ mysql.server start``). You should also have ``pip`` to install the Python-specific dependencies: ``sudo easy_install pip``. El Capitan users may need to reinstall Python to get around strange "permission denied" errors: ``brew reinstall python``.


.. _API spec: controversy/README.rst
.. _dependencies: http://www.scipy.org/install.html
.. _Article Search API: http://developer.nytimes.com/docs/read/article_search_api_v2
.. _Twitter's API: https://apps.twitter.com/
