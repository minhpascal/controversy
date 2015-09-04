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

Method improvements
===================

A few approaches |...|

#. Use the NYT `community API`_ primarily (perhaps interspersed with tweets) and switch to a better IR model (than BM25). Benefits: keep pieces of the structure currenty implemented. Caveats: none, just that it's imperative BM25 is a *baseline* compared to a newer model. Looking for candidates. I'm reading Svore, Burges: `A Machine Learning Approach for Improved BM25 Retrieval`_. If a better model is implemented, use a service like Mechanical Turk and build a highlighting platform through which turkers could review *full* articles and make a determination on each sentence's controversy (as a boolean). The new dataset would allow us to check our |---| equally new |---| model.
#. Use neural networks to organize collections of social content and their relationships to sentences (see Irsoy, Cardie: `Opinion Mining with Deep Recurrent Neural Networks`_). Benefits: potentially more accuracy. Caveats: longer implementation, added complexity.

demo todo
=========

* slight problems with Firefox on results page
* follow user keywords to find trends
* compare controversy keyboard plots
* (confidence included in api response, a function of number of social content used / article)

Now, sentiment entropy is what's used to rank articles in the UI. It also filters sentences, which are then scored by ratio and other entropy scores. How should the UI reflect the different scoring approaches?


-----

.. image:: http://web.engr.illinois.edu/~gdyer2/img/biography/uiuc.jpg

Ismini Lourentzou, Abhishek Sharma, Graham Dyer, ChengXiang Zhai |---| ``{lourent2, sharma51, gdyer2, czhai}@illinois.edu`` |---| University of Illinois, Urbana-Champaign (``|contributors|``)

.. _a live instance: http://controversy.2pitau.org
.. _dependencies: http://www.scipy.org/install.html
.. _community API: http://developer.nytimes.com/docs/community_api/The_Community_API_v3/
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
.. _Opinion Mining with Deep Recurrent Neural Networks: http://www.cs.cornell.edu/~oirsoy/files/emnlp14drnt.pdf
.. _A Machine Learning Approach for Improved BM25 Retrieval`: http://research.microsoft.com/pubs/101323/LearningBM25MSRTechReport.pdf
