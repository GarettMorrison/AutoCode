from PIL import Image
import math as m
import os
import sys
import random as r
import time


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
		input("Warning: Output Folder out/" + outString + " already exists. Continue?")


#Make output filenames
infoOutString = "out/" + outString + "/info.txt"
imgOutString_allPix = "out/" + outString + "/input_lessPix.png"
imgOutString_original = "out/" + outString + "/original.png"
imgOutString = "out/" + outString + "/matched.png"

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
inImg.save(imgOutString_original)

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

print("Loading colors.txt")

inFile = open("colors.txt", "r")

colors = []

while True:
	inStr = inFile.readline()
	if inStr == "":
		break
	strs = inStr.split(" ")

	fooCol = (int(strs[0]), int(strs[1]), int(strs[2]))
	print(fooCol)
	colors.append(fooCol)

colCounts = [0]*len(colors)

print("Starting setColors")

pixTotal = iW*iH

pixCounted = 0
frac = 0

# Loop every pixel
for x in range(iW):
	for y in range(iH):
		pixCounted += 1
		if pixCounted/pixTotal > frac:
			frac += 0.01
			print(str(int(frac*100)) + "%")

		currCol = iPix[(x,y)]
		bestCol = -1
		minDist = 255*5

		for i in range(len(colors)):
			sumVals = 0
			for j in range(3): sumVals += abs(colors[i][j] - currCol[j])

			if sumVals < minDist:
				minDist = sumVals
				bestCol = i


		colCounts[bestCol] += 1
		tPix[(x,y)] = colors[bestCol]

tImg.save(imgOutString_allPix)


print("Removing barely used colors")

print(pixTotal)
print(colCounts)

i = 0
while i < len(colors):
	if colCounts[i]/pixTotal < 0.01:
		print("Removing " + str(colors[i]) + " as it makes up " + str(colCounts[i]/pixTotal) + " of the image")
		colors.pop(i)
		colCounts.pop(i)
	else:
		i += 1


print("Getting Final Colors")

pixCounted = 0
frac = 0

# Loop every pixel
for x in range(iW):
	for y in range(iH):
		pixCounted += 1
		if pixCounted/pixTotal > frac:
			frac += 0.01
			print(str(int(frac*100)) + "%")

		currCol = iPix[(x,y)]
		bestCol = (0,0,0)
		minDist = 255*5

		for col in colors:
			sumVals = 0
			for i in range(3): sumVals += abs(col[i] - currCol[i])

			if sumVals < minDist:
				minDist = sumVals
				bestCol = col

		tPix[(x,y)] = bestCol

print("Saved " + imgOutString)
print("Finished running " + outString)

tImg.save(imgOutString)

bigImg = open