.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots

Controversy
~~~~~~~~~~~

Joint Mining of news text and social media to discover controversial points in news.

`A live instance`_. It appears controversy|...|nois.edu is having some cross-origin problems |---| working on a resolution a.o. June 29th. In the meantime, please just use the IP.

Running for development
-----------------------

* ``cd server``
* ``mv sample-config.py config.py``, and change credentials
* create MySQL db "controversy" with ``source schema.sql``
* satisfy ``scipy`` `dependencies`_
* ``pip install -r requirements.txt``
* install package ``redis-server`` or ``redis``, depending on your system
* ``python``
        - ``import nltk``
        - ``nltk.download('all')``
* ``python app.py``


Pending
--------

#. ui problems with Firefox on results page
#. cross-origin nonsense referenced above
#. linguistic features added to score
#. stats with matplotlib
        - average global sentiment of tweets vs time
        - average controversy score for a keyword vs time (this is the timeline feature spoken about in beginning of semester)
        - api calls vs time
        - trending queries
#. more than tweets using NYT `community API`_
#. "rank more" on results ui queries more than 10 articles without repeats
#. development of external api
#. "confidence" included in api response, a function of number of tweets


-----

.. image:: http://www.life.illinois.edu/newmark/_Media/uclogo_1867_horz_bold.gif

``|contributors|``: Ismini Lourentzou, Abhishek Sharma, Graham Dyer, ChengXiang Zhai |---| ``{lourent2, sharma51, gdyer2, czhai}@illinois.edu`` |---| University of Illinois, Urbana-Champaign

.. _a live instance: http://192.155.89.114/
.. _dependencies: http://www.scipy.org/install.html
.. _community API: http://developer.nytimes.com/docs/community_api/The_Community_API_v3/
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
