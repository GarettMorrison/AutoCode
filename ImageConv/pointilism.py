import ezdxf
from PIL import Image
import math as m
import os
import sys
import random as r
import time


#Start Clock
startTime = time.time()

# Data Structs
# Point (X, Y)
# Line (X, Y, theta)
# Route (X, Y, Theta, Score)

runAvg = (0,0)

#Big Vars
doInvert = 0 #1 inverts, 0 doesnt
skipWhite = 1 #1 does, 0 doesnt
minDist = 3
maxDist = 30

skipPixFactor = 3.2739

quickSaveTick = 100000

# connectDots = 0 #Set to 0 to ignore
# minAngConnect = 0 #Set to 0 to ignore

#Big calc vals
maxColor = 0
minColor = 0


#Arguments
outString = ""
try:
	outString = sys.argv[1]
except:
	outString = "output"

try:
	os.mkdir("out/" + outString)
except:
	if os.listdir("out/" + outString) != []:
		print("Error: Output Folder out/" + outString + " already exists")
		sys.exit()


# connectDots = 0
# try:
# 	connectDots = int(sys.argv[2])
# except:
# 	connectDots = 0

#Start geometry functions
def cos(inputVal):
	return(m.cos(m.radians(inputVal)))

def sin(inputVal):
	return(m.sin(m.radians(inputVal)))

def tan(inputVal):
	return(m.tan(m.radians(inputVal)))

def atan(inputVal):
	return(m.degrees(m.atan(inputVal)))

def getLinePt(line, val, isX): #gets point on line, isX is set to if it's an x input 
	if isX:
		outVal = (val - line[0])*tan(     line[2]) + line[1]
	else:
		outVal = (val - line[1])*tan(90 - line[2]) + line[0]

	return(outVal)

def getDist(a,b): #Dist between 2 points
	dist = m.sqrt(pow((a[0]-b[0]), 2) + pow((a[1]-b[1]), 2))
	return dist

def toRange(input,min,max): #Map to range with overflow
	while input < min:
		input += max - min
	while input > max:
		input -= max - min
	return input

def mapToRange(inVal, inRange, outRange):
	inVal = (inVal - inRange[0])/(inRange[1] - inRange[0])
	inVal = inVal*(outRange[1] - outRange[0]) + outRange[0]

	#If over bounds
	if inVal > outRange[1]:
		inVal = outRange[1]
	if inVal < outRange[0]:
		inVal = outRange[0]

	return(inVal)

def cap(input,min,max): #Map to range with overflow
	if input < min:
		input = min
	if input > max:
		input = max
	return input

def pointLineDist(line, p): #Get Dist from line to point
	if p[0] - line[0] == 0:
		dist = p[1]- line[1]
	else:
		dist = getDist(line,p) * (sin(atan((p[1]-line[1]) / (p[0] - line[0])) - line[2]))
	dist = abs(dist)
	return(dist)

#Autocad Functions
def convertCAD(p, yMod = 0, xMod = 0):
	pout = (p[0] + xMod, p[1] * -1 + yMod)
	return(pout)


#Start image functions
def getPix(p, inPix): #Compare value and point to image, return -1 if OOB
	global iW, iH
	if 0 <= p[0] < size[0] and 0 <= p[1] < size[1]:
		return(inPix[p])
	return(-1)

def compPix( p, val, inPix): #Compare value and point to image, return -1 if OOB
	global iW, iH
	if 0 <= p[0] < iW and 0 <= p[1] < iH:
		return(abs(inPix[p]  - val))
	return(-1)

def setPix(p, val, inPix): #Set pixel val, return false if fail
	global iW, iH

	val = m.floor(cap(val, 0, 255))
	if 0 <= p[0] < iW and 0 <= p[1] < iH:
		inPix[p] = val
		return(True)
	return(False)

def getImgAvg(inPix):
	global size
	count = size[0] * size[1]
	sumVals = 0
	for i in range(size[0]):
		for j in range(size[1]):
			sumVals += inPix[i,j]
	return(sumVals/count)

