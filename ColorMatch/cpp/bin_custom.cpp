#include "bin_custom.h"

#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <fstream>

using namespace std;




multiArray::multiArray(){
	dims = 0;
}


multiArray::multiArray(uint32_t _dims, uint32_t* _lens, uint8_t defVal){
	dims = _dims;
	lens = new uint32_t [dims];
	for(int i=0; i<dims; i++){
		lens[i] = _lens[i];

	}
}


uint readToInt(ifstream &iFile, int length){
	// cout << iFile.tellg() << ' ' << length;

	char * buffer = new char[length];

	iFile.read(buffer, length);

	uint outVal = 0;
	for(int i = 0; i < length; i++){
		outVal = (outVal << 8) + (int)buffer[i];
		// cout << i << ' ' << (int)buffer[i] << ' ' << outVal << '\n';
	}

	delete[] buffer;

	// iFile.seekg((size_t)iFile.tellg());
	return(outVal);
}

multiArray::multiArray(string iFileName){
	//Open iFile
	ifstream iFile;
	iFile.open(iFileName, ifstream::binary);

	//Read header, get sizes
	dims = (uint32_t)readToInt(iFile, 4);
	cout << "Read dims: " << dims << '\n';

	lens = new uint32_t[dims];

	for(int i=0; i<dims; i++){
		lens[i] = (uint32_t)readToInt(iFile, 4);
		
		cout << "Read lens["<<i<<"]: " << lens[i] << '\n';
	}

	//Get total number of values in grid and multipliers for each dimension to get index from grid pos
	valCount = 1;
	dimMults = new uint[dims];
	for(int i=0; i<dims; i++){
		valCount *= lens[i];
		dimMults[i] = 1;
		for(int j=0; j < i; j++){
			dimMults[j] *= lens[i];
		}
	}

	// cout << "valCount: " << valCount << '\n';

	// for(int i=0; i<dims; i++){
	// 	cout << "dimMult " << i <<" is " << dimMults[i] << '\n';
	// }

	//Fill in array from text
	vals = new uint8_t[valCount];
	for(int i=0; i<valCount; i++){
		vals[i] = (uint8_t)readToInt(iFile, 1);
	}
}

multiArray::~multiArray(){
	delete[] lens;
	delete[] dimMults;
	delete[] vals;
}


uint8_t multiArray::get(int* pos){
	uint index = 0;
	for(int i=0; i<dims; i++){
		index += dimMults[i]*pos[i];
	}
	return(vals[index]);
}


void multiArray::set( int* pos, uint8_t inVal){
	uint index = 0;
	for(int i=0; i<dims; i++){
		index += dimMults[i]*pos[i];
	}

	vals[index] = inVal;
}


void writeBytes(ofstream &oFile, int inVal, int bytes){
	uint64_t foo = (uint64_t)inVal;
	uint64_t bar = (foo << 8*(bytes));

	char* buffer = new char[bytes];
	for(int i=0; i<bytes; i++){
		bar = (bar >> 8);
		buffer[i] = *(char*)&bar;
	}
	oFile.write(buffer, bytes);

	// char outChar = ((char)bar);
	// char* buffer = (char*)&bar;
	// oFile.write(buffer, bytes);
	// for(int i=0; i<bytes; i++){
	// 	char outChar = ((char)bar);
	// 	char* buffer = &outChar;
	// 	// cout << "B: " << bar << " P: " << (int*)buffer << " Bytes: " << bytes << '\n';
	// 	oFile.write(buffer, 2);
	// 	bar = (8 >> bar);
	// }
}

void multiArray::save(string oFileName){
	ofstream oFile;
	oFile.open(oFileName, ofstream::binary);

	//write number of dims
	writeBytes(oFile, dims, 4);

	//Write array of lens
	for(int i=0; i<dims; i++){
		writeBytes(oFile, lens[i], 4);
	}

	//Write value
	for(int i=0; i<valCount; i++){
		writeBytes(oFile, vals[i], 1);
	}

}