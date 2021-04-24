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

#Big Vars
lineRadius = 10
lineWeight = 0.25

quickSaveTick = 50

#For each line gen
initialLines = 40
tweakingLines = 15
tweakingDegrees = 0.5

lineCount = 100

#Calculated Consts
weightFactor = -m.log(255 * lineWeight) / lineRadius

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

#Start image functions
def getPix(p, inPix, size): #Compare value and point to image, return -1 if OOB
	iH, iW = size
	if 0 <= p[0] < iW and 0 <= p[1] < iH:
		return(inPix[p])
	return(-1)

def compPix( p, val, inPix, size): #Compare value and point to image, return -1 if OOB
	iH, iW = size
	if 0 <= p[0] < iW and 0 <= p[1] < iH:
		return(abs(inPix[p]  - val))
	return(-1)

def setPix(p, val, inPix, size): #Set pixel val, return false if fail
	iH, iW = size

	val = m.floor(cap(val, 0, 255))
	if 0 <= p[0] < iW and 0 <= p[1] < iH:
		inPix[p] = val
		return(True)
	return(False)

#Autocad Functions
def convertCAD(p):
	pout = (p[0], p[1] * -1)
	return(pout)


def addPixChange(p, val, inSum, inPix, tPix, size): #Calculate diff between actual and changed val
	baseVal = getPix(p, tPix, size)
	if baseVal == -1:	#Catch OOB
		return(inSum)

	inVal = getPix(p, inPix, size)
	diff =  abs(inVal - baseVal) - abs(inVal - val)
	# print("Diff: " + str(diff) + " " + str(baseVal) + " " + str(inVal))

	inSum += diff
	return(inSum)


def newPixVal(line, pTemp, tPix, size):
	outVal = 0
	dist = pointLineDist(line, pTemp)
	change = m.floor(255*lineWeight * m.exp(dist * weightFactor))

	baseVal = getPix(pTemp, tPix, size)
	if baseVal != -1:
		outVal = cap(baseVal - change, 0, 255)

	return outVal

def checkLine(line, inPix, tPix, size): #Check drawing line
	# important vars:
	#Side index goes [left, right, top, bottom]
	# currSide is the starting side of the line
	#nextSide is the end side of the line

	#Load image info
	iH, iW = size

	# # #Turns out I don't actually need these values lol
	# #Get starting side
	# sideDists = [line[0], iW-line[0], line[1], iH-line[1]]
	# currSide = -1
	# minVal = iH*2
	# outPoint = (0,0)
	# for i in range(4):
	# 	if sideDists[i] < minVal:
	# 		minVal = sideDists[i]
	# 		currSide = i

	# #Get end side
	# nextSide = -1
	# for i in range(4):
	# 	if i == currSide:
	# 		continue
	# 	elif i == 0:
	# 		 if 0 <= getLinePt(line, 0, True) < iH:
	# 		 	nextSide = i
	# 	elif i == 1:
	# 		 if 0 <= getLinePt(line, iW, True) < iH:
	# 		 	nextSide = i
	# 	elif i == 2:
	# 		 if 0 <= getLinePt(line, 0, False) < iW:
	# 		 	nextSide = i
	# 	elif i == 3:
	# 		 if 0 <= getLinePt(line, iH, False) < iW:
	# 		 	nextSide = i

	# vertOffset = False
	# if nextSide == 2 or nextSide == 3:
	# 	vertOffset = True

	
	score = 0
	if sin(line[2]) < 0.707: #do vertical pixel offsets rather then horiz
		realPixRadius = m.floor(abs(lineRadius/cos(line[2]))) #Get actual number of pixels to offset, as diagonal lines need more than vert
		for x in range(iW): #go left to right
			y = m.floor(getLinePt(line, x, True))
			for yTemp in range(y - realPixRadius, y + realPixRadius): #Compare values
				pTemp = (x, yTemp)
				setVal = newPixVal(line, pTemp, tPix, size)
				score = addPixChange(pTemp, setVal, score, inPix, tPix, size)

	else: #Horizontal offsets
		realPixRadius = m.floor(abs(lineRadius/sin(line[2]))) #Get actual number of pixels to offset, as diagonal lines need more than horz
		for y in range(iH): #go top to bottom
			x = m.floor(getLinePt(line, y, False))

			for xTemp in range(x - realPixRadius, x + realPixRadius): #Compare values
				pTemp = (xTemp, y)
				setVal = newPixVal(line, pTemp, tPix, size)
				score = addPixChange(pTemp, setVal, score, inPix, tPix, size)


	return(score)



