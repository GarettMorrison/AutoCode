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
minDist = 0
maxDist = 8

quickSaveTick = 50000

#Big calc vals
maxColor = 0

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
def convertCAD(p):
	pout = (p[0], p[1] * -1)
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

def getImgMax(inPix):
	global size
	maxVal = 0
	for i in range(size[0]):
		for j in range(size[1]):
			if inPix[i,j] > maxVal:
				maxVal = inPix[i,j]
	return(maxVal)

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

#End Function Definitions










#Find output string
outString = "output_"
i = 0
while  os.path.exists("out/" + outString + str(i) + ".dxf"):
	i+=1
outString = outString + str(i) 


#Make output file
fileOut = open("out/" + outString + ".txt", "w")

#Load input Image
try:
	#Find any image files in directory
	imgPath = ""
	for file in os.listdir(os.getcwd()):
		if file.endswith(".png"):
			imgPath = file

	inImg = Image.open(imgPath).convert('L')
except IOError:
	print("Unable to load image")
	sys.exit(1)

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
msp.add_line((0,0), (0,-1*iH), dxfattribs={'layer': 'Border'})
msp.add_line((0,0), (iW,0), dxfattribs={'layer': 'Border'})
msp.add_line((iW,0), (iW,-1*iH), dxfattribs={'layer': 'Border'})
msp.add_line((iW,-1*iH), (0,-1*iH), dxfattribs={'layer': 'Border'})


#Done with setup
#We have loaded an input image and initialized an output dxf and image




#Vars
# base = []
# theta = []
# for i in range(15):
# 	base.append()


print("iW (width): " + str(iW))
print("iH (height): " + str(iH))

print("Saveing to:        " + "out/" + outString)
print("Image saving to:   " + "out/" + outString + ".png")
print("Autocad saving to: " + "out/" + outString + ".dxf")
print("Log saving to:     " + "out/" + outString + ".txt")

print("Starting Run")


#Test points
testPix = (50,10)
pos = (100, 100)

# tPix[testPix] = 0
# r = getClosestDist(pos, tPix, True)
# tPix[testPix] = 0
# print("-------------------------------- ", end = "")
# print(r)


#Set inits
maxColor = getImgMax(tPix)
tPix[0,0] = 0
pos = (0,0)
checkPix = 1

#Actually run through procedural generator
while True:
	#Get pixel
	pos = (pos[0]-1, pos[1]+1)


	if pos[0] < 0: #If over left or bottom bound
		pos = (pos[1] + pos[0] + 1, 0)

	while (pos[1] >= iH) or (pos[1] < 0):
		if pos[1] >= iH: #If over bottom bound
			pos = (pos[1] + pos[0] + 1, 0)
		if pos[0] >= iW: #If over right bound
			pos = (iW -1, pos[0] -iW +1)

		if pos[1] >= iH:
			break

	if pos[1] >= iH: #Out of pixels and out of time
		break

	#pos is secured
	dist = getClosestDist(pos, tPix)
	inVal = getPix(pos, iPix)
	targetDist = mapToRange(inVal, (maxColor, 0), (minDist, maxDist))

	#If pixel should be placed
	if dist > targetDist:
		setPix(pos, 0, tPix)
		msp.add_point(convertCAD(pos), dxfattribs={'layer': 'Sketch'})


	








	#Do periodic ifs
	if checkPix % m.floor(quickSaveTick/5) == 0 and checkPix > 10: #Print time estimate
		currTime = time.time()
		timeEst = (currTime - startTime) * (totalPix - checkPix)/checkPix
		print(str(round(100*checkPix/totalPix, 2)) + "% done, " + str(totalPix - checkPix) + "/" + str(totalPix) + " pixels, est ", end = "")
		if timeEst/60 > 1:
			print(str(m.floor(timeEst/60)) + " minutes ", end = '')
		print(str(timeEst%60)[:4] + " seconds.")

	if checkPix % quickSaveTick == 0: #Save current file formate
		tImg.save("dump/" + outString + str(checkPix) + ".png")
		doc.saveas("dump/" + outString + str(checkPix) + ".dxf")
		#Close and reopen in case of crash
		fileOut.close()
		fileOut = open("out/" + outString + ".txt", "a")

	checkPix += 1
	#End big loop








#Save files
tImg.save("out/" + outString + ".png")
doc.saveas("out/" + outString + ".dxf")

#Get endtime
endTime = time.time()
totalTime = endTime - startTime

#Write metadata
metadata = ()
metadata += (("totalPix", str(totalPix)),)
metadata += (("maxColor", str(maxColor)),)
metadata += (("minDist", str(minDist)),)
metadata += (("maxDist", str(maxDist)),)
metadata += (("quickSaveTick", str(quickSaveTick)),)
metadata += (("totalTime", str(totalTime)),)



for i in metadata:
	fileOut.write(i[0] + "," + i[1] + "\n")


print("Done!")
#Start Clock
print("Info----------------")
for i in metadata:
	print(i[0] + ": " + i[1])
print("--------------------")
print("PureData-----------")
for i in metadata:
	print(i[1])
print("--------------------")




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