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



	bool** ptChecked = new bool*[iW];


	for(int i = 0; i < iW; i++){
		ptChecked[i] = new bool[iH];
		for(int j = 0; j < iH; j++){
			ptChecked[i][j] = false;
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
	for(int x=0; x < colCount; x++){printf("Col %d : %d\n", x, colGroupSizes[x]);}

	uint* colEdgeCounts = new uint[colCount];
	for(int x=0; x < colCount; x++){
		colEdgeCounts[x] = 0;
	}

	//Go over edges of map
	for(int ptx = 0; ptx < iW; ptx++){
		if(ptx != 0 && ptx != iW-1){continue;} //Skip non edge
		for(int pty = 0; pty < iH; pty++){
			if(pty != 0 && pty != iH-1){continue;} //Skip non edge

			if(ptChecked[ptx][pty]){continue;} //Skip if already checked

			// printf("bbb\n");

			int targCol = pixIn.get(ptx,pty);

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
					if(ptChecked[x][y]){continue;}

					if(pixIn.get(x,y) == targCol || pixIn.get(x,y) == 255){
						ptChecked[x][y] = true;
						colEdgeCounts[targCol] += 1;

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

	int maxInd = -1;
	int maxCount = 0;
	for(int i=0; i<colCount; i++){
		if(colGroupSizes[i] > maxCount){
			maxCount = colGroupSizes[i];
			maxInd = i;
		}
	}


	for(int x = 0; x < iW; x++){
		for(int y = 0; y < iH; y++){
			if(pixIn.get(x,y) == targCol || pixIn.get(x,y) == 255){

			}
		}
	}
	// 		//Found group
	// 		if(groupCount > minGroupSize){ //Large, dont remove
	// 			for(int x = 0; x < iW; x++){
	// 				for(int y = 0; y < iH; y++){
	// 					if(currMap[x][y] == 1){ptChecked[x][y] = true;}
	// 				}
	// 			}
	// 		}else{
	// 			// printf("REPLACING GROUP at %d,%d\n", ptx, pty);
	// 			//Find most common neighbor
	// 			int* colBuckets = new int[colCount];
	// 			for(int i=0; i<colCount; i++){colBuckets[i] = 0;}
	// 			//Fill buckets
	// 			for(int x = 0; x < iW; x++){
	// 				for(int y = 0; y < iH; y++){
	// 					if(currMap[x][y] == 2){colBuckets[pixIn.get(x,y)] += 1;}
	// 				}
	// 			}

	// 			//Find replacement col
	// 			int bestReplaceCol = 1;
	// 			int bestReplaceColCount = -1;
	// 			for(int i=0; i<colCount; i++){
	// 				// printf("| i%d:%d ", i, colBuckets[i]);
	// 				// cout << colBuckets[i] << ' ';
	// 				if(colBuckets[i] > bestReplaceColCount){
	// 					bestReplaceColCount = colBuckets[i];
	// 					bestReplaceCol = i;
	// 				}
	// 			}

	// 			// printf("\n");


	// 			delete colBuckets;

	// 			//
	// 			for(int x = 0; x < iW; x++){
	// 				for(int y = 0; y < iH; y++){
	// 					if(currMap[x][y] == 1){
	// 						pixIn.set(bestReplaceCol, x, y);
	// 						// printf("Replaced %d with %d\n", targCol, bestReplaceCol);

	// 					}
	// 				}
	// 			}


	// 			// cout << "RM " << targCol << " -> " << bestReplaceCol << '\n';
	// 		}
			
	// 	}
	// }

	// // printf("Final Output\n");
	// // for(int ptx = 0; ptx < iW; ptx++){
	// // 	for(int pty = 0; pty < iH; pty++){
	// // 		printf("%d ", pixIn.get(ptx, pty));
	// // 	}
	// // 	printf("\n");
	// // }

	// cout << "Saving to " << fileName << '\n';
	// pixIn.save(fileName);
	// printf("All saved!");

	//Clean up
	for(int i = 0; i < iH; i++){
		delete[] ptChecked[i];
	}
	// delete[] colVals;
	delete[] ptChecked;
	
	delete pos;

	delete[] colGroupSizes;
	delete[] colEdgeCounts;
	// cout << "DONE!\n";
}