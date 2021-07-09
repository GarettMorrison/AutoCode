import ezdxf
from PIL import Image
import math as m
import os
import sys
import random as r
import time

from pyFunc.bin_customLib import newBinArr, saveBinArr, loadBinArr

#Arguments
outString = ""
try:
	outString = sys.argv[1]
except:
	outString = "output"

try:
	os.mkdir("out")
except:
	print("", end="")
try:
	os.mkdir("out/" + outString)
except:		
	if len(os.listdir("out/" + outString)) > 1:
		input("Error: Output Folder out/" + outString + " already exists. Continue?")
		# sys.exit()



#Make output filenames
infoOutString = "out/" + outString + "/colors.txt"
imgOutString = "out/" + outString + "/matched.png"

#Load output string
fileOut = open(infoOutString, "w")

#Load input Image
imgPath = ""
if len(sys.argv) > 2:
	imgPath = sys.argv[2]
else:
	#Find any image files in directory
	imgPaths = ()
	for file in os.listdir(os.getcwd()) + ["img/" + strVal for strVal in (os.listdir(os.getcwd() + "/img"))]:
		# print(file)
		if file.endswith(".png"):
			imgPaths += (file,)

	if len(imgPaths) == 0:
		print("No Images Found")
		sys.exit()
	elif len(imgPaths) == 1:
		imgPath = imgPaths[0]
		print("One image found: " + imgPath)
	else:
		print("Multiple Images Found. Please select one.")
		for i in range(1, 1+len(imgPaths)):
			print(str(i).ljust(3, " ") + imgPaths[i -1])
		index = int(input("Select Index:"))
		imgPath = imgPaths[index -1]

	if imgPath == "None":
		sys.exit()

#Actually open image
try:
	inImg = Image.open(imgPath).convert('RGB')
except:
	print("Error opening image")
	sys.exit()

size = inImg.size
iW, iH = size
totalPix = iW*iH
iPix = inImg.load()

#Make new image to experiment on
tImg = Image.new("RGB",size, 0)
tPix = tImg.load()




def inRange(pos, size):
	for i in range(len(pos)):
		if pos[i] < 0 or pos[i] >= size[i]:
			return(False)
	else:
		return(True)


#Done with setup
#We have initialized input and output

print("Starting GetColors")


groupCount = 1

outPts = []
for i in range(iW):
	outPts.append([0]*iH)


#Loop every pixel
for x in range(iW):
	for y in range(iH):
		if iPix[(x,y)] == (0,0,0):
			outPts[x][y] = -1



print("Starting run to sort pixels")
#Loop every point
for y in range(iH):
	for x in range(iW):
		if outPts[x][y] != 0: #No double set
			continue

		newGroup = groupCount
		print("Made Group " + str(newGroup) + " at pos " + str((x,y)))
		groupCount += 1

		pixToCheck = [(x,y)]

		while len(pixToCheck) > 0:
			pos = pixToCheck.pop(0)
			outPts[pos[0]][pos[1]] = newGroup

			checkPos = ((-1,0), (0,-1), (1,0), (0,1))
			for i in checkPos:
				xTest = pos[0] +i[0]
				yTest = pos[1] +i[1]
				if not inRange((xTest, yTest), size): continue
				if not outPts[xTest][yTest] == 0: continue
				if (xTest, yTest) in pixToCheck: continue

				pixToCheck.append((xTest, yTest))

			
print("Getting group averages")

outCols = []
for i in range(groupCount):
	outCols.append([0,0,0])

outColsCounts = [0]*groupCount

for y in range(iH):
	for x in range(iW):
		group = outPts[x][y]
		if group > 0:
			pixel = iPix[(x,y)]
			for i in range(3):
				outCols[group][i] = outCols[group][i]*outColsCounts[group] +pixel[i]
				outColsCounts[group] += 1
				outCols[group][i] /= outColsCounts[group]

finCols = []
for i in range(groupCount):
	fooCol = (m.floor(outCols[i][0]), m.floor(outCols[i][1]), m.floor(outCols[i][2]))
	finCols.append(fooCol)


for y in range(iH):
	for x in range(iW):
		group = outPts[x][y]
		if group > 0:
			tPix[(x,y)] = finCols[group]

print("Printing colors:")
for i in finCols:
	if i != (0,0,0):
		strOut = str(i[0]) + " " + str(i[1]) + " " + str(i[2])
		print(strOut)
		fileOut.write(strOut + "\n")

saveBinArr("out/"+outString+"/colors.bin", finCols)
tImg.save(imgOutString)
fileOut.close()
