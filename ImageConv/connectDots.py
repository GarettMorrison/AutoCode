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
quickSaveTick = 100000

connections = 8
minAngle = 10 #Set to 0 to ignore

rollLineTarget = -1 #Set -1 to ignore

hexBuckSize = 150 #Set very large to ignore



#Big calc vals
startTime = time.time()

#Arguments
outString = ""
try:
	outString = sys.argv[1]
except:
	outString = "output"


runAvgSet = ((0,0),)*5
def addToAvg(inVal, index):
	global runAvgSet
	avgSet = runAvgSet[index]

	avgSet = ((avgSet[0]*avgSet[1]+inVal)/(avgSet[1]+1), avgSet[1]+1)

	runAvgSet = runAvgSet[:index] + (avgSet,) + runAvgSet[index +1:]



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
		y = (val - line[0])*tan(     line[2]) + line[1]
		x = (y - line[1])*tan(90 - line[2]) + line[0]
	else:
		x = (val - line[1])*tan(90 - line[2]) + line[0]
		y = (x - line[0])*tan(     line[2]) + line[1]

	return((x,y))

def getDist(a,b): #Dist between 2 points
	dist = m.sqrt(pow((a[0]-b[0]), 2) + pow((a[1]-b[1]), 2))
	return dist

def getAngle(a,b): #Dist between 2 points
	outAng = -1
	if(b[0] - a[0] == 0):
		if b[1] > a[1]:
			outAng = 90
		else:
			outAng = 270
	else:
		outAng = atan((b[1]-a[1]) / (b[0]-a[0]))

	# if outAng < 0:
	# 	outAng += 360

	if (b[0]-a[0]) < 0:
		outAng += 180
	if outAng < 0:
		outAng += 360

	return outAng

def getDiffWrap(in1, in2, range):
	basic = abs(in1-in2)
	wrap = abs((in1 +range[1] -range[0] -in2))

	if basic < wrap:
		return(basic)
	else:
		return(wrap)

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

def returnIfInRange(inputArr, pos, sizeMax, sizeMin = (0,0)):
	point = inputArr
	for i in range(len(sizeMax)):
		if pos[i] < sizeMin[i] or pos[i] >= sizeMax[i]:
			return(())
		point = point[pos[i]]
	return(point)


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



def getClosestPts(pos, inPix, getPts = 1, expRange = 0, doPrint = False):
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

		if expRange == 0 :#If checking normally
			if foundCount >= getPts: #Found enough points
				doLoop = False
		else: #Not have expRange var
			if (foundCount)*r >= getPts*expRange:
				doLoop = False

		r += 1


	#Get actual outputs
	outPts = ()
	for i in range(len(minRs)):#Save good points
		if minRs[i] < r:
			outPts = outPts + (minPts[i],)

	return(outPts)

	#End of function, will run infinitely with no pixels to find



#End Function Definitions




infoOutString = "out/" + outString + "/connectedInfo.txt"
dxfOutString = "out/" + outString + "/connected.dxf"
imgInString = "out/" + outString + "/dots.png"






#Find output string
# i = 0
# while  os.path.exists("out/" + outString + str(i) + ".dxf"):
# 	i+=1
# outString = outString + str(i) 


#Make output file
fileOut = open(infoOutString, "w")

#Load input Image
try:
	#Find any image files in directory
	inImg = Image.open(imgInString).convert('L')
except IOError:
	print("Unable to load " + imgInString)
	sys.exit(1)

size = inImg.size
iW, iH = size
totalPix = iW*iH
iPix = inImg.load()



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
#We have loaded an input image and initialized an output dxf

print("Starting ConnectDots")
print("iW (width): " + str(iW))
print("iH (height): " + str(iH))

print("Autocad saving to: " + dxfOutString)
print("Log saving to:     " + infoOutString)

print("Getting Pix")


#Connect dots
print("Loading Dots")
#Make hexagonal square bucket pattern
#odd buckets are offset by 1/2, x has 1 extra bc of this
hexBuck = (((),)*m.ceil(iH/hexBuckSize),)*m.ceil(iW/hexBuckSize +1)

dotsHandled = 0
dots = ()
for i in range(iW):
	for j in range(iH):
		pos = (i,j)
		if not (getPix(pos, iPix) in (-1, 255, 100)):
			by = m.floor(j/hexBuckSize)
			bx = m.floor((i +0.5)/hexBuckSize)
			dotsHandled += 1
			dots += pos,
			hexBuck = hexBuck = hexBuck[:bx] + (hexBuck[bx][:by] + (hexBuck[bx][by] + (pos,) ,) + hexBuck[bx][by +1:] ,) + hexBuck[bx +1:]

# print("---------------------------")
# for ii in range(len(hexBuck[0])):
# 	for jj in range(len(hexBuck)):
# 		print(str(len(hexBuck[jj][ii])).rjust(4), end = " ")
# 	print(" ")