def getImgRange(inPix):
	global size
	global maxVal
	global minVal
	maxVal = 0
	minVal = 0
	for i in range(size[0]):
		for j in range(size[1]):
			if inPix[i,j] > maxVal:
				maxVal = inPix[i,j]
			if inPix[i,j] < minVal:
				minVal = inPix[i,j]
	return(minVal, maxVal)

def getClosestDist(pos, inPix, doPrint = False):
	global size
	minR = size[0] + size[1] #Set large, so anything is preferable. 

	r = 1
	while True:
		# print("\n" + str(r))
		for i in range(-1*r +1, r+1):
			# print(i, end = " ")
			check = 0
			check += (getPix((   r + pos[0],    i + pos[1]), inPix) in (-1, 255, 100))#Right-up
			check += (getPix((-1*r + pos[0], -1*i + pos[1]), inPix) in (-1, 255, 100))#Left-down
			check += (getPix((-1*i + pos[0],    r + pos[1]), inPix) in (-1, 255, 100))#Top-left
			check += (getPix((   i + pos[0], -1*r + pos[1]), inPix) in (-1, 255, 100))#Bott-right


			#Print search area for debugging
			if doPrint:
				setPix((   r + pos[0],    i + pos[1]), 100, inPix)
				setPix((-1*r + pos[0], -1*i + pos[1]), 100, inPix)
				setPix((-1*i + pos[0],    r + pos[1]), 100, inPix)
				setPix((   i + pos[0], -1*r + pos[1]), 100, inPix)


			if check < 4: #If one of the pix was positive
				tempR = getDist((0,0), (i,r))
				if tempR < minR:
					minR = tempR

		if minR < r: #Confirm that there isn't a closer point, as this may be a corner of the square
			return(minR) 
		r += 1
	#End of function, will run infinitely with no pixels to find



def getClosestPts(pos, inPix, getPts = 1, minAng = 0, doPrint = False):
	global size
	minRs = () #Set large, so anything is preferable.
	minPts = () #Set large, so anything is preferable.

	r = 1
	doLoop = True
	while doLoop:
		# print("\n" + str(r))
		for i in range(-1*r +1, r+1):
			# print(i, end = " ")
			checkPt = (r + pos[0],i + pos[1])
			if checkPt[0] > size[0] and checkPt[1] > size[1]:
				doLoop = False

			checkPts = ()
			checkPts += ((   r + pos[0],    i + pos[1]), )#Right -up
			checkPts += ((-1*r + pos[0], -1*i + pos[1]), )#Left-down
			checkPts += ((-1*i + pos[0],    r + pos[1]), )#Top -left
			checkPts += ((   i + pos[0], -1*r + pos[1]), )#Bot-right

			# check += (getPix((   r + pos[0],    i + pos[1]), inPix) in (-1, 255, 100))#Right -up
			# check += (getPix((-1*r + pos[0], -1*i + pos[1]), inPix) in (-1, 255, 100))#Left-down
			# check += (getPix((-1*i + pos[0],    r + pos[1]), inPix) in (-1, 255, 100))#Top -left
			# check += (getPix((   i + pos[0], -1*r + pos[1]), inPix) in (-1, 255, 100))#Bot-right


			#Print search area for debugging
			if doPrint:
				setPix((   r + pos[0],    i + pos[1]), 100, inPix)
				setPix((-1*r + pos[0], -1*i + pos[1]), 100, inPix)
				setPix((-1*i + pos[0],    r + pos[1]), 100, inPix)
				setPix((   i + pos[0], -1*r + pos[1]), 100, inPix)

			for pt in checkPts:
				if not (getPix(pt, inPix) in (-1, 255, 100)): #If pt exists
					checkR = getDist(pos, pt)
					minPts = minPts	+ (pt,)
					minRs = minRs + (checkR,)
					# print(str(checkPt) + " " + str(minPts))

		
		foundCount = 0
		for i in minRs:
			if i < r:
				foundCount += 1

		if foundCount >= getPts: #Found enough points
			doLoop = False
		# else: #Not have expRange var
		# 	if (foundCount)*r >= getPts*expRange:
		# 		doLoop = False

		r += 1


	#Get actual outputs
	outPts = ()
	for i in range(len(minRs)):#Save good points
		if minRs[i] < r:
			outPts = outPts + (minPts[i],)

	return(outPts)

	#End of function, will run infinitely with no pixels to find



