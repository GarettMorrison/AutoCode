from PIL import Image
# import math as m
# import os
# import sys

def saveColMapImg(path, colMap, colors):
	oImg = Image.new("RGB", (len(colMap), len(colMap[0])), 0)
	oPix = oImg.load()
	for x in range(len(colMap)):
		for y in range(len(colMap[0])):
			colInd = colMap[x][y]
			oPix[x,y] = (colors[colInd][0], colors[colInd][1], colors[colInd][2])
	oImg.save(path)
	oImg.close()



def savePixImg(path, pix):
	oImg = Image.new("RGB", (len(pix), len(pix[0])), 0)
	oPix = oImg.load()
	for x in range(len(pix)):
		for y in range(len(pix[0])):
			oPix[x,y] = (pix[x][y][0], pix[x][y][1], pix[x][y][2])
	oImg.save(path)
	oImg.close()