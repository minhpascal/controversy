#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "queue.h"

int main(void) {
	Queue *q = Queue_init();
	char *s = "hello";
	Queue_push(q, s);
	assert(strcmp(s, (char *)Queue_pull(q)) == 0);

	Queue_free(q);


	return 0;
}
