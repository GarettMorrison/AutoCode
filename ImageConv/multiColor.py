import ezdxf
from PIL import Image
import math as m
import os
import sys
import subprocess as sp
import random as r
import time




# inColors = ((0,0,0), (255,0,0), (0,255,0), (0,0,255))

#Black, Yellow, Blue, Orange, LightBlue
inColors = ((0,0,0), (255,255,0), (0,0,255), (255,127,0), (41,164,232))





# #Run clean, easy to goof otherwise
sp.run(["./cleanUp.sh"])

outString = ""
try:
	outString = sys.argv[1]
except:
	outString = "output"

try:
	os.mkdir("out/" + outString)
	os.mkdir("out/" + outString + "/imgs")
except:		
	print("Error: Output Folder out/" + outString + " already taken")
	sys.exit()



#Define Functions
def getAvgDiff(in1, in2, inMax):
	maxSumDiff = 0
	sumDiff = 0
	for i in range(len(in1)):
			maxSumDiff += inMax	
			sumDiff += abs(in1[i] - in2[i])
	return(sumDiff/maxSumDiff)





#Load input Image
imgPath = ""
if len(sys.argv) > 2:
	imgPath = sys.argv[2]
else:
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

#Actually open image
try:
	inImg = Image.open(imgPath)
	sp.run(["cp", imgPath, ("out/" + outString)]) #Move orig image over
except:
	print("Error opening image")
	sys.exit()

size = inImg.size
pix = inImg.load()





Imgs = []
Pixs = []
ColStrs = []
for color in inColors:
	ColStrs.append('#%02x%02x%02x' % color)
	newImg = Image.new("L", size)
	Imgs.append(newImg)
	Pixs.append(newImg.load())



print("Splitting Image")
tLast = time.time()
for x in range(size[0]):
	t = time.time()
	if t > tLast +2:
		tLast = t
		print(str(round(100*x/size[0], 1)) +"% done")

	for y in range(size[1]):
		px = pix[x,y]
		weights = []
		sumWeights = 0

		for i in range(len(inColors)):
			weight = 1 -getAvgDiff(inColors[i], px, 255)
			weight = pow(weight, 5)
			# weight = m.exp(weight*-10)
			weights.append(weight)
			sumWeights += weight

		for i in range(len(inColors)):
			Pixs[i][x,y] = m.floor(255 *(1 - weights[i]/sumWeights))


		# hardness = 255
		# indArr = []
		# for i in range(len(inColors)): indArr.append(i)
		# while hardness > 0 and len(indArr) > 0:
		# 	maxW = -1
		# 	maxI = -1
		# 	for i in indArr:
		# 		if weights[i] > maxW:
		# 			maxW = weights[i]
		# 			maxI = i

		# 	# print((maxI, indArr))
		# 	# try:
		# 	indArr.remove(maxI)
		# 	h = weights[maxI]*255
		# 	if hardness < h:
		# 		h = hardness
		# 	hardness -= h

		# 	Pixs[maxI][x,y] = m.floor(h)





#Save Images
for i in range(len(inColors)):
	print("Saving " + str(ColStrs[i]))
	Imgs[i].save("out/" +ColStrs[i] + ".png")
	Imgs[i].close()


for i in range(len(inColors)):
	print("\n\nRunning " +ColStrs[i] +"\n")
	sp.run(["python3", "pointilism.py", ColStrs[i], ("out/" +ColStrs[i] +".png")])
	sp.run(["python3", "connectDots.py", ColStrs[i]])
	sp.run(["mv", ("out/" +ColStrs[i] +".png"), ("out/" +outString +"/imgs")]) #Move input Image
	sp.run(["mv", ("out/" +ColStrs[i]), ("out/" +outString)]) #Move output folder to final pos



#Now we have all 3 colors processed

lineDxf = ezdxf.new(setup=True)
lineMSP = lineDxf.modelspace()

lineDxf.layers.new(name='Border', dxfattribs={'linetype': 'CONTINUOUS', 'true_color': 0xAAAAAA})
iW, iH = size
lineMSP.add_line((0,0), (iW,0), dxfattribs={'layer': 'Border'})
lineMSP.add_line((0,0), (0,iH), dxfattribs={'layer': 'Border'})
lineMSP.add_line((iW,0), (iW,iH), dxfattribs={'layer': 'Border'})
lineMSP.add_line((iW,iH), (0,iH), dxfattribs={'layer': 'Border'})



dotDxf = ezdxf.new(setup=True)
dotMSP = dotDxf.modelspace()

dotDxf.layers.new(name='Border', dxfattribs={'linetype': 'CONTINUOUS', 'true_color': 0xAAAAAA})
iW, iH = size
dotMSP.add_line((0,0), (iW,0), dxfattribs={'layer': 'Border'})
dotMSP.add_line((0,0), (0,iH), dxfattribs={'layer': 'Border'})
dotMSP.add_line((iW,0), (iW,iH), dxfattribs={'layer': 'Border'})
dotMSP.add_line((iW,iH), (0,iH), dxfattribs={'layer': 'Border'})




for i in range(len(inColors)):
	# print(ColStrs[i])
	lineDxf.layers.new(name=ColStrs[i],    dxfattribs={'linetype': 'CONTINUOUS', 'true_color': int(ColStrs[i][1:], 16)})
	dotDxf.layers.new(name=ColStrs[i],    dxfattribs={'linetype': 'CONTINUOUS', 'true_color': int(ColStrs[i][1:], 16)})

#Save each output
for i in range(len(inColors)):
	print("Saving " +ColStrs[i])
	inDxf = ezdxf.readfile("out/" +outString +'/' +ColStrs[i] +"/connected.dxf")
	msp = inDxf.modelspace()

	for l in msp.query('LINE'):
		pt1 = l.dxf.start
		pt2 = l.dxf.end
		if l.dxf.layer == "Sketch":
			lineMSP.add_line(pt1, pt2, dxfattribs = {'layer': ColStrs[i]})

#Save each output dots
for i in range(len(inColors)):
	print("Saving " +ColStrs[i])
	inDxf = ezdxf.readfile("out/" +outString +'/' +ColStrs[i] +"/dots.dxf")
	msp = inDxf.modelspace()

	for l in msp.query('POINT'):
		pt1 = l.dxf.location
		if l.dxf.layer == "Sketch":
			dotMSP.add_point(pt1, dxfattribs = {'layer': ColStrs[i]})

lineDxf.saveas(("out/" + outString + "/RGB_connected.dxf"))
dotDxf.saveas(("out/" + outString + "/RGB_dots.dxf"))