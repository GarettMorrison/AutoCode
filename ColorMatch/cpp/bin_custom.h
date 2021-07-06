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
	multiArray(string iFileName);
	~multiArray();

	uint8_t get(int* pos);
	void set(int* pos, uint8_t inVal);
	void save(string oFileName);
private:
	uint32_t dims = 0; //How many dimensions to address
	uint32_t* lens;	//Array of lengths for each dimension
	uint8_t* vals;	//Array of values that are referenced

	uint valCount;	//Total number of values
	uint* dimMults;	//Factor to multiply each coord by to find index in vals

};

#endif