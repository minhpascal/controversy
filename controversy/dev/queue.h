/* a thread-safe queue implementation for article/comment fetcher */
#ifndef QUEUE_H
#define QUEUE_H

#include <pthread.h>

typedef struct QueueNode {
	struct QueueNode *next;
	void *data;
} QueueNode;

typedef struct {
	int size;
	int cancel;
	QueueNode *head, *tail;
	pthread_cond_t not_empty;
	pthread_mutex_t lock;
} Queue;

Queue *Queue_init();

// frees q and its nodes but not their data
void Queue_free(Queue *q);

// add element to queue; won't block
void Queue_push(Queue *q, void *data);

// removes node; will block until q->size > 0
void *Queue_pull(Queue *q);

#endif
