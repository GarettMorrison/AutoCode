#include "bin_custom.h"

#include <stdlib.h>
#include <math.h>
#include <iostream>
#include <fstream>

using namespace std;



multiArray::multiArray(){
	int* posArr = new int[10];
	dims = 0;
}







multiArray::multiArray(uint32_t _dims, uint32_t* _lens, uint8_t defVal){
	posArr = new int[10];
	cout << "Making new multiArray\n";


	dims = _dims;
	lens = new uint32_t [dims];
	for(int i=0; i<dims; i++){
		lens[i] = _lens[i];
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

	//Fill in array from text
	vals = new uint8_t[valCount];
	for(int i=0; i<valCount; i++){
		vals[i] = defVal;
	}
}


multiArray::~multiArray(){
	delete[] lens;
	delete[] dimMults;
	delete[] vals;
	delete[] posArr;
}




// Get pointer to area of memory
// Reccomended to only pull at lowest dimension
uint8_t* multiArray::getPtr(int p0, int p1, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9){
	posArr[0] = p0;
	posArr[1] = p1;
	posArr[2] = p2;
	posArr[3] = p3;
	posArr[4] = p4;
	posArr[5] = p5;
	posArr[6] = p6;
	posArr[7] = p7;
	posArr[8] = p8;
	posArr[9] = p9;
	uint8_t* outVar = getPtr(posArr);
	return(outVar);
}

uint8_t* multiArray::getPtr(int* pos){
	uint index = 0;
	for(int i=0; i<dims; i++){
		index += dimMults[i]*pos[i];
	}
	return(&vals[index]);
}



//Get value at address
uint8_t multiArray::get(int p0, int p1, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9){
	posArr[0] = p0;
	posArr[1] = p1;
	posArr[2] = p2;
	posArr[3] = p3;
	posArr[4] = p4;
	posArr[5] = p5;
	posArr[6] = p6;
	posArr[7] = p7;
	posArr[8] = p8;
	posArr[9] = p9;
	return(get(posArr));
}

uint8_t multiArray::get(int* pos){
	uint index = 0;
	for(int i=0; i<dims; i++){
		index += dimMults[i]*pos[i];
	}
	return(vals[index]);
}



//Set value at point
uint8_t multiArray::set(uint8_t inVal, int p0, int p1, int p2, int p3, int p4, int p5, int p6, int p7, int p8, int p9){
	posArr[0] = p0;
	posArr[1] = p1;
	posArr[2] = p2;
	posArr[3] = p3;
	posArr[4] = p4;
	posArr[5] = p5;
	posArr[6] = p6;
	posArr[7] = p7;
	posArr[8] = p8;
	posArr[9] = p9;
	set(inVal, posArr);
}

void multiArray::set(uint8_t inVal, int* pos){
	uint index = 0;
	for(int i=0; i<dims; i++){
		index += dimMults[i]*pos[i];
	}

	vals[index] = inVal;
}

void multiArray::debug(bool setDebug){
	debugMode = setDebug;
}



//File manip
uint readToInt(ifstream &iFile, int length){
	char buff;
	uint outVal = 0;


	for(int i = 0; i < length; i++){
		iFile.read(&buff, 1);
		uint tempVal = 0;
		tempVal = (uint8_t)buff;

		outVal = outVal << 8;

		outVal += tempVal;
	}

	return(outVal);
}

multiArray::multiArray(string iFileName, bool setDebug){
	posArr = new int[10];
	//Set debug status
	debugMode = setDebug;


	if(debugMode){cout << "File reading: " << iFileName << '\n';}

	//Open iFile
	ifstream iFile;
	iFile.open(iFileName, ifstream::binary);
	iFile.seekg(0);

	//Read header, get sizes
	dims = readToInt(iFile, 4);

	if(debugMode){cout << "Read dims: " << dims << '\n';}

	lens = new uint32_t[dims];
	for(int i=0; i<dims; i++){
		lens[i] = (uint32_t)readToInt(iFile, 4);
		
		if(debugMode){printf("Read lens[%d]: %d\n", i, lens[i]);}
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

	// //Fill in array from text
	vals = new uint8_t[valCount];
	for(int i=0; i<valCount; i++){
		vals[i] = readToInt(iFile, 1);
	}
	// printf("\n");
	iFile.close();
}


void writeBytes(ofstream &oFile, int inVal, int bytes){
	unsigned long int foo = (uint64_t)inVal;
	uint8_t* bar = (uint8_t*)&foo;// (foo >> 8*(8-bytes));
	bar += bytes;
	// bar += 
	// char* buffer = new char[bytes];
	char buffer;

	for(int i=0; i<bytes; i++){
		bar -= 1;
		buffer = *bar;
		// printf("  Save byte %d read as %d as %i\n", i, (uint)*bar, (uint32_t)buffer);
		oFile.write(&buffer, 1);
	}
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
	oFile.close();
}