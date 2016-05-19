#include <stdlib.h>
#include <stdio.h>
#include "queue.h"

Queue *Queue_init() {
	Queue *q = malloc(sizeof(Queue));
	q->size = 0;
	q->head = NULL;
	q->tail = NULL;
	q->cancel = 0;
	pthread_mutex_init(&q->lock, NULL);
	pthread_cond_init(&q->not_empty, NULL);
	return q;
}

void Queue_free(Queue *q) {
	pthread_mutex_destroy(&q->lock);
	pthread_cond_destroy(&q->not_empty);
	QueueNode *i = q->head;
	while (i) {
		fprintf(stderr, "here!\n");
		free(i);
		i = i->next;
	}

	free(q);
}

void Queue_push(Queue *q, void *data) {
	pthread_mutex_lock(&q->lock);

	q->size++;

	QueueNode *node = malloc(sizeof(QueueNode));
	node->data = data;
	node->next = NULL;
	if (!q->head) {
		q->head = q->tail = node;
	} else {
		q->tail->next = node;
		q->tail = node;
	}


	pthread_cond_signal(&q->not_empty);
	pthread_mutex_unlock(&q->lock);
}

void *Queue_pull(Queue *q) {
	pthread_mutex_lock(&q->lock);
	while (!q->cancel && q->size == 0) {
		pthread_cond_wait(&q->not_empty, &q->lock);
	}

	if (q->cancel) {
		pthread_mutex_unlock(&q->lock);
		return NULL;
	}

	q->size--;

	QueueNode *old_head = q->head;
	if (q->head == q->tail) {
		q->head = q->tail = NULL;
	} else {
		q->head = q->head->next;
	}

	void *res = old_head->data;
	free(old_head);

	pthread_mutex_unlock(&q->lock);
	return res;
}
