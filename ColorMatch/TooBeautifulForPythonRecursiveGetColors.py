import ezdxf
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
	os.mkdir("out/" + outString)
except:		
	if len(os.listdir("out/" + outString)) > 1:
		print("Error: Output Folder out/" + outString + " already exists")
		sys.exit()





#Make output filenames
infoOutString = "out/" + outString + "/info.txt"
imgOutString = "out/" + outString + "/colsMapped.png"

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









#Define big vars
checkColors = [0,0,0]
checkedPix = 0
pxToChange = []


#Recursive function, check pix
sys.setrecursionlimit(100000) #Set limit to recursion, causes segfault :(

def testPx(X, Y):
	global iPix, tPix, iW, iH, checkColors, checkedPix, pxToChange
	pos = (X,Y)
	#Check in range
	if pos[0] < 0 or pos[0] >= iW or pos[1] < 0 or pos[1] >= iH:
		return(False)

	#Get pixel value
	pixel = iPix[pos]
	#If black or white skip
	if sum(pixel) == 0 or sum(pixel) == 765:
		return(False)


	#Confirmed pixel should be run

	print(str(pos) + " | " + str(pixel))
	#Save to arr)ay to change to average
	pxToChange.append(pos)

	#Make pixel black on orig image
	iPix[pos] = (255,255,255)

	#Add val to average
	for i in range(3):
		checkColors[i] = checkColors[i]*checkedPix +pixel[i]
		checkedPix += 1
		checkColors[i] /= checkedPix

	#Test adjacent positions
	testPx(X -1, Y)
	testPx(X, Y -1)
	testPx(X +1, Y)
	testPx(X, Y +1)

	return(True)








#Done with setup
#We have initialized input and output

print("Starting GetColors")


#Loop every pixel
for y in range(iH):
	for x in range(iW):
		# print((x,y))
		#If found new pixel
		if testPx(x, y):
			#Make pixel val
			pixelOut = (m.floor(checkColors[0]), m.floor(checkColors[1]), m.floor(checkColors[2]))

			#Set pix in output
			for i in pxToChange:
				tPix[i] = pixelOut

			print(pixelOut)
			fileOut.write(str(pixelOut[0]) + " " + str(pixelOut[1]) + " " + str(pixelOut[2]))
			checkPix = 0
			pxToChange = []

tImg.save(imgOutString)
fileOut.close()