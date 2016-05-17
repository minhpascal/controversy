/* a thread-safe queue implementation for
   article/comment fetcher */
#ifndef QUEUE_H
#define QUEUE_H

#include <pthread.h>

#define true 1
#define false 0
#define bool int

typedef struct QueueNode {
	struct QueueNode *next;
	void *data;
} QueueNode;

typedef struct {
	int size;
	QueueNode *head, *tail;
	pthread_cond_t not_empty;
	pthread_mutex_t lock;
	bool cancel;
} Queue;

Queue *Queue_init();
void Queue_free(Queue *q);

// add element to queue; won't block
void Queue_push(Queue *q, void *data);

// removes node; will block until q->size > 0
void *Queue_pull(Queue *q);

#endif
