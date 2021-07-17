from PIL import Image
import math as m
import os
import sys
import subprocess as sp

sys.path.append('pyCommon')
from bin_customLib import newBinArr, saveBinArr, loadBinArr
from getInputFile import newDir
from makeImg import saveColMapImg, savePixImg

#TAGS
#shortHand stl
#reqTags cpp
#locks matched
#desc WIP Export matched to workable areas

outFolder = sys.argv[1]

colors = loadBinArr(outFolder + "bin/cols.bin")

newDir(outFolder + "bin/layers/")
cppPrintOut = open("log_dump/stlCPP.txt", "w")

sp.run(["./splitLayers.o", "colMap.bin", "layers/"], cwd=outFolder +"bin/", stderr = sp.STDOUT, stdout = cppPrintOut)

bigImg = []
first = True

for binName in os.listdir(outFolder + "bin/layers"):
	file = outFolder + "bin/layers/" + binName
	inArr = loadBinArr(file)
	print(file[:-4]+".png")
	saveColMapImg(file[:-4]+".png", inArr, colors)

	vertGap = [255]*len(inArr[0])

	if not first:
		for i in range(m.floor(len(inArr)/10)):
			bigImg.append(vertGap)
	first = False

	for collumn in inArr:
		bigImg.append(collumn)

saveColMapImg(outFolder + "split.png", bigImg, colors)
# in1 = loadBinArr(outFolder + "bin/layers/l1.bin")

# cols = loadBinArr(outFolder + "dat/cols/")

# saveColMapImg(path, colMap, colors)

print("DONE")