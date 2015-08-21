.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots

Controversy
~~~~~~~~~~~

Joint mining of news text and social media to discover controversial points in news.

`A live instance`_. `controversy.web.engr.illinois.edu`_ will redirect there.

Running for development
-----------------------

#. ``$ cd controversy``
#. ``$ mv sample-config.py config.py``, and change credentials
#. create MySQL db "controversy" with ``source schema.sql``
#. satisfy ``scipy`` `dependencies`_
#. ``$ pip install -r requirements.txt``
#. install package ``redis-server`` or ``redis``, depending on your system
#. ``$ python``
        - ``>>> import nltk``
        - ``>>> nltk.download('all')``
#. ``$ python app.py``


Pending
--------

* slight problems with Firefox on results page
* "rank more" on results ui queries more than 10 articles without repeats
* (confidence included in api response, a function of number of tweets)
* (more than tweets using NYT `community API`_)


-----

.. image:: http://web.engr.illinois.edu/~gdyer2/img/biography/uiuc.jpg

Ismini Lourentzou, Abhishek Sharma, Graham Dyer, ChengXiang Zhai |---| ``{lourent2, sharma51, gdyer2, czhai}@illinois.edu`` |---| University of Illinois, Urbana-Champaign (``|contributors|``)

.. _a live instance: controversy.2pitau.org
.. _dependencies: http://www.scipy.org/install.html
.. _community API: http://developer.nytimes.com/docs/community_api/The_Community_API_v3/
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
