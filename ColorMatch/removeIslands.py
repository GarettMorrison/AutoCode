import ezdxf
from PIL import Image
import math as m
import os
import sys
import random as r
import time


minGroupSize = 100



#Arguments
outString = ""
try:
	outString = sys.argv[1]
except:
	print("No output folder selected")
	sys.exit()

#Make output filenames
imgPath = "out/" + outString + "/matched.png"
imgBackupPath = "out/" + outString + "/input_removeIslands.png"


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
for i in range(iW):
	outPts.append([0]*iH)
	ptChecked.append([False]*iH)


colors = []
colCount = 0

#Get every color used
for y in range(iH):
	for x in range(iW):
		testCol = iPix[(x,y)]
		if not testCol in colors:
			colors.append(testCol)
			colCount += 1
		outPts[x][y] = colors.index(testCol)

print(colors)

print("Setting into groups")

pixTotal = iW*iH
pixCounted = 0
frac = 0


#Loop every point
for y in range(iH):
	for x in range(iW):
		if pixCounted/pixTotal > frac:
			frac += 0.005
			print(str(int(frac*1000)/10) + "%")
			try:
				inImg.save("out/" + outString + "/temp.png")
			except:
				print("Unable to save temp")

		if ptChecked[x][y]: #No double set
			continue

		# print("-----" + str((x,y)))

		setCol = colors.index(iPix[(x,y)])
		pixToCheck = [(x,y)]

		groupSize = 0
		groupBorders = []
		groupPix = []

		borderCounts = [0]*colCount
		# print("------------------------------------------------------------------------------------------------")
		while len(pixToCheck) > 0:
			# print(len(pixToCheck))
			pos = pixToCheck.pop(0)
			fooCol = outPts[pos[0]][pos[1]]

			if fooCol != setCol:
				# print("Border " + str(fooCol) + " " + str(setCol))
				groupBorders.append(pos)
				borderCounts[fooCol] += 1
				continue

			if ptChecked[pos[0]][pos[1]]: continue #Dont add if already part of group

			# print("Inside " + str(fooCol) + " " + str(setCol))

			groupPix.append(pos)
			groupSize += 1
			ptChecked[pos[0]][pos[1]] = True
			pixCounted += 1

			checkPos = ((-1,0), (0,-1), (1,0), (0,1))
			for i in checkPos:
				xTest = pos[0] +i[0]
				yTest = pos[1] +i[1]
				if not inRange((xTest, yTest), size): continue #Dont add if outside of image
				if (xTest, yTest) in pixToCheck: continue #Dont add twice
				if (xTest, yTest) in groupBorders: continue #Dont add twice

				pixToCheck.append((xTest, yTest))

		# print("Made Group " + str(setGroup) + " at pos " + str((x,y)) + " with size " + str(groupSize) + " and color " + str(matchCol), end="")

		if groupSize > minGroupSize:
		# 	print("")
			continue

		# print(" and then pruned")

		adjacentGroupCounts = []
		adjacentGroupCols = []

		newColIndex = borderCounts.index(max(borderCounts))
		# print("SET " + str(setCol) + " val " + str(colors[setCol]))
		# print("NEW " + str(newColIndex) + " val " + str(colors[newColIndex]))
		# print(borderCounts)
		# print(str(newColIndex) + " ")
		# print(groupBorders)

		for pos in groupPix:
			iPix[pos] = colors[newColIndex]
			outPts[pos[0]][pos[1]] = newColIndex



inImg.save(imgPath)