#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <curl/curl.h>
#include "queue.h"
#include "fetcher.h"

#define THREAD_MAX 8
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

int n_fetches, n_todo;
pthread_mutex_t n_fetches_lock = PTHREAD_MUTEX_INITIALIZER;

void *perform(void *arg) {
	while (1) {
		pthread_mutex_lock(&n_fetches_lock);
		int end = (n_fetches == n_todo);
		pthread_mutex_unlock(&n_fetches_lock);

		if (end) {
			tasks->cancel = 1;
			break;
		}

		char *url = (char *)Queue_pull(tasks);
		if (!url) {
			tasks->cancel = 1;
			break;
		}

		pthread_mutex_lock(&n_fetches_lock);
		n_fetches++;
		pthread_mutex_unlock(&n_fetches_lock);

		CURL *curl;
		CURLcode res;

		curl = curl_easy_init();
		if (curl) {
			curl_easy_setopt(curl, CURLOPT_URL, url);
			curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

			res = curl_easy_perform(curl);
			if (res != CURLE_OK) {
				fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
			}

			curl_easy_cleanup(curl);
		}
	}

	return 0;
}

void Fetcher_init(char **sources) {
	tasks = Queue_init();
	while (sources) {
		Queue_push(tasks, *sources);
		sources++;
	}

	n_todo = tasks->size;
	int n_threads = MIN(n_todo, THREAD_MAX);
	pthread_t pids[n_threads];
	memset(&pids, 0, sizeof(pthread_t) * n_threads);

	for (int i = 0; i < n_threads; i++) {
		pthread_create(&pids[i], NULL, perform, NULL);
	}
	for (int i = 0; i < n_threads; i++) {
		pthread_join(pids[i], NULL);
	}
}
