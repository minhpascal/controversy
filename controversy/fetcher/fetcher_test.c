#include "fetcher.h"

int main(void) {
	// TODO
	char *urls[] = { "http://www.nytimes.com/2016/05/22/arts/television/roots-remade-for-a-new-era.html?hp&action=click&pgtype=Homepage&clickSource=image&module=photo-spot-region&region=top-news&WT.nav=top-news&_r=0", "http://www.nytimes.com/2016/05/18/us/politics/bernie-sanders-oregon-results.html?action=click&contentCollection=Television&module=Trending&version=Full&region=Marginalia&pgtype=article" };
	Fetcher_fetch(urls);
	return 0;
}
