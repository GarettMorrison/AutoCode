#include <iostream>
#include <fstream>
#include <iomanip>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "bin_custom.h"

using namespace std;

int iW;
int iH;


int compPix(uint8_t* val1, uint8_t* val2){
	int outDiff = 0;
	for(int i=0; i<3; i++){outDiff += abs(val1[i] - val2[i]);}
	return(outDiff);
}


int main(){
	multiArray pixIn("origPix.bin");	//Read original pix vals
	iW = pixIn.lens[0];
	iH = pixIn.lens[1];

	multiArray colors("cols.bin");	//Read colors from file
	int colCount = colors.lens[0];

	multiArray colMap(2, pixIn.lens, 0); //Make colorMap of indexes for output

	printf("Testing colMap\n");	uint8_t foo = colMap.get(0,0);	printf("Got:%d\n", foo);

	for(int x=0; x<iW; x++){
		for(int y=0; y<iH; y++){
			//Get comp val
			uint8_t* pixCheck = pixIn.getPtr(x,y,0);

			// printf("Check get: %d %d %d\n", pixIn.get(x,y,0), pixIn.get(x,y,1), pixIn.get(x,y,2));
			// printf("Check ptr: %d %d %d\n", pixCheck[0], pixCheck[1], pixCheck[2]);

			//Get best color index
			int bestColIndex = 0;
			int bestColScore = compPix(pixCheck, colors.getPtr(0));



			for(int i=1; i<colCount; i++){
				uint8_t* colCheck = colors.getPtr(i);
				int score = compPix(pixCheck, colors.getPtr(i));
				if(score < bestColScore){
					bestColScore = score;
					bestColIndex = i;
				}
			}


			//Save
			for(uint i=0; i<3; i++){	//Save pixIn to color val
				pixIn.set(colors.get(bestColIndex, i), x,y,i);
			}

			// printf("colMap 0 0 is %d\n", colMap.get(0,0));
			// printf("Setting colMap (%d,%d) to %d\n", x,y,bestColIndex);
			colMap.set(bestColIndex, x,y);
		}
	}

	pixIn.save("pix.bin");
	colMap.save("colMap.bin");
}