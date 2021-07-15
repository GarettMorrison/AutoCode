CC = g++ # Flag for implicit rules
CFLAGS = -g # Flag for implicit rules. Turn on debug info

all: o/rmIslands.o o/matchToPix.o o/splitLayers.o

# o/splitLayers.o : tmp/bin_custom.o splitLayers.cpp
# 	mkdir -p o
# 	$(CC) $(CFLAGS) -o o/splitLayers.o tmp/bin_custom.o splitLayers.cpp

o/rmIslands.o : tmp/bin_custom.o rmIslands.cpp
	mkdir -p o
	$(CC) $(CFLAGS) -o o/rmIslands.o tmp/bin_custom.o rmIslands.cpp

o/matchToPix.o : tmp/bin_custom.o matchToPix.cpp
	mkdir -p o
	$(CC) $(CFLAGS) -o o/matchToPix.o tmp/bin_custom.o matchToPix.cpp


tmp/bin_custom.o : bin_custom.h bin_custom.cpp
	mkdir -p tmp
	$(CC) $(CFLAGS) -c -o tmp/bin_custom.o bin_custom.cpp

.PHONY : clean

clean :
	rm -f o/*
	rm -f tmp/*