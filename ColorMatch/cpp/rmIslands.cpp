#include <iostream>
#include <fstream>

#include <iomanip>
#include <stdlib.h>
#include <time.h>
#include <math.h>
// #include <string>

using namespace std;

int iW;
int iH;

int minGroupSize = 10;

// struct linkPoint{
// 	linkPoint* next;
// 	int x;
// 	int y;
// }

// class linkPointList{
// 	public:
// 		linkPoint* first;
// 		linkPoint* end;
// 		bool popFirst(int* output){
// 			if(first -> next == NULL){return false;}
// 			output[0] = first -> x;
// 			output[1] = first -> y;
// 			linkPoint tmp = first;
// 			first = first -> next;
// 			delete tmp;

// 		};
// 		void
// }


// class intGrid{
// public:
// 	int iW;
// 	int iH;
// 	int** grid;
// 	intGrid(int _iW, int _iH){
// 		grid = new int*[iW];
// 		for(int i = 0; i < iW; i++){
// 			grid[i] = new int[iH];
// 			for(int j = 0; j < iH; j++){
// 				grid[i][j] = -1;
// 			}
// 		}
// 	};
// };

// void checkPt(int x, int y, int targ, int iW, int iH, int** inGrid, int** outGrid){
// 	if(x < 0 || x >= iW || y < 0 || y >= iH){return}
// 	if(outGrid[x][y] != 0){return;} //Point already checked

// 	if(inGrid[x][y] != targ){
// 		outGrid[x][y] = 2;
// 		return;
// 	}
	
// }

int main(){
	ifstream pixIn;
	pixIn.open("pix.txt");

	pixIn >> iW;
	pixIn >> iH;

	cout << "Running C++ SCRIPT!!!";

	// char inLocation = 20

	// cin >> cout;
	// for(int i=0; i<15; i++){int foo; pixIn >> foo; printf(foo); printf("\n");}

	// cout << "pixIn is " << pixIn.is_open() << "\n";
	// cout << iW << " " << iH << "\n";

	//Init arrays
	int** colVals = new int*[iH];
	int** currMap = new int*[iH];
	bool** ptChecked = new bool*[iH];
	for(int i = 0; i < iW; i++){
		colVals[i] = new int[iW];
		currMap[i] = new int[iW];
		ptChecked[i] = new bool[iW];
		for(int j = 0; j < iW; j++){
			pixIn >> colVals[i][j];
			currMap[i][j] = 0;
			ptChecked[i][j] = false;
		}
	}
	pixIn.close();

	//Get max color
	int colCount = -1;
	for(int ptx = 0; ptx < iW; ptx++){
		for(int pty = 0; pty < iH; pty++){
			if(colVals[ptx][pty] > colCount){colCount = colVals[ptx][pty];}
		}
	}


	//Find groups
	for(int ptx = 0; ptx < iW; ptx++){
		for(int pty = 0; pty < iH; pty++){
			if(ptChecked[ptx][pty]){continue;} //Skip if already checked


			//Clean currMap
			for(int x = 0; x < iW; x++){
				for(int y = 0; y < iH; y++){
					currMap[x][y] = 0;
				}
			}



			// cout << "--------------\n";
			int targCol = colVals[ptx][pty];

			//Loop and find group borders
			int groupCount = 0;
			bool pixPlaced = true;
			currMap[ptx][pty] = 1;

			while(pixPlaced){
				pixPlaced = false;

				for(int x = 0; x < iW; x++){
					for(int y = 0; y < iH; y++){
						if(currMap[x][y] != 0){continue;}

						int isAdjacent = 0;

						if(x+1 < iW && currMap[x +1][y] == 1){isAdjacent += 1;}
						if(x-1 >= 0 && currMap[x -1][y] == 1){isAdjacent += 1;}
						if(y+1 < iH && currMap[x][y +1] == 1){isAdjacent += 1;}
						if(y-1 >= 0 && currMap[x][y -1] == 1){isAdjacent += 1;}

						if(isAdjacent <= 0){continue;} //Ignore if not adjacent

						pixPlaced = true;
						if(colVals[x][y] == targCol){
							currMap[x][y] = 1;
							groupCount += 1;
						}else{
							currMap[x][y] = 2;
						}
					}
				}
			}


			

			//Found group
			if(groupCount > minGroupSize){ //Large, dont remove
				for(int x = 0; x < iW; x++){
					for(int y = 0; y < iH; y++){
						if(currMap[x][y] == 1){ptChecked[x][y] = true;}
					}
				}
			}else{
				//Remove groups

				//Find most common neighbor
				int* colBuckets = new int[colCount];
				for(int i=0; i<colCount; i++){colBuckets[i] = 0;}
				//Fill buckets
				for(int x = 0; x < iW; x++){
					for(int y = 0; y < iH; y++){
						if(currMap[x][y] == 2){colBuckets[colVals[x][y]] += 1;}
					}
				}

				//Find replacement col
				int bestReplaceCol = -1;
				int bestReplaceColCount = -1;
				for(int i=0; i<colCount; i++){
					// cout << colBuckets[i] << ' ';
					if(colBuckets[i] > bestReplaceColCount){
						bestReplaceColCount = colBuckets[i];
						bestReplaceCol = i;
					}
				}

				delete colBuckets;

				//
				for(int x = 0; x < iW; x++){
					for(int y = 0; y < iH; y++){
						if(currMap[x][y] == 1){
							colVals[x][y] = bestReplaceCol;

						}
					}
				}


				// cout << "RM " << targCol << " -> " << bestReplaceCol << '\n';
			}

			// //Print group
			// for(int y = 0; y < iH; y++){
			// 	for(int x = 0; x < iW; x++){
			// 		if(currMap[x][y] == 0){cout << ' ';}
			// 		if(currMap[x][y] == 1){cout << 'X';}
			// 		if(currMap[x][y] == 2){cout << '*';}
			// 		cout << ' ';
			// 	}
			// 	cout << '\n';
			// }


			// cout << groupCount << " " << targCol << "\n";
			// for(int y = 0; y < iH; y++){
			// 	for(int x = 0; x < iW; x++){
			// 		if(ptChecked[x][y]){cout << 'O';}
			// 		else{cout << ' ';}
			// 		cout << ' ';
			// 	}
			// 	cout << '\n';
			// }

			// cout << '\n';

			// for(int y = 0; y < iH; y++){
			// 	for(int x = 0; x < iW; x++){
			// 		cout << colVals[x][y] << ' ';
			// 	}
			// 	cout << '\n';
			// }
			
		}
	}


	//Save
	ofstream pixOut;
	pixOut.open("nPix.txt");
	pixOut << iW << ' ' << iH << '\n';

	for(int x = 0; x < iW; x++){
		for(int y = 0; y < iH; y++){
			pixOut << colVals[x][y];
			if(y < iH-1){pixOut << ' ';}
		}
		pixOut << '\n';
	}
	pixOut.close();

	// for(int x = 0; x < iW; x++){
	// 	for(int y = 0; y < iH; y++){
	// 		cout << colVals[x][y] << ' ';
	// 	}
	// 	cout << '\n';
	// }

	// cout << "------------------\n";

	//Clean up
	for(int i = 0; i < iH; i++){
		delete colVals[i];
		delete currMap[i];
		delete ptChecked[i];
	}
	delete colVals;
	delete currMap;
	delete ptChecked;

	cout << "DONE\n";
}