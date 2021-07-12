#Convert input image to matches within data

from PIL import Image
import math as m
import os
import sys
import time
import subprocess as sp

sys.path.append('pyCommon')
from bin_customLib import newBinArr, saveBinArr, loadBinArr

#TAGS
#shortHand im
#reqTags cpp
#locks
#desc Load original.png in pix iPix


outFolder = sys.argv[1]

print("Loading image")

inImg = Image.open(outFolder + "original.png").convert('RGB')
#Init image
size = inImg.size
iW, iH = size
iPix = inImg.load()
inImg.save(outFolder + "original.png")


pixArr = []
for x in range(iW):
	pixArr.append([])
	for y in range(iH):
		pixArr[x].append([])
		fooPix = iPix[x,y]
		for i in range(3):
			pixArr[x][y].append(fooPix[i])

saveBinArr(outFolder + "bin/pix.bin", pixArr)
saveBinArr(outFolder + "bin/origPix.bin", pixArr)
inImg.close()

print("Loading colors")

colsData = []

readCols = open(outFolder + "dat/colors.txt")
for line in readCols:
	if line == '':
		break
	line = line.split(' ')
	colsData.append([int(line[0]), int(line[1]), int(line[2])])

saveBinArr(outFolder + "bin/cols.bin", colsData)

print("Running ./matchToPix")
sp.run(["./matchToPix.o"], cwd=outFolder+"bin/", stderr = sp.STDOUT)

print("Reloading pix from bin")
readPix = loadBinArr(outFolder + "bin/pix.bin")


print("Saving output")
#Make new image to experiment on
tImg = Image.new("RGB",size, 0)
tPix = tImg.load()

for x in range(iW):
	for y in range(iH):
		for i in range(3):
			px = readPix[x][y]
			tPix[x,y] = (px[0], px[1], px[2])

tImg.save(outFolder + "matched.png")
tImg.save(outFolder + "imageToPix.png")

tImg.close()