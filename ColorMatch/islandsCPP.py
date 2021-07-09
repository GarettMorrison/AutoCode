import ezdxf
from PIL import Image
import math as m
import os
import sys
import subprocess as sp
# import random as r
# import time
from pyFunc.bin_customLib import newBinArr, saveBinArr, loadBinArr

minGroupSize = 100



#Arguments
outFolder = ""
try:
	outFolder = "out/" + sys.argv[1]
except:
	print("No output folder selected")
	sys.exit()

#Make output filenames
imgPath = outFolder + "/matched.png"
imgBackupPath = outFolder + "/input_removeIslands.png"


#Actually open image
try:
	inImg = Image.open(imgPath).convert('RGB')
	iPix = inImg.load()
except:
	print("Error opening image")
	sys.exit()

#Get data
size = inImg.size
iW, iH = size
totalPix = iW*iH

#Save image for posterity
print("Saving " + imgBackupPath)
inImg.save(imgBackupPath)




def inRange(pos, size):
	for i in range(len(pos)):
		if pos[i] < 0 or pos[i] >= size[i]:
			return(False)
	else:
		return(True)


#Done with setup
#We have initialized input and output

#Split into colors, similar to getColors
print("Finding colors")



outPts = []
ptChecked = []

colors = []

#Get every color used
for x in range(iW):
	outPts.append([0]*iH)
	ptChecked.append([False]*iH)

	for y in range(iH):
		testCol = iPix[(x,y)]
		if not testCol in colors:
			colors.append(testCol)
		outPts[x][y] = colors.index(testCol)

print(colors)

print("Saving data for C++ script")

tmpFolder = outFolder + "/tmp/"

if not os.path.isdir(outFolder + "/tmp"):
	os.mkdir(outFolder + "/tmp")

#Save colors
# colFile = open(tmpFolder + "colors.txt", "w+")
# colFile.write(str(len(colors)) + "\n")
# for fooCol in colors:
# 	colFile.write(str(fooCol[0]) + " ")
# 	colFile.write(str(fooCol[1]) + " ")
# 	colFile.write(str(fooCol[2]) + "\n")
# colFile.close()

#Save pix
pixArr = []
for x in range(iW):
	pixArr.append([])
	for y in range(iH):
		pixArr[x].append(outPts[x][y])

print("Saving "+ tmpFolder + "cArr.bin")
saveBinArr(tmpFolder + "cArr.bin", pixArr)


# print("Compiling & running script")
# sp.call(["make"], cwd="cpp")
# print("Made!")
sp.call(["cp","cpp/o/rmIslands.o",tmpFolder])
print("Moved!")
sp.run(["./rmIslands.o"], cwd=tmpFolder)
print("Ran!")


print("------------")

oPix = loadBinArr(tmpFolder + "ncArr.bin")

# pixRead = open(tmpFolder + "nPix.txt", "r")
# print(pixRead.readline())
# for x in range(iW):
# 	line = pixRead.readline()
# 	line = line.split(' ')
# 	for y in range(iH):
# 		outPts[x][y] = int(line[y])
# 		iPix[(x,y)] = colors[outPts[x][y]]	

# for i in outPts: print(i)
# print("Final pts")
for x in range(iW):
	for y in range(iH):
		# print(colors[oPix[x][y]])
		iPix[(x,y)] = colors[oPix[x][y]]

inImg.save(outFolder + "/temp.png")
inImg.save(outFolder + "/matched.png")
inImg.close()
