OBJ =  o/binCust.o
CFLAGS = -g #-Wall

TARGET = o/rmIslands.o

$(TARGET) : o/binCust.o rmIslands.cpp
	g++ $(CFLAGS) -o $(TARGET) o/binCust.o rmIslands.cpp

o/binCust.o : bin_custom.h bin_custom.cpp
	mkdir -p o
	g++ $(CFLAGS) -c -o o/binCust.o bin_custom.cpp

.PHONY : clean

clean :
	rm o/*