#End Function Definitions










#Find output string
# i = 0
# while  os.path.exists("out/" + outString + str(i) + ".dxf"):
# 	i+=1
# outString = outString + str(i) 


#Make output filenames
infoOutString = "out/" + outString + "/info.txt"
dxfOutString = "out/" + outString + "/dots.dxf"
imgOutString = "out/" + outString + "/dots.png"
imgOrigOutString = "out/" + outString + "/input.png"

#Load output string
fileOut = open(infoOutString, "w")

#Load input Image

#Find any image files in directory
imgPaths = ()
for file in os.listdir(os.getcwd()) + ["img/" + strVal for strVal in (os.listdir(os.getcwd() + "/img"))]:
	print(file)
	if file.endswith(".png"):
		imgPaths += (file,)


if len(imgPaths) == 0:
	print("No Images Found")
	sys.exit()
elif len(imgPaths) == 1:
	imgPath = imgPaths[0]
else:
	print("Multiple Images Found. Please select one.")
	for i in range(1, 1+len(imgPaths)):
		print(str(i).ljust(3, " ") + imgPaths[i -1])
	index = int(input("Select Index:"))
	imgPath = imgPaths[index -1]

if imgPath == "None":
	sys.exit()
inImg = Image.open(imgPath).convert('L')

size = inImg.size
iW, iH = size
totalPix = iW*iH
iPix = inImg.load()

#Make new image to experiment on
tImg = Image.new("L",size, 255)
tPix = tImg.load()


#Make new dxf
doc = ezdxf.new(setup=True)
msp = doc.modelspace()
doc.layers.new(name='Sketch', dxfattribs={'linetype': 'CONTINUOUS', 'color': 1})
doc.layers.new(name='Border', dxfattribs={'linetype': 'CONTINUOUS', 'color': 2})
#Make Border


msp.add_line((0,0), (iW,0), dxfattribs={'layer': 'Border'})
msp.add_line((0,0), (0,iH), dxfattribs={'layer': 'Border'})
msp.add_line((iW,0), (iW,iH), dxfattribs={'layer': 'Border'})
msp.add_line((iW,iH), (0,iH), dxfattribs={'layer': 'Border'})


#Done with setup
#We have loaded an input image and initialized an output dxf and image


#Vars
# base = []
# theta = []
# for i in range(15):
# 	base.append()

print("Starting Pointilism")
print("iW (width): " + str(iW))
print("iH (height): " + str(iH))

print("Saveing to:        " + "out/" + outString)
print("Image saving to:   " + imgOutString)
print("Autocad saving to: " + dxfOutString)
print("Info saving to:    " + infoOutString)

print("Starting Run")


#Test points
# testPix = (50,10)

# tPix[testPix] = 0
# r = getClosestDist(pos, tPix, True)
# tPix[testPix] = 0
# print("-------------------------------- ", end = "")
# print(r)

# pos = (10, 10)
# tPix[20,20] = 0
# tPix[30,30] = 0
# tPix[40,40] = 0
# tPix[50,50] = 0
# tPix[60,60] = 0
# tPix[70,70] = 0
# print("----------------------")
# for i in range(8):
# 	print(str(i) + " " + str(getClosestPts(pos, tPix, getPts = i)))
# print("----------------------")



#Set inits
colorRange = getImgRange(tPix)
if doInvert: #Invert image during runtime
	colorRange = (colorRange[1], colorRange[0])

