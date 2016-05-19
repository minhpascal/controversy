/* multithreaded article fetcher */
#ifndef FETCHER_H 
#define FETCHER_H 
#include "queue.h"

// HTML of URLs in ``sources`` to ``key``
void Fetcher_fetch(char **sources);

#endif
