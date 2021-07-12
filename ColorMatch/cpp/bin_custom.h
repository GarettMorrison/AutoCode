#ifndef BIN_CUSTOM_H
#define BIN_CUSTOM_H

#include <string>
#include <iostream>

// typedef bitset<8> BYTE;

using namespace std;

class multiArray{
public:
	multiArray();
	multiArray(uint32_t _dims, uint32_t* _lens, uint8_t defVal = 0);
	multiArray(string iFileName, bool setDebug = false);
	~multiArray();

	uint8_t* getPtr(int*pos);
	uint8_t* getPtr(int p0=0, int p1=0, int p2=0, int p3=0, int p4=0, int p5=0, int p6=0, int p7=0, int p8=0, int p9=0);

	uint8_t get(int* pos);
	uint8_t get(int p0=0, int p1=0, int p2=0, int p3=0, int p4=0, int p5=0, int p6=0, int p7=0, int p8=0, int p9=0); //Kinda dumb ngl, but allows easier get() syntax
	
	void set(uint8_t inVal, int* pos);
	uint8_t set(uint8_t inVal, int p0=0, int p1=0, int p2=0, int p3=0, int p4=0, int p5=0, int p6=0, int p7=0, int p8=0, int p9=0); //Also dumb, but allows easier set() syntax
	
	void save(string oFileName);

	uint32_t dims = 0; //How many dimensions to address
	uint32_t* lens;	//Array of lengths for each dimension

	void debug(bool setDebug);

	bool debugMode = false;
	
private:
	uint8_t* vals;	//Array of values that are referenced
	uint valCount;	//Total number of values
	uint* dimMults;	//Factor to multiply each coord by to find index in vals
	int* posArr;		//Internal ref

};

#endif