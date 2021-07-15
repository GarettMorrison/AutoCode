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

int minGroupSize = 5;

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

	multiArray pixIn(fileName, true);
	if(argc > 2){
		minGroupSize = stoi(argv[2]);
	}
	


	iW = pixIn.lens[0];
	iH = pixIn.lens[1];

	// cout << pixIn.lens[0] << ' ' << pixIn.lens[1] << '\n';

	int* pos = new int[2];

	//Init arrays
	// int** colVals = new int*[iH];
	int** currMap = new int*[iW];
	bool** ptChecked = new bool*[iW];


	for(int i = 0; i < iW; i++){

		// colVals[i] = new int[iW];
		currMap[i] = new int[iH];
		ptChecked[i] = new bool[iH];
		for(int j = 0; j < iH; j++){
			pos[0] = i;
			pos[1] = j;
			// colVals[i][j] = pixIn.get(i,j);
			currMap[i][j] = 0;
			ptChecked[i][j] = false;
			// printf("%d %d", i, j);
			// if(pixIn.get(pos) > 0){printf("testsucc %d\n", pixIn.get(pos));}
		}
	}



	//Get max color
	// printf("Printing pixels\n");
	int colCount = -1;
	for(int ptx = 0; ptx < iW; ptx++){
		for(int pty = 0; pty < iH; pty++){
			// printf("%d ", pixIn.get(ptx, pty));
			if(pixIn.get(ptx,pty) > colCount){colCount = pixIn.get(ptx,pty);}
		}
		// printf("\n");
	}



	colCount += 1;

	bool colsRemain = true;

	//Find groups
	while(colsRemain){
		for(int ptx = 0; ptx < iW; ptx++){
			// printf("On line %d\n", ptx);
			for(int pty = 0; pty < iH; pty++){
				if(ptChecked[ptx][pty]){continue;} //Skip if already checked

				//Clean currMap
				for(int x = 0; x < iW; x++){
					for(int y = 0; y < iH; y++){
						currMap[x][y] = 0;
					}
				}

				// printf("bbb\n");

				int targCol = pixIn.get(ptx,pty);

				//Loop and find group borders
				int groupCount = 0;

				currMap[ptx][pty] = 1;

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
						if(currMap[x][y] != 0){continue;}

						if(pixIn.get(x,y) == targCol){
							currMap[x][y] = 1;
							groupCount += 1;

							lastPoint -> next = new linkPoint;
							lastPoint -> next -> x = x;
							lastPoint -> next -> y = y;
							lastPoint = lastPoint -> next;
						}else{
							// printf("%d", pixIn.get(x,y));
							currMap[x][y] = 2;
						}
					}

					linkPoint* temp = currPoint;
					currPoint = currPoint -> next;
					delete temp;
				}	
			}
		}
	}


	// printf("Final Output\n");
	// for(int ptx = 0; ptx < iW; ptx++){
	// 	for(int pty = 0; pty < iH; pty++){
	// 		printf("%d ", pixIn.get(ptx, pty));
	// 	}
	// 	printf("\n");
	// }

	cout << "Saving to " << fileName << '\n';
	pixIn.save(fileName);
	printf("All saved!");

	//Clean up
	for(int i = 0; i < iH; i++){
		// delete colVals[i];
		delete[] currMap[i];
		delete[] ptChecked[i];
	}
	// delete[] colVals;
	delete[] currMap;
	delete[] ptChecked;
	delete pos;

	cout << "DONE!\n";
}