print("Found " + str(dotsHandled) + " dots.")

rollingLen = rollLineTarget

#Init Vals
linesDrawn = 0
lastPrintTime = time.time()
#Add lines
for ptPos in range(len(dots)):
	pt = dots[ptPos]
	t1 = time.time()

	ptbx = m.floor(pt[0]/hexBuckSize)
	ptby = m.floor(pt[1]/hexBuckSize)
	ptboff = (ptby % 2)

	#make tuple of points to consider
	closeDots = ()
	closeDots += returnIfInRange(hexBuck, (ptbx           , ptby   ), (len(hexBuck), len(hexBuck[0]))) #One is in
	closeDots += returnIfInRange(hexBuck, (ptbx +ptboff -1, ptby -1), (len(hexBuck), len(hexBuck[0]))) #UL
	closeDots += returnIfInRange(hexBuck, (ptbx +ptboff   , ptby -1), (len(hexBuck), len(hexBuck[0]))) #UR
	closeDots += returnIfInRange(hexBuck, (ptbx -1        , ptby   ), (len(hexBuck), len(hexBuck[0]))) #L
	closeDots += returnIfInRange(hexBuck, (ptbx +1        , ptby   ), (len(hexBuck), len(hexBuck[0]))) #R
	closeDots += returnIfInRange(hexBuck, (ptbx +ptboff -1, ptby +1), (len(hexBuck), len(hexBuck[0]))) #DL
	closeDots += returnIfInRange(hexBuck, (ptbx +ptboff   , ptby +1), (len(hexBuck), len(hexBuck[0]))) #DR


	#Data at this point in loop
	#pos: input position
	#endPts: sorted list of other points by dist, (X, Y, ang, dist)

	#Sort into array by dist
	endPts = ()
	for endPt in closeDots:
		if pt == endPt: #Dont examine same point
			continue

		dist = getDist(pt, endPt)
		ang = getAngle(pt, endPt)
		#Sort val. I don't have the energy rn to script in binary sort, deal with it. 
		bestPos = len(endPts)
		for i in range(len(endPts)):
			if dist < endPts[i][3]:
				bestPos = i
				break
		endPts = endPts[:bestPos] + ((endPt + (ang, dist)), ) + endPts[bestPos:]

	#If doing rolling len then stop here
	if rollLineTarget > 0:
		for i in endPts:
			if i[3] < rollingLen:
				msp.add_line(convertCAD(pt, yMod = iH), convertCAD(i, yMod = iH), dxfattribs={'layer': 'Sketch'})
				linesDrawn += 1
				rollingLen -= i[3]
			else:
				break
		rollingLen += rollLineTarget

	#No rolling len
	else: 
		#Loop until lines have been found and drawn that meet conditions
		endLoop = False
		for tempCon in range(connections, 0, -1): #loop with decreasing
			for i in range(len(endPts) -tempCon):
				goodRange = True

				for p1 in range(i, i +tempCon -1): #Loop through every pair in current range
					for p2 in range(p1 +1, i +tempCon): 
						diffAng = getDiffWrap(getAngle(pt, endPts[p1]), getAngle(pt, endPts[p2]), (0,360))
						if minAngle > diffAng:
							goodRange = False
				if goodRange:
					for j in range(i, i+tempCon):
						linesDrawn += 1
						outPt = endPts[j]
						# outPt = getLinePt(pt + (outPt[2],), pt[0] + cos(outPt[2])*outPt[3]/3, True)
						msp.add_line(convertCAD(pt, yMod = iH), convertCAD(outPt, yMod = iH), dxfattribs={'layer': 'Sketch'})

					#Break out of whole loop
					endLoop = True
					break
			if endLoop:
				break

	

	currTime = time.time()
	if currTime - lastPrintTime > 1 and ptPos >0:
		lastPrintTime = currTime
		print("Dot " + str(ptPos) + "/" + str(dotsHandled) + " time est ", end = "")
		timeEst = (currTime - startTime)*((dotsHandled -ptPos)/ptPos)
		if timeEst/60 > 1:
			print(str(m.floor(timeEst/60)) + " minutes ", end = '')
		print(str(timeEst%60)[:4] + " seconds.")
		# print(runAvgSet[0])

	t2 = time.time()
	addToAvg(t2-t1, 0)
	#end loop




#Save files
# tImg.save("out/" + outString + ".png")
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
metadata += (("connections", str(connections)),)
metadata += (("minAngle", str(minAngle)),)
metadata += (("hexBuckSize", str(hexBuckSize)),)
metadata += (("dotsHandled", str(dotsHandled)),)
metadata += (("linesDrawn", str(linesDrawn)),)
metadata += (("totalTime", str(totalTime)),)



for i in metadata:
	fileOut.write(i[0] + ", " + i[1] + "\n")


print("Done!")

print("Info----------------")
for i in metadata:
	print(i[0] + ": " + i[1])
print("--------------------")