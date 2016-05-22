CC=gcc
INC=-isystem
LOPTS=-pthread
EXEC=fetcher_test queue_test 

all: $(EXEC)

fetcher_test: fetcher_test.c fetcher.o queue.o
	$(CC) $(shell pkg-config --cflags --libs libmongoc-1.0) $(INC) $(LOPTS) -ggdb $^ -o $@ -lcurl 

fetcher.o: fetcher.c fetcher.h queue.o
	$(CC) $(shell pkg-config --cflags --libs libmongoc-1.0) $(INC) $(LOPTS) -lcurl -ggdb -c $<

queue_test: queue_test.c queue.o
	$(CC) $(INC) $(LOPTS) -ggdb $^ -o $@

queue.o: queue.c queue.h
	$(CC) $(INC) $(LOPTS) -ggdb -c $<

clean:
	rm *.o $(EXEC)
