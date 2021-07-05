#Custom .bin file encoding for multidimensional arrays
#Made by Garett Morrison
#First int (4 bytes) determines number of dimensions (N)
#N following bytes determines length in each dimension, highest to lowest
#Following bytes are the data, one byte per address, using ints 0-255

import struct

def newBinArr(lens, blankVal = 0):
	if len(lens) == 1:
		arr = [blankVal]*lens[0]
	else:
		arr = []
		for i in range(lens[0]):
			arr.append(newBinArr(lens[1:], blankVal))
	return(arr)



def recursiveSave(oFile, inObj):
	if(type(inObj) is int):
		oFile.write(inObj.to_bytes(1, 'big'))
	else:
		for i in inObj:
			recursiveSave(oFile, i)
	return(0)


def saveBinArr(oFileName, arr):
	oFile = open(oFileName, "wb")

	dims = []
	foo = arr
	while type(foo) is not int:
		dims.append(len(foo))
		foo = foo[0]

	oFile.write(len(dims).to_bytes(4, 'big'))
	for i in dims: 
		oFile.write(i.to_bytes(4, 'big'))

	recursiveSave(oFile, arr)

	oFile.close()
	return(1)



def recursiveLoad(lens, iFile):
	arr = []
	for i in range(lens[0]):
		if len(lens) == 1:
			arr.append(int.from_bytes(iFile.read(1), "big")) #Read 1 byte to int
		else:
			arr.append(recursiveLoad(lens[1:], iFile))
	return(arr)


def loadBinArr(iFileName):
	iFile = open(iFileName, "rb")

	dimCount = int.from_bytes(iFile.read(4), "big")
	dims = []
	for i in range(dimCount):
		dims.append(int.from_bytes(iFile.read(4), "big"))

	arr = recursiveLoad(dims, iFile)

	iFile.close()
	return(arr)