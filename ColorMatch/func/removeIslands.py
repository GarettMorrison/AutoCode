from PIL import Image
import math as m
import os
import sys
import subprocess as sp

sys.path.append('pyCommon')
from bin_customLib import newBinArr, saveBinArr, loadBinArr

#TAGS
#shortHand rmi
#reqTags cpp im
#locks matched
#desc Remove small areas from image

groupSize = 40



outFolder = sys.argv[1]

sp.run(["./rmIslands.o", "colMap.bin", str(groupSize)], cwd=outFolder +"bin/", stderr = sp.STDOUT)

colMap = loadBinArr(outFolder + "bin/colMap.bin")
colors = loadBinArr(outFolder + "bin/cols.bin")

outPix = newBinArr([len(colMap), len(colMap[0]), 3], 0)

oImg = Image.new("RGB", (len(colMap), len(colMap[0])), 0)
oPix = oImg.load()

for x in range(len(colMap)):
	for y in range(len(colMap[0])):
		colInd = colMap[x][y]
		for i in range(3): outPix[x][y][i] = colors[colInd][i]
		oPix[x,y] = (colors[colInd][0], colors[colInd][1], colors[colInd][2])

saveBinArr(outFolder +"bin/pix.bin", outPix)
oImg.save(outFolder +"removeIslands.png")
oImg.save(outFolder +"matched.png")