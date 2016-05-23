/* multithreaded article fetcher */
#ifndef FETCHER_H 
#define FETCHER_H 
#include "queue.h"

// fetch HTML from ``sources[i]`` cooresponding to ``keyword``
void Fetcher_fetch(char **sources, char *keyword);

#endif
