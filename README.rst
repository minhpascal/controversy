Controversy
~~~~~~~~~~~

Joint Mining of News Text and Social Media to Discover Controversial Points in News

``requirements.txt`` and setup changed on 4/22

running the server
------------------
* ``cd server``

running the server::

	echo "import os
	DB_HOST = 'localhost'
	DB_PORT = 3306
	DB_NAME = 'controversy'
	DB_PASSWORD = None # or 'password' if you made one
	DB_USER = 'root' # or your computer's name
	SECRET_KEY = os.urandom(24)
	API_KEY = 'api key' # create this and below @ apps.twitter.com or ask g afk
	API_SECRET = 'api secret'
	NYT_KEY = 'nyt key'
	SENTIGEM_KEY = 'sgm key'" >> config.py

* ``mysql -p`` (or ``sudo mysql -p``)
	- ``{{ type DB_PASSWORD }}``
	- ``CREATE DATABASE {{ DB_NAME }};``
	- ``USE  {{ DB_NAME }};``
	- ``SOURCE schema.sql;``
	- ``CTRL C`` (leave MySQL)
* ``sudo pip install -r requirements.txt``
	- ``{{ type admin password }}``
        - if there's an error, ensure you have ``scipy`` `requirements <http://www.scipy.org/install.html>`_ satisfied
* ``python``
        - ``import nltk``
        - ``nltk.download('all')`` (may take a while, but all data is downloaded to ``~/``, so you can purge it later)
        - ``CTRL D`` (leave Python)
* ``python app.py``
        - if an error appears about ``winreg`` : remove the line ``MovedModule("winreg", "_winreg"),`` from ``/usr/lib/python2.7/dist-packages/scipy/lib/six.py``
* open ``localhost:5000`` in your web browser


pending
-------
#. cache scored result
#. cache full NYT articles
#. continued development of experimental ui
        * full article ui
        * highlighted-sentences/hover/tweet ui
        * trending queries ui
        * user history ui


pending (after PURE)
----------------------
#. development of external api
#. queries table -> redis cache
#. "show more" on results ui queries more than 10 articles
#. "confidence" included in api response (a function of number of tweets)

---------

Ismini Lourentzou, Lisa Huang, Graham Dyer -- ``{lourent2, xhuang62, gdyer2}@illinois.edu`` -- University of Illinois, Urbana-Champaign
