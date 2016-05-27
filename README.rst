.. |---| unicode:: U+2014 .. em dash
.. |->| unicode:: U+2192 .. to
.. |...| unicode:: U+2026 .. ldots
.. |ui| image:: controversy/static/img/affiliation.jpg

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

Pending
--------

1. prepare a pre-mturk method for downloading the training data dynamically (both annotated and not).
2. improving upon the method mentioned in our IEEE paper.

Running for development
-----------------------

If you'd like to reproduce our results, we encourage you to use the demo online or look at our `API spec`_ for raw ``json`` results. Alternatively, you can clone this repository and either call the scoring function or run the demo server yourself. We wrote `some instructions to help you`_.

------

.. image:: https://sxibolet.2pitau.org/_static/img/uiuc.gif
	:target: http://cs.illinois.edu

.. _IEEE Big Data 2015: https://sxibolet.2pitau.org/pdf/big-data-2015.pdf
.. _UIUC PURE Conference 2015: http://sxibolet.2pitau.org/pdf/pure.pdf
.. _controversy.2pitau.org: https://controversy.2pitau.org
.. _controversy.web.engr.illinois.edu: http://controversy.web.engr.illinois.edu
.. _API spec: https://docs.controversy.2pitau.org
.. _some instructions to help you: controversy/documents/development-help.rst
