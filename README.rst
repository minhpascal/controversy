Controversy
~~~~~~~~~~~

Joint Mining of News Text and Social Media to Discover Controversial Points in News

Running for development
-----------------------
* ``cd server``
    * ``mv sample-config.py config.py``, and change credentials
    * ``mysql -p`` (or ``sudo mysql -p``)
      - ``{{ type DB_PASSWORD }}``
      - ``CREATE DATABASE {{ DB_NAME }};``
      - ``USE  {{ DB_NAME }};``
      - ``SOURCE schema.sql;``
      - ``CTRL C`` (leave MySQL)
    * ensure you have ``scipy`` `dependencies <http://www.scipy.org/install.html>`_ satisfied
    * ``sudo pip install -r requirements.txt``
    * ``apt-get install redis-server``, ``brew install redis`` or  `non-brew-OSX <http://jasdeep.ca/2012/05/installing-redis-on-mac-os-x/>`_
    * ``redis-server``
    * ``python``
        - ``import nltk``
        - ``nltk.download('all')`` (may take a while, but all data is downloaded to ``~/``, so you can purge it later)
        - ``CTRL D`` (leave Python)
    * ``python app.py``
        - if an error appears about ``winreg`` : remove the line ``MovedModule("winreg", "_winreg"),`` from ``/usr/lib/python2.7/dist-packages/scipy/lib/six.py``
    * open ``localhost:5000`` in your web browser


Pending
--------

#. StanfordNLP sentiment
#. stats for nerds with nvd3
    - average global sentiment of tweets vs time
    - average controversy score for a keyword vs time (this is the timeline feature spoken about in beginning of semester)
    - api calls vs time
    - trending queries
#. cache full NYT articles (with SQL)
#. "show more" on results ui queries more than 10 articles without repeats
#. "confidence" included in api response (a function of number of tweets)
#. when should cached content should be considered too old? intelligent purge system based on frequency of keyword in queries
#. use more than sentiment
#. development of external api
#. deployment
#. web ui Firefox, Safari support

---------

Ismini Lourentzou, Lisa Huang, Graham Dyer -- ``{lourent2, xhuang62, gdyer2}@illinois.edu`` -- University of Illinois, Urbana-Champaign