tPix[0,0] = 0
pos = (0,0)
checkPix = 0
placePix = 0
startLoopTime = time.time()
currTime = startLoopTime
skipIterator = 0
#Actually run through procedural generator
while True:
	#Get pixel
	while skipIterator < skipPixFactor: #Skiup multiple pix sometimes
		pos = (pos[0]-1, pos[1]+1)
		checkPix += 1
		skipIterator += 1
	skipIterator -= skipPixFactor #Is intentionally weird to prevent pattern emergence



	while (pos[1] >= iH) or (pos[1] < 0) or (pos[0] < 0):
		if pos[0] < 0: #If over left bound
			pos = (pos[1] + pos[0] + 1, 0)
		if pos[1] >= iH: #If over bottom bound
			pos = (pos[1] + pos[0] + 1, 0)
		if pos[0] >= iW: #If over right bound
			pos = (iW -1, pos[0] -iW +1)

		if pos[1] >= iH:
			break

	if pos[1] >= iH: #Out of pixels
		break

	#pos is secured
	inVal = getPix(pos, iPix)
	if skipWhite and inVal == 255:
		continue
	dist = getClosestDist(pos, tPix)


	distRange = (minDist, maxDist)
	targetDist = mapToRange(inVal, colorRange, distRange)

	#If pixel should be placed
	if dist > targetDist:
		placePix += 1
		setPix(pos, 0, tPix)
		msp.add_point(convertCAD(pos, yMod = iH), dxfattribs={'layer': 'Sketch'})
	#Do periodic ifs
	if time.time() - currTime > 1: #Print time estimate
		currTime = time.time()
		timeEst = (currTime - startLoopTime) * (totalPix - checkPix)/checkPix
		print(str(round(100*checkPix/totalPix, 2)).rjust(4) + "% done, Placed|Checked|Total" + str(placePix).rjust(m.floor(m.log(totalPix, 10))) + "|" + str(checkPix).rjust(m.floor(m.log(totalPix, 10))) + "|" + str(totalPix).rjust(m.floor(m.log(totalPix, 10))) + " est ", end = "")
		if timeEst/60 > 1:
			print(str(m.floor(timeEst/60)) + " minutes ", end = '')
		print(str(timeEst%60)[:4] + " seconds.")

	if checkPix % quickSaveTick == 0: #Save current file formate
		tImg.save("dump/" + outString + "_" + str(checkPix) + ".png")
		doc.saveas("dump/" + outString + "_" + str(checkPix) + ".dxf")
		#Close and reopen in case of crash
		# fileOut.close()
		# fileOut = open("out/" + outString + ".txt", "a")

	#End big loop
pointTime = time.time() - startLoopTime









# pixConnected = 0
# linesDrawn = 0
# connectTime = 0
# #Connect dots
# if connectDots > 0:
# 	print("Connecting Dots")
# 	#Make outline
# 	msp.add_line((0,0), (0,iH), dxfattribs={'layer': 'Border'})
# 	msp.add_line((iW,0), (iW,iH), dxfattribs={'layer': 'Border'})
# 	msp.add_line((iW,iH), (0,iH), dxfattribs={'layer': 'Border'})

# 	#Add lines
# 	#Init Vals
# 	startLoopTime = time.time()
# 	currTime = startLoopTime
# 	pos = (0,0)
# 	checkPix = 0
# 	skipIterator = 0
# 	doLoop = True

# 	#Big loop
# 	while doLoop:
# 		#Get pixel
# 		while skipIterator < skipPixFactor: #Skiup multiple pix sometimes
# 			pos = (pos[0]-1, pos[1]+1)
# 			checkPix += 1
# 			skipIterator += 1
# 		skipIterator -= skipPixFactor #Same pattern as start so should hit pix



# 		while (pos[1] >= iH) or (pos[1] < 0) or (pos[0] < 0):
# 			if pos[0] < 0: #If over left bound
# 				pos = (pos[1] + pos[0] + 1, 0)
# 			if pos[1] >= iH: #If over bottom bound
# 				pos = (pos[1] + pos[0] + 1, 0)
# 			if pos[0] >= iW: #If over right bound
# 				pos = (iW -1, pos[0] -iW +1)

