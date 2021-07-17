#Quickly request input files to transfer to dir
#Used to get initial image and color files

import os, sys
import subprocess as sp

def moveInputFile(extension, checkDirs, placeFile):
	#Load input Image
	inPath = ""

	#Find any image files in directory
	imgPaths = []
	for fooDir in checkDirs:
		# print(fooDir)
		for file in os.listdir(fooDir):
			# print("   " + file)
			if file.endswith(extension):
				imgPaths.append(fooDir + '/' + file)

	if len(imgPaths) == 0:
		print("No files Found")
		sys.exit()
	else:
		print("Files found:")
		for i in range(len(imgPaths)):
			print(str(i).ljust(4, " ") + imgPaths[i])
		index = int(input("Select Index:"))
		inPath = imgPaths[index]

	sp.run(["cp", inPath, placeFile])



def newDir(filePath, checkErr = False):
	if not os.path.exists(filePath):
		os.mkdir(filePath)
		return(True)
	elif checkErr:
		input("Error: Output Folder " + filePath + " already exists. Continue?")
		return(False)