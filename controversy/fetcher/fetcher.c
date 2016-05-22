#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <curl/curl.h>
#include <mongoc.h>
#include <bson.h>
#include "queue.h"
#include "fetcher.h"

#define THREAD_MAX 8
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

Queue *tasks;
int n_fetches, n_todo;
pthread_mutex_t n_fetches_lock = PTHREAD_MUTEX_INITIALIZER;


typedef struct page {
	char *string;
	size_t len;
} page_t;

size_t w_callback(void *ptr, size_t size, size_t nmemb, page_t *pg) {
	size_t pckt_size = size * nmemb,
	       nl = pg->len + pckt_size;
	pg->string = realloc(pg->string, nl + 1);
	memcpy(pg->string + pg->len, ptr, pckt_size);
	pg->len = nl;
	pg->string[nl] = '\0';

	return pckt_size;
}

// write ``page`` to db
void write_page(page_t *page, mongoc_client_pool_t *pool) {
	mongoc_client_t *client = mongoc_client_pool_pop(pool);
	mongoc_collection_t *collection = mongoc_client_get_collection(client, "controversy", "training_html");

	bson_t *doc = bson_new();
	bson_oid_t oid;
	bson_oid_init(&oid, NULL);

	BSON_APPEND_OID(doc, "_id", &oid);
	BSON_APPEND_UTF8(doc, "hello", "world");

	// TODO: write to articles collection
	// ts, keyword, article, 

	bson_error_t error;
	if (!mongoc_collection_insert(collection, MONGOC_INSERT_NONE, doc, NULL, &error)) {
	}

	bson_destroy(doc);
	mongoc_collection_destroy(collection);
	mongoc_client_pool_push(pool, client);
}

void *perform(void *arg) {
	mongoc_client_pool_t *pool = arg;

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
			page_t *page = malloc(sizeof(page));
			page->len = 0;
			// allocate enough space for NULL-char
			page->string = malloc(1);
			page->string[0] = '\0';

			// TODO: get twitter search result too!
			curl_easy_setopt(curl, CURLOPT_URL, url);
			curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);
			curl_easy_setopt(curl, CURLOPT_COOKIEFILE, "");
			curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, w_callback);
			curl_easy_setopt(curl, CURLOPT_WRITEDATA, page);

			res = curl_easy_perform(curl);
			if (res != CURLE_OK) {
				fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
				exit(EXIT_FAILURE);
			}

			if (page->len > 0) {
				write_page(page, pool);
			} else {
				fprintf(stderr, "(!) ===> page %s is NULL\n", url);
			}

			free(page->string);
			free(page);
			curl_easy_cleanup(curl);
		} else {
			exit(EXIT_FAILURE);
		}

		curl_easy_cleanup(curl);
	}

	return 0;
}

void Fetcher_fetch(char **sources) {
	tasks = Queue_init();

	while (*sources != NULL) {
		Queue_push(tasks, *sources++);
		sources++;
	}

	n_todo = tasks->size;
	int n_threads = MIN(n_todo, THREAD_MAX);
	pthread_t pids[n_threads];
	memset(&pids, 0, sizeof(pthread_t) * n_threads);

	mongoc_init();
	mongoc_uri_t *uri = mongoc_uri_new("mongodb://localhost/27017/");
	mongoc_client_pool_t *pool = mongoc_client_pool_new(uri);

	int i, j;
	for (i = 0; i < n_threads; i++) {
		pthread_create(&pids[i], NULL, perform, pool);
	}

	mongoc_uri_destroy(uri);

	for (i = 0; i < n_threads; i++) {
		pthread_join(pids[i], NULL);
	}

	mongoc_cleanup();
	curl_global_cleanup();
}
