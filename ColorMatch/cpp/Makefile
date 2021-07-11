OBJ =  o/binCust.o
CFLAGS = -g #-Wall

TARGET = o/rmIslands.o

$(TARGET) : tmp/binCust.o rmIslands.cpp
	mkdir -p o
	g++ $(CFLAGS) -o $(TARGET) tmp/binCust.o rmIslands.cpp

tmp/binCust.o : bin_custom.h bin_custom.cpp
	mkdir -p tmp
	g++ $(CFLAGS) -c -o tmp/binCust.o bin_custom.cpp

.PHONY : clean

clean :
	rm o/*
	rm tmp/*