# 			if pos[1] >= iH:
# 				break

# 		if pos[1] >= iH: #Out of pixels
# 			doLoop = False

# 		if not (getPix(pos, tPix) in (-1, 255, 100)): #Pixel black
# 			pixConnected += 1
# 			points = getClosestPts(pos, tPix, getPts = connectDots, minAng = minAngConnect)
# 			# print(str(pos) + ", " + str(points))
# 			for pt in points:
# 				linesDrawn += 1
# 				msp.add_line(convertCAD(pos, yMod = iH), convertCAD(pt, yMod = iH), dxfattribs={'layer': 'Sketch'})


# 		if time.time() - currTime > 4: #Print time estimate
# 			currTime = time.time()
# 			timeEst = (currTime - startLoopTime) * (placePix - pixConnected)/pixConnected
# 			print(str(round(100*pixConnected/placePix, 2)) + "% done, " + str(pixConnected) + "/" + str(placePix) + " pixel connected, est ", end = "")
# 			if timeEst/60 > 1:
# 				print(str(m.floor(timeEst/60)) + " minutes ", end = '')
# 			print(str(timeEst%60)[:4] + " seconds.")

# 	connectTime = time.time() - startLoopTime


#Save files
tImg.save(imgOutString)
inImg.save(imgOrigOutString)

try:
	doc.saveas(dxfOutString)
except:
	print(dxfOutString + " Taken")
	i = 0
	while True:
		try:
			doc.saveas(dxfOutString[:-4] + "_" + str(i) + ".dxf")
			break
		except:
			print(dxfOutString[:-4] + "_" + str(i) + ".dxf" + " Taken")
			i += 1

#Get endtime
endTime = time.time()
totalTime = endTime - startTime

#Write metadata
metadata = ()
metadata += (("placePix", str(placePix)),)
metadata += (("doInvert", str(doInvert)),)
metadata += (("skipPixFactor", str(skipPixFactor)),)
metadata += (("maxColor", str(maxColor)),)
metadata += (("minColor", str(minColor)),)
metadata += (("minDist", str(minDist)),)
metadata += (("maxDist", str(maxDist)),)
metadata += (("quickSaveTick", str(quickSaveTick)),)

metadata += (("totalPix", str(totalPix)),)
metadata += (("checkPix", str(checkPix)),)
# if connectDots > 0:
# 	metadata += (("linesDrawn", str(linesDrawn)),)

metadata += (("totalTime", str(totalTime)),)
# if connectDots > 0:
# 	metadata += (("connectTime", str(connectTime)),)
metadata += (("pointTime", str(pointTime)),)



for i in metadata:
	fileOut.write(i[0] + "," + i[1] + "\n")


print("Done!")
#Start Clock
print("Info----------------")
for i in metadata:
	print(i[0] + ": " + i[1])
print("--------------------")
# print("PureData-----------")
# for i in metadata:
# 	print(i[1])
# print("--------------------")




#Scrap code I may need later
#I know this is on github and I could just fork like any reasonable person, it's just not worth it

# Get endpoint of line
# # lefInter = (0, getLinePt(line, 0, True))
# # rigInter = (iW, getLinePt(line, iW, True))
# # topInter = (getLinePt(line, 0, False), 0)
# # botInter = (getLinePt(line, iH, False), iH)

# # if 0 <= lefInter[1] < iH and lefInter != startPoint:
# #  	endpoint = lefInter
# # elif 0 <= rigInter[1] < iH and rigInter != startPoint:
# #  	endpoint = rigInter
# # elif 0 <= topInter[0] < iW and topInter != startPoint:
# #  	endpoint = topInter
# # elif 0 <= botInter[0] < iW and botInter != startPoint:
# #  	endpoint = botInter





#Get running average of something
# global runAvg
# runAvg = ((runAvg[0]*runAvg[1]+j)/(runAvg[1]+1), runAvg[1]+1)
# print(runAvg)