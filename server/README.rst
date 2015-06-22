Internal RESTful API docs
~~~~~~~~~~~~~~~~~~~~~~~~~

errors
------

usage error
        ``error`` will be ``1``, ``message`` will have an error message, ``400`` status code
non-usage error
        same as above, except with a ``200``. ex: no articles exist for the queryterm

keyword rank
------------

query
        ``/api?q=hippo`` or with ``&test=1`` for manufactured sentiment data

response:: 

    {
	     'articles': [
		    {
			'xlarge': 'http://www.nytimes.com/images/2015/03/31/world/31IRAQ/31IRAQ-articleLarge.jpg',
			'title': "Islamic State's Grip on City Appears Firmer Than Iraqis Acknowledge",
			'url': 'http://www.nytimes.com/2015/03/31/world/middleeast/un-leader-warns-iraq-not-to-mistreat-civilians-after-liberation-from-isis.html',
			'full': 'We had some exciting results today, involving hippos and Rod Nordland, our senior hippo...'
			'abstract': 'Great results today!',
			'author': 'By ROD NORDLAND',
			'source': 'The New York Times',
			'score': 0.0,
			'sentences': [
				{
					'tweets': [
						{
								'sentiment': 4,
								'author': 'Minas',
								'tweet': 'It is a great day!',
								'pimg': 'http://illinois.edu/assets/img/navigation/submenu_about.jpg',
								'followers': 100000,
								'clean_tweet': 'It is a great day!'
						}
					],
					'text': 'Great results today!',
                                        'entropy': 1.52121243,

				}
			],
			'published': '2015-03-31'
		},
	
	     ...]
	     'error' : 0
    }


``["articles"][n]["xlarge"]``
        cover image of article
``["articles"][n]["abstract"]``
        either the abstract or first paragraph, in that order of preference. Recent commit removes html tags
``["articles"][n]["abstract"]``
        full text of the article
``["articles"][n]["sentences"][m]["tweets"][p]["clean"]``
        tweet without pound signs, @authors, urls. used to query sentiment
``["articles"][n]["sentences"][m]["tweets"][p]["followers"]``
        followers of author, not of the tweet
``["articles"][n]["sentences"][m]["tweets"][p]["pimg"]``
        profile picture of author


user search history
-------------------

query
        ``/api/user-history``. It's only possible to query the currently-signed-in user's history, so no arguments.

response::

        {
                "error": 0, 
                "queries": [
                        {
                                "Performed": "2015-04-13 09:13:54", 
                                "Term": "alex honnold"
                        },
                ...] 
        }

