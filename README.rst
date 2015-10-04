.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots

Controversy
~~~~~~~~~~~

Joint mining of news text and social media to discover controversial points in news.

.. image:: http://ocha.2pitau.org/img/biography/uiuc.jpg

Ismini Lourentzou, Graham Dyer, Abhishek Sharma, ChengXiang Zhai |---| ``{lourent2, gdyer2, sharma51, czhai}@illinois.edu`` |---| University of Illinois, Urbana-Champaign

----

Live \@ `controversy.2pitau.org`_ or `controversy.web.engr.illinois.edu`_.

Publications: full paper in progress, `IEEE Big Data 2015`_, `PURE Conference 2015`_.


Pending
--------

We're currently preparing this server for a demo during **IEEE Big Data 2015 on October 29th**.

We're also working on a full paper, which will add variables to our scoring function and improve BM25's accuracy for mapping article sentences to tweets.


Demo todo
=========

* slight problems with Firefox on results page
* re-run analysis daily for every keyword entered. show this to the user
* most controversial keywords on search page (not just trending)
* potentially most controversial articles too, independent of keyword
* (compare controversy keyboard plots)

Now, sentiment entropy is what's used to rank articles in the UI. It also filters sentences, which are then scored by ratio and other entropy scores. How should the UI reflect the different scoring approaches?


Running for development
-----------------------

If you'd like to reproduce our results, we encourage you to use the demo or look at our `API spec`_ for raw results. Alternatively, you can clone this repository and run the server yourself.

Please use Python 2.7.x

#. ``$ cd controversy``
#. ``$ mv sample-config.py config.py``, and change credentials
#. create MySQL DB called "controversy" with ``source schema.sql``
#. satisfy SciPy `dependencies`_
#. ``$ pip install -r requirements.txt``
#. install redis and run ``redis-server`` and close
#. ``$ python``
        - ``>>> import nltk``
        - ``>>> nltk.download('all')``
#. ``$ python app.py``



.. _IEEE Big Data 2015: #
.. _PURE Conference 2015: http://ocha.2pitau.org/pdf/pure.pdf
.. _API spec: controversy/README.rst
.. _controversy.2pitau.org: http://controversy.2pitau.org
.. _dependencies: http://www.scipy.org/install.html
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
