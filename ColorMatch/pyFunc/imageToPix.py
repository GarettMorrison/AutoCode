#Convert input image to matches within data

from PIL import Image
import math as m
import os
import sys
import time

#TAGS
#shortHand im
#reqTags
#locks
#desc Load original.png in pix iPix

from pyCommon.bin_customLib import newBinArr, saveBinArr, loadBinArr

outFolder = sys.argv[1]


inImg = Image.open(outFolder + "original.png").convert('RGB')
#Init image
size = inImg.size
iW, iH = size
iPix = inImg.load()
inImg.save(outFolder + "original.png")

#Make new image to experiment on
tImg = Image.new("RGB",size, 0)
tPix = tImg.load()


pixArr = []
for x in range(iW):
	pixArr.append([])
	for y in range(iH):
		pixArr[x].append([])
		fooPix = iPix[x,y]
		for i in range(3):    
			# print(fooPix)
			pixArr[x][y].append(fooPix[i])

# print(pixArr)
saveBinArr(outFolder + "bin/pix.bin", pixArr)
saveBinArr(outFolder + "bin/iPix.bin", pixArr)