.. |---| unicode:: U+2014 .. em dash
        :trim:
.. |--| unicode:: U+2013 .. en dash
.. |->| unicode:: U+2192 .. to
.. |=>| unicode:: U+27FA .. implies
.. |...| unicode:: U+2026 .. ldots

Controversy
~~~~~~~~~~~

Joint Mining of News Text and Social Media to Discover Controversial Points in News


Running for development
-----------------------
* ``cd server``
* ``mv sample-config.py config.py``, and change credentials
* create MySQL db "controversy" with ``source schema.sql``
* satisfy ``scipy`` `dependencies`_
* ``pip install -r requirements.txt``
* install package ``redis-server`` or ``redis``
* ``python``
        - ``import nltk``
        - ``nltk.download('all')``
* ``python app.py``


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
#. web ui Firefox, Safari support

---------

Ismini Lourentzou, Lisa Huang, Graham Dyer |---| ``{lourent2, xhuang62, gdyer2}@illinois.edu`` |---| University of Illinois, Urbana-Champaign

.. _Live: http://192.155.89.114/
.. _dependencies: http://www.scipy.org/install.html
