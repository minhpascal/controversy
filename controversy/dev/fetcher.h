/* multithreaded article fetcher */
#ifndef FETCHER_H 
#define FETCHER_H 
#include "queue.h"

Queue *tasks;
void Fetcher_init(char **sources);

#endif
