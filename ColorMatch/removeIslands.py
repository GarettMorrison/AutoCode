import ezdxf
from PIL import Image
import math as m
import os
import sys
import random as r
import time

minGroupSize = 25



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

colors = []
colCount = 0

#Get every color used
for x in range(iW):
	outPts.append([0]*iH)
	ptChecked.append([False]*iH)

	for y in range(iH):
		testCol = iPix[(x,y)]
		if not testCol in colors:
			colors.append(testCol)
			colCount += 1
		outPts[x][y] = colors.index(testCol)

print(colors)

print("Sorting into groups")

pixTotal = iW*iH
pixCounted = 0
frac = 0


#Loop every point
for y in range(iH):
	for x in range(iW):
		if pixCounted/pixTotal > frac:
			frac += 0.001
			print(str(int(frac*1000)/10) + "%")
			try:
				inImg.save("out/" + outString + "/temp.png")
			except:
				print("Unable to save temp")

		if ptChecked[x][y]: #No double set
			continue

		setCol = colors.index(iPix[(x,y)])
		pixToCheck = [(x,y)]

		#Make new group, init borders and group
		groupSize = 0
		groupBorders = []
		groupPix = []
		borderTallies = [0]*colCount

		# print("------------------------------------------------------------------------------------------------")
		while len(pixToCheck) > 0: #Loop until all pix in group have been checked
			# if len(pixToCheck) > 200:
				# print(len(pixToCheck))

			pos = pixToCheck.pop(0)
			fooCol = outPts[pos[0]][pos[1]]

			groupPix.append(pos)
			groupSize += 1

			ptChecked[pos[0]][pos[1]] = True
			pixCounted += 1

			checkPos = ((-1,0), (0,-1), (1,0), (0,1))
			for i in checkPos:
				testPt = (pos[0] +i[0], pos[1] +i[1])

				if not inRange(testPt, size): continue #Dont add if outside of image
				if testPt in pixToCheck: continue #Dont add twice if already on queue
				if testPt in groupBorders: continue #Dont add twice if already in border
				if testPt in groupPix: continue #Dont add twice if already in group

				if outPts[testPt[0]][testPt[1]] != setCol or ptChecked[testPt[0]][testPt[1]]:
					groupBorders.append(testPt)
					borderTallies[outPts[testPt[0]][testPt[1]]] += 1
					continue

				# if ptChecked[pos[0]][pos[1]]: continue

				pixToCheck.append(testPt)

		# print("Made Group " + str(setGroup) + " at pos " + str((x,y)) + " with size " + str(groupSize) + " and color " + str(matchCol), end="")

		if groupSize > minGroupSize:
			continue

		adjacentGroupCounts = []
		adjacentGroupCols = []

		newColIndex = borderTallies.index(max(borderTallies))
		newCol = colors[newColIndex]

		# print("SET " + str(setCol) + " val " + str(colors[setCol]))
		# print("NEW " + str(newColIndex) + " val " + str(newCol))
		# print(borderTallies)
		# print(str(newColIndex) + " ")
		# print(groupBorders)

		for pos in groupPix:
			ptChecked[pos[0]][pos[1]] = False
			pixCounted -= 1
			iPix[pos] = newCol
			# print("AAAAA")
			outPts[pos[0]][pos[1]] = newColIndex

		# inImg.save("out/" + outString + "/temp.png")
		# sys.exit()


inImg.save(imgPath)
# inImg.save("out/" + outString + "/temp.png")