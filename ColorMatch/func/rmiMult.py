from PIL import Image
import math as m
import os
import sys
import subprocess as sp
import time

sys.path.append('pyCommon')
from bin_customLib import newBinArr, saveBinArr, loadBinArr
from getInputFile import newDir

#TAGS
#shortHand rmim
#reqTags cpp im
#locks matched
#desc Remove small areas from image, running parralel scripts

outFolder = sys.argv[1]
workDir = outFolder + "bin/"
newDir(workDir + "split")

colors = loadBinArr(outFolder + "bin/cols.bin")

boxSize = 100
groupSize = 20

timeOut = 60

colMap = loadBinArr(outFolder + "bin/colMap.bin")

#Get init values
iW = len(colMap)
iH = len(colMap[0])

xDivs = m.ceil(iW/boxSize)
yDivs = m.ceil(iH/boxSize)

xDivLen = m.floor(iW/xDivs)
yDivLen = m.floor(iH/yDivs)

xBreaks = []
for x in range(xDivs): xBreaks.append(x*xDivLen)
xBreaks.append(iW)

yBreaks = []
for y in range(yDivs): yBreaks.append(y*yDivLen)
yBreaks.append(iH)

#Save in subArrs
for x in range(xDivs):
	for y in range(yDivs):
		xSize = xBreaks[x+1] - xBreaks[x]
		ySize = yBreaks[y+1] - yBreaks[y]
		tempArr = newBinArr([xSize, ySize])
		print("OutSlice: " + str(x) + ' ' + str(y) + " is " + str(xSize) + 'x' + str(ySize))
		for ix in range(xSize):
			for iy in range(ySize):
				# print(str(ix) + ',' + str(iy) + " real:" + str(xBreaks[x]) + ',' + str(yBreaks[y]))
				tempArr[ix][iy] = colMap[ix + xBreaks[x]][iy + yBreaks[y]]

		saveBinArr(workDir + "split/" + "s_" + str(x) + '_' + str(y) + ".bin", tempArr)


#Startup procs, 1 per subArr
tossOut = open(os.devnull, 'w')
jobSet = []
idSet = []

dumpOut = open("log_dump/rmi.txt", "w")

for x in range(xDivs):
	for y in range(yDivs):
		fooProc = sp.Popen(["./rmIslands.o", "split/"+"s_"+str(x)+'_'+str(y)+".bin", str(groupSize)], cwd = workDir, stderr = sp.STDOUT, stdout = dumpOut)
		print("Init job on " + "split/"+"s_"+str(x)+'_'+str(y)+".bin")
		jobSet.append(fooProc)
		idSet.append(str(x) + '_' + str(y))

dumpOut.close()

del colMap
del tempArr
startTime = time.time()

#Wait for procs to end
while len(jobSet) > 0:
	i = 0
	while i < len(jobSet):
		if jobSet[i].poll() is not None:
			jobSet.pop(i)
			idSet.pop(i)

		i += 1
	print(str(len(jobSet)) + " jobs remaining")
	print(idSet)
	time.sleep(0.5)

	currTime = time.time()
	if (timeOut - (currTime - startTime)) < 0:
		print("KILLLL")
		while len(jobSet) > 0:
			print(jobSet[0].pid)
			sp.Popen.kill(jobSet[0])
			jobSet.pop(0)

	print("Time to timeout:" + str(timeOut - (currTime - startTime)))

# tossOut.close()



#Save output
colMap = newBinArr([iW,iH])
print("Reloading!")

for x in range(xDivs):
	for y in range(yDivs):
		xSize = xBreaks[x+1] - xBreaks[x]
		ySize = yBreaks[y+1] - yBreaks[y]
		tempArr = loadBinArr(workDir + "split/" + "s_" + str(x) + '_' + str(y) + ".bin")

		print("OutSlice: " + str(x) + ' ' + str(y) + " is " + str(xSize) + 'x' + str(ySize) + " tempArr:" + str(len(tempArr)) + "x" + str(len(tempArr[0])))
		for ix in range(xSize):
			for iy in range(ySize):
				# print(str(ix) + ',' + str(iy) + " real:" + str(xBreaks[x]) + ',' + str(yBreaks[y]))
				colMap[ix + xBreaks[x]][iy + yBreaks[y]] = tempArr[ix][iy]

print("Saving " +outFolder +"rmiMult.png")
oImg = Image.new("RGB", (len(colMap), len(colMap[0])), 0)
oPix = oImg.load()
for x in range(len(colMap)):
	for y in range(len(colMap[0])):
		colInd = colMap[x][y]
		oPix[x,y] = (colors[colInd][0], colors[colInd][1], colors[colInd][2])

oImg.save(outFolder +"rmiMult.png")
oImg.save(outFolder +"matched.png")
oImg.close()


sp.run(["rm", workDir+"split/", "-r"])


# print("Running final combination")
# saveBinArr(outFolder + "bin/colMap.bin",colMap)
# del colMap
# sp.run(["./rmIslands.o", "colMap.bin", str(finGroupSize)], cwd = workDir, stderr = sp.STDOUT)#, stdout = tossOut)

# colMap = loadBinArr(outFolder + "bin/colMap.bin")
# print("Saving final image")
# oImg = Image.new("RGB", (len(colMap), len(colMap[0])), 0)
# oPix = oImg.load()
# for x in range(len(colMap)):
# 	for y in range(len(colMap[0])):
# 		colInd = colMap[x][y]
# 		# for i in range(3): outPix[x][y][i] = colors[colInd][i]
# 		oPix[x,y] = (colors[colInd][0], colors[colInd][1], colors[colInd][2])

# oImg.save(outFolder +"rmiMult_final.png")
# oImg.save(outFolder +"matched.png")
# oImg.close()