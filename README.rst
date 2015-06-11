.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots

Controversy
~~~~~~~~~~~

Joint Mining of news text and social media to discover controversial points in news. `Learn more`_

`A live instance`_.

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


.. image:: http://www.life.illinois.edu/newmark/_Media/uclogo_1867_horz_bold.gif

Ismini Lourentzou, Lisa Huang, Graham Dyer |---| ``{lourent2, xhuang62, gdyer2}@illinois.edu`` |---| University of Illinois, Urbana-Champaign

.. _a live instance: http://192.155.89.114/
.. _dependencies: http://www.scipy.org/install.html
.. _Learn more: https://github.com/gdyer/controversy/blob/master/documents/gdyer2_poster.pdf
