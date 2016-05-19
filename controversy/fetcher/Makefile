CC=gcc
INC=-I.
LOPTS=-pthread
EXEC=fetcher_test queue_test 

all: $(EXEC)

fetcher_test: fetcher_test.c fetcher.o queue.o
	$(CC) $(INC) $(LOPTS) -std=c99 -ggdb $^ -o $@ -lcurl

fetcher.o: fetcher.c fetcher.h queue.o
	$(CC) $(INC) $(LOPTS) -std=c99 -ggdb -c $<

queue_test: queue_test.c queue.o
	$(CC) $(INC) $(LOPTS) -std=c99 -ggdb $^ -o $@

queue.o: queue.c queue.h
	$(CC) $(INC) $(LOPTS) -std=c99 -ggdb -c $<

clean:
	rm *.o $(EXEC)
