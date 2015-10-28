.. |---| unicode:: U+2014 .. em dash

API specification
~~~~~~~~~~~~~~~~~

You must be logged in to query any of these endpoints.

errors
------

``UsageError``
        ``error`` will be ``1``, ``message`` will have an error message, ``400`` status code
other error
        same, except with a ``200``. e.g.: no articles exist for the queryterm

article rank
------------

**GET** ``/api?q=hippo``

.. include:: documents/hippo.js
	:code: javascript
	:number-lines:

    
Where ``["result"][i]["score"]`` is the entropy score, the sum of the entropies of each sentence for each lingustic feature and sentiment.


user search-history
-------------------

**GET** ``/api/user-history``. It's only possible to query the currently-signed-in user's history, so no arguments.

.. include:: documents/history.js
	:code: javascript
	:number-lines:


trends
------

**GET** ``/api/trend``

.. include:: documents/trend.js
	:code: javascript
	:number-lines:


Where ``['result']['trending']`` is a key-value pair list where the key is the query and the value is the amount of search traffic towards that query. ``['result']['top-5']`` is a ranked list of the most popular queries. ``top-5`` will always be a (non-proper) subset of trending.

``/api/trend/<k>``. Where ``<k>`` is an element of ``/api/trend``'s ``trending`` list (a keyword that's been searched for before).

.. include:: documents/trend.js
	:code: javascript
	:number-lines:
	
**GET** ``/api/trend/<k>.png`` will generate a trendline (if there's enough data) of the controversy of a keyword versus time. Here's a *fabricated* example:

.. image:: documents/fake-trend.png

If you don't want a normalized plot, do ``<k>.png?nonorm``
