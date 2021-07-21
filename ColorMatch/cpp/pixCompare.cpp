#include "pixCompare.h"

#include <iostream>

#include <stdlib.h>
#include <math.h>
#include <fstream>
// #include <stdint.h>
#include <sys/types.h>
using namespace std;

uint32_t compPix(uint8_t* pix1, uint8_t* pix2){
	uint32_t sumDiff = 1;
	// for(size_t i=0; i<3; i++){
	// 	sumDiff *= abs(pix1[i] - pix2[i]) + 25;
	// }

	sumDiff += abs(pix1[0] - pix2[0]);
	sumDiff += abs(pix1[1] - pix2[1]);
	sumDiff += abs(pix1[2] - pix2[2]);

	return(sumDiff);
};