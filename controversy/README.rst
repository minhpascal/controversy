.. |---| unicode:: U+2014 .. em dash

API spec
~~~~~~~~

You must be logged in to query any of these endpoints.

errors
------

``UsageError``
        ``error`` will be ``1``, ``message`` will have an error message, ``400`` status code
other error
        same, except with a ``200``. e.g.: no articles exist for the queryterm

article rank
------------

``/api?q=hippo``::


    {
	     'result': [
		    {
			'xlarge': 'http://www.nytimes.com/images/2015/03/31/world/31IRAQ/31IRAQ-articleLarge.jpg',
			'title': "Islamic State's Grip on City Appears Firmer Than Iraqis Acknowledge",
			'url': 'http://www.nytimes.com/2015/03/31/world/middleeast/un-leader-warns-iraq-not-to-mistreat-civilians-after-liberation-from-isis.html',
			'full': '<the full article>'
			'abstract': '<the article\'s abstract',
			'author': 'By ROD NORDLAND',
			'source': 'The New York Times',
			'score': 0.0,
			'sentences': [
				{
					'tweets': [
						{
								'sentiment': 4,
								'is_negative': 0,
								'is_positive': 1,
								'author': 'Minas',
								'tweet': 'It is a great day!',
								'pimg': 'http://i.dailymail.co.uk/i/pix/2009/08/24/article-1208479-0627718E000005DC-357_634x378.jpg',
								'followers': 100000,
								'clean_tweet': 'It is a great day!'
						}
					],
					'text': 'Great results today!',
                                        'entropy': 1.52121243,
					'ratio': 0.31415

				}
			],
			'published': '2015-03-31'
		},
	
	     ...],
	     'error' : 0
    }

Right now: where ``["result"][i]["score"]`` is the entropy score.

Intention: where ``["result"][i]["score"]`` is the entropy score, ``["result"][i]["ratio_score"]`` is the ratio score, and ``["result"][i]["visual_score"]`` is a combination of the two. Right now, only the entropy score is used for presentation purposes.


user search-history
-------------------

``/api/user-history``. It's only possible to query the currently-signed-in user's history, so no arguments.::


        {
                "error": 0, 
		"result" : {
                	"queries": [
                        	{
                                	"Performed": "2015-04-13 09:13:54", 
                                	"Term": "alex honnold"
                        	},
                	...] 
        	}
	}


trends
------

``/api/trend``::

	{
		"error": 0,
		"result": {
			"top-5": {
				"obama",
				"republican",
				"democratic primary",
				"mitt romney",
				"chris christie"
			},
			"trending": {
				"obama": 19.23
				"republican": 16.66,
				"democratic primary": 15.314159265358,
				"mitt romney": 14.2321,
				"chris christie": 4.95,
				"global warming": 4.05
				...
			}
		}
	}


Where ``['result']['trending']`` is a key-value pair list where the key is the query and the value is the amount of search traffic towards that query. ``['result']['top-5']`` is a ranked list of the most popular queries. top-5 will always be a non-proper subset of trending.

``/api/trend/<k>``. Where ``<k>`` is an element of ``/api/trend``'s ``trending`` list (a keyword that's been searched for before).::

	{
		"error": 0,
		"result": {
			"EntropyScore": 517.303,
			"RatioScore": 0.423695,
			"Performed": 2015-07-12
		},
		...
	}

``/api/trend/<k>.png`` will generate a trendline (if there's enough data) of the controversy of a keyword versus time. Here's `a fabricated example`_.

.. _a fabricated example: ../documents/fake-trend.png
