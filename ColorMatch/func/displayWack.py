import os
import sys
import subprocess as sp
import math as m

sys.path.append('pyCommon')
from bin_customLib import newBinArr, saveBinArr, loadBinArr
from makeImg import saveColMapImg, printCols
from getInputFile import newDir

#TAGS
#shortHand diw
#reqTags cpp im
#locks
#desc display top 4 colors simultaneously

layers = 7



outFolder = sys.argv[1]

newDir(outFolder + "displayWack/")

colRank = loadBinArr(outFolder + "bin/colsRanked.bin")

colors = loadBinArr(outFolder + "bin/cols.bin")



iW = len(colRank)
iH = len(colRank[0])
colCountTotal = len(colRank[0][0])

if colCountTotal != len(colors):
	throw("Ranked Cols and colors did not match")

printCols(outFolder + "displayWack/ColorsOut.png",colors)

displayCols = newBinArr([iW, iH], 255)

print(colors)
print(colRank[10][m.floor(iH/3)])

colScores = []
colIDs = []
for i in range(len(colors)):
	colIDs.append(i)
	colScores.append(0)

bestLayers = []
for i in range(layers): bestLayers.append(0)




for i in range(len(colors)): colScores[0]


# colInRanked = []
# for i in range(len(colors)): colInRanked.append(0)

#Get scores for ranking
#Low scores are best, 0->0  score, 1-n-> n+2 score


while len(colIDs) >= layers:
	for i in range(colCountTotal): colScores[i] = 0


	for x in range(iW):
		for y in range(iH):
			for i in range(colCountTotal):
				# if i > layers: break
				fooID = colRank[x][y][i]
				if fooID in colIDs:
					colScores[fooID] += 1
					break

				# foo = colCountTotal - i
				# if i == 0: foo += 5
				# elif i < 3: foo += 2

				# colScores[fooID] += m.pow(foo, 2)

	print("-")
	for i in colIDs: 
		print(("Score " + str(i).rjust(3," ") + ' :') + str(colScores[i]))

	print("-")
	# for i in range(colCountTotal): print(f"Mention {i}:{colInRanked[i]}")
	# print(" ")

	# saveMentions = open(outFolder + "mentions.csv", "w+")
	# saveMentions.write("ColorIndex,Mentions\n")
	# for i in range(colCountTotal): saveMentions.write(f"{i},{colInRanked[i]}\n")
	# saveMentions.close()

	for i in range(layers): bestLayers[i] = 0

	for checkID in colIDs:
		for j in range(layers):
			bestID = bestLayers[j]
			# print(f"{j} IDs: {checkID}, {bestID} Scores: {colScores[checkID]}, {colScores[bestID]}")
			
			if colScores[checkID] > colScores[bestID]:
				# print(f"{checkID}:{colScores[checkID]} > {bestID}:{colScores[bestID]}")
				for h in range(layers-1, j, -1): bestLayers[h] = bestLayers[h-1]
				bestLayers[j] = checkID
				break

	print(bestLayers)

	for x in range(iW):
		for y in range(iH):
			for i in range(colCountTotal):
				if colRank[x][y][i] in bestLayers:
					displayCols[x][y] = colRank[x][y][i]
					break

	saveColMapImg(outFolder + "displayWack/imageSplit_" + str(len(colIDs)) + ".png", displayCols, colors)
	print("Saved from set with len " + str(len(colIDs)))

	colIDs.remove(bestLayers[0])

# oImg = Image.new("RGB", (len(arr)*100, 100), 0)
# oPix = oImg.load()
# for i in range(len(arr)):
# 	fooCol = arr[i]
# 	xBase = i*100
# 	for x in range(100):
# 		for y in range(100):
# 			oPix[x +xBase,y] = (fooCol[0], fooCol[1], fooCol[2])
# oImg.save(path)
# oImg.close()



# print(displayCols)
# print(colors)

