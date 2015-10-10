.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots

Controversy
~~~~~~~~~~~

Joint mining of news text and social media to discover controversial points in news.

.. image:: http://ocha.2pitau.org/img/biography/uiuc.gif
	:target: http://cs.illinois.edu

+---------------------------------------+-------------------------------+-------------------------------------------------------------------+
| Live demo                             | Publications                  | Authors                                                           |
+=======================================+===============================+===================================================================+
| `controversy.2pitau.org`_             | `IEEE Big Data 2015`_         | Ismini Lourentzou, Graham Dyer, Abhishek Sharma, ChengXiang Zhai  |
+---------------------------------------+-------------------------------+-------------------------------------------------------------------+
| `controversy.web.engr.illinois.edu`_  | `UIUC PURE Conference 2015`_  | Graham Dyer (mentee), Ismini Lourentzou (mentor)                  |
+---------------------------------------+-------------------------------+-------------------------------------------------------------------+
|                                       | (full paper in progress)      | ?                                                                 |
+---------------------------------------+-------------------------------+-------------------------------------------------------------------+


Pending
--------

We're currently preparing this server for a demo during **IEEE Big Data 2015 on October 29th**.

Demo todo
=========

* slight problems with Firefox on results page
* Safari problem on Tweets page
* transition when hovering over tweets
* show user their graphs 
* most controversial keywords on search page (not just trending)
* average same-day points in matplotlib
* normalize the graph between 0 and 1 (not comparable yet)
* more than NYTimes, Reuters, and AP. CNN is next
* tokenizer needs to remove acronyms


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



.. _IEEE Big Data 2015: http://ocha.2pitau.org/pdf/big-data-2015.pdf
.. _UIUC PURE Conference 2015: http://ocha.2pitau.org/pdf/pure.pdf
.. _controversy.2pitau.org: http://controversy.2pitau.org
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
.. _API spec: controversy/README.rst
.. _dependencies: http://www.scipy.org/install.html
