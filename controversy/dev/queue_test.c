#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "queue.h"

char *v = NULL;
void *push(void *arg) {
	v = strdup("bye!");
	Queue_push((Queue *)arg, v);
	return NULL;
}


int main(void) {
	Queue *q = Queue_init();
	char *s = "hello";
	Queue_push(q, s);
	assert(strcmp(s, (char *)Queue_pull(q)) == 0);

	char *t = "hello!";
	char *u = "again...";
	Queue_push(q, strdup(t));
	Queue_push(q, strdup(t));

	pthread_t p;
	pthread_create(&p, NULL, push, (void *)q);

	char *x = (char *)Queue_pull(q);
	assert(strcmp(t, x) == 0);
	free(x);
	char *y = (char *)Queue_pull(q);
	assert(strcmp(t, y) == 0);
	free(y);
	assert(strcmp(v, (char *)Queue_pull(q)) == 0);

	pthread_join(p, NULL);
	free(v);

	Queue_push(q, u);
	assert(strcmp(u, (char *)Queue_pull(q)) == 0);

	Queue_free(q);


	return 0;
}