def drawLine(line, tPix, size): #Check drawing line
	# important vars:
	#Side index goes [left, right, top, bottom]
	# currSide is the starting side of the line
	#nextSide is the end side of the line

	#Load image info
	iH, iW = size

	
	#Get starting side
	sideDists = [line[0], iW-line[0], line[1], iH-line[1]]
	currSide = -1
	minVal = iH*2
	for i in range(4):
		if sideDists[i] < minVal:
			minVal = sideDists[i]
			currSide = i

	#Get end side
	nextSide = -1
	for i in range(4):
		if i == currSide:
			continue
		elif i == 0:
			 if 0 <= getLinePt(line, 0, True) < iH:
			 	nextSide = i
			 	outPoint = (0, getLinePt(line, 0, True))
		elif i == 1:
			 if 0 <= getLinePt(line, iW, True) < iH:
			 	nextSide = i
			 	outPoint = (iW, getLinePt(line, iW, True))
		elif i == 2:
			 if 0 <= getLinePt(line, 0, False) < iW:
			 	nextSide = i
			 	outPoint = (getLinePt(line, 0, False), 0)
		elif i == 3:
			 if 0 <= getLinePt(line, iH, False) < iW:
			 	nextSide = i
			 	outPoint = (getLinePt(line, iH, False), iH)


	if sin(line[2]) < 0.707: #do vertical pixel offsets rather then horiz
		realPixRadius = m.floor(abs(lineRadius/cos(line[2]))) #Get actual number of pixels to offset, as diagonal lines need more than vert
		for x in range(iW): #go left to right
			y = m.floor(getLinePt(line, x, True))

			for yTemp in range(y - realPixRadius, y + realPixRadius): #Compare values
				pTemp = (x, yTemp)
				setVal = newPixVal(line, pTemp, tPix, size)
				setPix(pTemp, setVal, tPix, size)

	else: #Horizontal offsets
		realPixRadius = m.floor(abs(lineRadius/sin(line[2]))) #Get actual number of pixels to offset, as diagonal lines need more than horz
		for y in range(iH): #go top to bottom
			x = m.floor(getLinePt(line, y, False))

			for xTemp in range(x - realPixRadius, x + realPixRadius): #Compare values
				pTemp = (xTemp, y)
				setVal = newPixVal(line, pTemp, tPix, size)
				setPix(pTemp, setVal, tPix, size)

	return(outPoint)










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
	inputFile = "input.png"
	inImg = Image.open(inputFile).convert('L')
except IOError:
	print("Unable to load image")
	sys.exit(1)

size = inImg.size
iH, iW = size
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

endPoint = (0,  m.floor(iH/2))
line = (0,0,0)

#Actually run through procedural generator
for i in range(lineCount):
	startPoint = endPoint

	# print("Rand")
	#Run some random lines
	initialBest = (0,0,0,0) #index 3 is score
	for j in range(initialLines):
		theta = (180*j/initialLines) + r.randint(0, 500)/100
		line = startPoint + (theta,)
		score = checkLine(line, iPix, tPix, size)
		if score > initialBest[3]:
			initialBest = line + (score,)

		# print("------Line: " + str(line) + " Score: " + str(score))

	# print("Tweak")
	#Run some tweaked lines from the best big one
	lineBest = initialBest
	for j in range(tweakingLines):
		theta = lineBest[2]  + tweakingDegrees*(j - tweakingLines/2) + r.randint(1, m.ceil(tweakingDegrees*25))/25
		line = startPoint + (theta,)
		score = checkLine(line, iPix, tPix, size)
		if score > lineBest[3]:
			lineBest = line + (score,)

		# print("------Line: " + str(line) + " Score: " + str(score))





	print(("Count: " + str(i+1) + '/' + str(lineCount)).ljust(18) + " Line: " + str(lineBest[0])[:6].ljust(6) + " " + str(lineBest[1])[:6].ljust(6) + " "+ str(lineBest[2])[:6].ljust(6) + " Score: " + str(lineBest[3]) )

	#Best line picked, now to output
	#Draw line on image
	endPoint = drawLine(lineBest, tPix, size)

	#Print line to dxf
	msp.add_line(convertCAD(startPoint), convertCAD(endPoint), dxfattribs={'layer': 'Sketch'})

	#Print line to file
	fileOut.write(str(startPoint[0]) + "," + str(startPoint[1]) + "," + str(endPoint[0]) + "," + str(endPoint[1]) + "," + str(lineBest[3]) + "\n")

	if i%20 == 0 and i > 10: #Print time estimate
		currTime = time.time()
		timeEst = (currTime - startTime) * (lineCount - i)/i
		print("TODO: " + str(lineCount - i) + " lines in ", end = "")
		if timeEst/60 > 1:
			print(str(m.floor(timeEst/60)) + " minutes ", end = '')
		print(str(timeEst%60)[:4] + " seconds.")

	if i % quickSaveTick == 0: #Save current file formate
		tImg.save("dump/" + outString + str(i) + ".png")
		doc.saveas("dump/" + outString + str(i) + ".dxf")
		#Close and reopen in case of crash
		fileOut.close()
		fileOut = open("out/" + outString + ".txt", "a")



#Save files
tImg.save("out/" + outString + ".png")
doc.saveas("out/" + outString + ".dxf")

#Get endtime
endTime = time.time()
totalTime = endTime - startTime

#Write metadata
metadata = ()
metadata += (("lineRadius", str(lineRadius)), )
metadata += (("lineWeight", str(lineWeight)), )
metadata += (("initialLines", str(initialLines)), )
metadata += (("tweakingLines", str(tweakingLines)), )
metadata += (("tweakingDegrees", str(tweakingDegrees)), )
metadata += (("quickSaveTick", str(quickSaveTick)), )
metadata += (("totalTime", str(totalTime)), )

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