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

int adjPtsOffsets[4][2] = {{0,1},{0,-1},{1,0},{-1,0}};

struct linkPoint{
	linkPoint* next = NULL;
	int x;
	int y;
};



int main(int argc, char *argv[]){
	printf("STL CPP INIT\n");
	if(argc < 2){
		printf("Too Few Args");
	}
	string fileName = argv[1];
	string savDir = argv[2];

	multiArray pixIn(fileName, true);
	// if(argc > 2){
		// minGroupSize = stoi(argv[2]);
	// }

	iW = pixIn.lens[0];
	iH = pixIn.lens[1];

	int* pos = new int[2];

	//Get max color
	int colCount = -1;
	for(int ptx = 0; ptx < iW; ptx++){
		for(int pty = 0; pty < iH; pty++){
			// printf("%d ", pixIn.get(ptx, pty));
			if(pixIn.get(ptx,pty) > colCount){colCount = pixIn.get(ptx,pty);}
		}
		// printf("\n");
	}

	colCount += 1;

	printf("colCount:%d\n", colCount);



	uint mapLens[2] = {0, 0};
	mapLens[0] = iW;
	mapLens[1] = iH;

	printf("iW:%d\n", mapLens[0]);
	printf("iH:%d\n", mapLens[1]);



	int** ptChecked = new int*[iW];

	multiArray outArrBin(2, mapLens, 255);

	for(int i = 0; i < iW; i++){
		ptChecked[i] = new int[iH];
		for(int j = 0; j < iH; j++){
			ptChecked[i][j] = 255;
		}
	}

	uint* colGroupSizes = new uint[colCount];
	for(int x=0; x < colCount; x++){
		colGroupSizes[x] = 0;
	}

	for(int ptx = 0; ptx < iW; ptx++){
		for(int pty = 0; pty < iH; pty++){
			size_t foo = pixIn.get(ptx, pty);
			// printf("%d\n", foo);
			colGroupSizes[foo] += 1;
		}
	}
	// for(int x=0; x < colCount; x++){printf("Col %d : %d\n", x, colGroupSizes[x]);}


	uint* TEMPCHECKS = new uint[colCount];



	uint* colEdgeCounts = new uint[colCount];
	size_t outputCount = 0;
	bool pixRemaining = true;
	while(pixRemaining){	//Loop until all cols have been printed
		pixRemaining = false;

		for(int x=0; x < colCount; x++){	//Reset edgecounts
			colEdgeCounts[x] = 0;
			TEMPCHECKS[x] = 0;
		}


		for(int ptx = 0; ptx < iW; ptx++){
			for(int pty = 0; pty < iH; pty++){
				ptChecked[ptx][pty] = 255;
			}
		}


		//Go over edges of map
		for(int targCol = 0; targCol < colCount; targCol++){	//Loop over checking all colors
			if(colGroupSizes[targCol] == 0){continue;}
			pixRemaining = true;
			printf("Check %d\n", targCol);

			for(int ptx = 0; ptx < iW; ptx++){
				for(int pty = 0; pty < iH; pty++){
					if(ptx != 0 && ptx != iW-1 && pty != 0 && pty != iH-1){continue;} //Skip non edge
					
					int tmpFoo = pixIn.get(ptx,pty);
					if(tmpFoo < colCount){TEMPCHECKS[tmpFoo] += 1;}
					
					

					if(ptChecked[ptx][pty] != 255){continue;} //Skip if already checked
					if(pixIn.get(ptx,pty) != 255 && pixIn.get(ptx,pty) != targCol){continue;}

					//Loop and find group borders

					linkPoint* currPoint = new linkPoint;
					linkPoint* lastPoint = currPoint;
					currPoint -> x = ptx;
					currPoint -> y = pty;

					while(currPoint != NULL){
						for(int i = 0; i < 4; i++){
							// printf("DDDDDD\n");
							int x = currPoint -> x + adjPtsOffsets[i][0];
							int y = currPoint -> y + adjPtsOffsets[i][1];
							// printf("pt %d %d %d \n", i, x, y);
							if(x < 0 || x >= iW || y < 0 || y >= iH){continue;}
							if(ptChecked[x][y] == targCol){continue;}

							if(pixIn.get(x,y) == targCol || pixIn.get(x,y) == 255){
								ptChecked[x][y] = targCol;

								if(pixIn.get(x,y) == targCol){
									colEdgeCounts[targCol] += 1;
									// pixRemaining = true;
								}

								lastPoint -> next = new linkPoint;
								lastPoint -> next -> x = x;
								lastPoint -> next -> y = y;
								lastPoint = lastPoint -> next;
							}
						}

						linkPoint* temp = currPoint;
						currPoint = currPoint -> next;
						delete temp;
					}

				}
			}
		}


		if(!pixRemaining){break;}
		// for(int i=0; i<colCount; i++){printf("EdgeCounts %d %d\n", i, TEMPCHECKS[i]);}

		int maxInd = -1;
		float bestRatio = -1;
		for(int i=0; i<colCount; i++){
			if(colGroupSizes[i] < 1){continue;}

			float currRatio = (float)colEdgeCounts[i]/(float)colGroupSizes[i];

			printf("%d %d %d %.7f \n", i, colGroupSizes[i], colEdgeCounts[i], currRatio);
			if(currRatio > bestRatio){
				bestRatio = (float)colEdgeCounts[i]/(float)colGroupSizes[i];
				maxInd = i;
			}
			else if(currRatio == bestRatio && colGroupSizes[i] > colGroupSizes[maxInd]){
				bestRatio = (float)colEdgeCounts[i]/(float)colGroupSizes[i];
				maxInd = i;	
			}
		}

		for(int x = 0; x < iW; x++){
			for(int y = 0; y < iH; y++){
				if(pixIn.get(x,y) == maxInd || pixIn.get(x,y) == 255){
					outArrBin.set(maxInd, x, y);
					pixIn.set(255, x, y);
				}
				else{
					outArrBin.set(255, x, y);
				}
			}
		}
		colGroupSizes[maxInd] = 0; //Do not consider in future
		printf("Saving number %d color %d\n\n", outputCount, maxInd);
		outArrBin.save(savDir + to_string(outputCount) + "_" + to_string(maxInd) + "_outPix.bin");
		outputCount += 1;
	}

	printf("EXIT LOOP %d\n", iW);

	//Clean up
	for(int i = 0; i < iW; i++){
		delete[] ptChecked[i];
	}

	// delete[] colVals;
	delete[] ptChecked;
	delete pos;

	delete[] colGroupSizes;
	delete[] colEdgeCounts;
	printf("STL CPP DONE!\n");
	// cout << "DONE!\n";
}