CC=gcc
INC=-I.
LOPTS=-pthread
EXEC=fetcher_test queue_test 

all: $(EXEC)

fetcher_test: fetcher_test.c fetcher.o queue.o
	$(CC) $(INC) $(LOPTS) -ggdb -lcurl $^ -o $@

fetcher.o: fetcher.c fetcher.h queue.o
	$(CC) $(INC) $(LOPTS) -ggdb -c $<

queue_test: queue_test.c queue.o
	$(CC) $(INC) $(LOPTS) -ggdb $^ -o $@

queue.o: queue.c queue.h
	$(CC) $(INC) $(LOPTS) -ggdb -c $<

clean:
	rm *.o $(EXEC)
