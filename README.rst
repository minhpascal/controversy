.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots
.. |ui| image:: http://ocha.2pitau.org/img/biography/affiliation.jpg

Controversy
~~~~~~~~~~~~

Joint mining of news text and social media to discover controversial points in news.

+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+
| Live demo                             | Publication                   | People                                                                                |
+=======================================+===============================+=======================================================================================+
| `controversy.2pitau.org`_             | `IEEE Big Data 2015`_         | Ismini Lourentzou |ui|, Graham Dyer |ui|, Abhishek Sharma |ui|, ChengXiang Zhai |ui|  |
+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+
| `controversy.web.engr.illinois.edu`_  | `UIUC PURE Conference 2015`_  | Graham Dyer |ui| (mentee), Ismini Lourentzou |ui| (mentor)                            |
+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+
| ?                                     | (full paper in progress)      | ?                                                                                     |
+---------------------------------------+-------------------------------+---------------------------------------------------------------------------------------+

Pending
--------

We're currently preparing this server for a demo during **IEEE Big Data 2015 on October 29th**.

Scoring todo
============

1. Switch to conditional probability for linguistic features:
  
Recall :math:`p(X_sent = x_i) = \frac{P(x_i) \in C_i^'}{\sum_{i=1}^{z} f(x_i) \in C_i^'}` is equivalent to the number of comments (tweets) with sentiment :math:`x_i` divided by the total number of comments. Therefore, :math:`p(X_caps = x_i) = p(X_sent = x_i | C_i^' \in Caps) = \frac{p(X_sent = x_i \cap C_i^' \in Caps}{p(C_i^' \in Caps)` where :math:`Caps`` is the set of comments that have capitalized terms. This works similarly for the extreme lexicon.

Demo todo
=========

* appears to be a problem loading matplotlib graph for trends
* show user their graphs 
* average same-day points in matplotlib
* tokenizer needs to remove acronyms


Running for development
-----------------------

If you'd like to reproduce our results, we encourage you to use the demo or look at our `API spec`_ for raw ``json`` results. Alternatively, you can clone this repository and run the server yourself. We wrote `some instructions to help you`_.

------


.. image:: http://ocha.2pitau.org/img/biography/uiuc.gif
	:target: http://cs.illinois.edu

.. _IEEE Big Data 2015: http://ocha.2pitau.org/pdf/big-data-2015.pdf
.. _UIUC PURE Conference 2015: http://ocha.2pitau.org/pdf/pure.pdf
.. _controversy.2pitau.org: http://controversy.2pitau.org
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
.. _API spec: controversy/README.rst
.. _some instructions to help you: documents/development-help.rst
