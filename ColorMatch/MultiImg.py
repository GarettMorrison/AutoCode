#! /usr/bin/python3
import math as m
import os
import sys
import subprocess as sp
import pty
import time
import re

sys.path.append('pyCommon')
from getInputFile import moveInputFile, newDir

timeOut = 1200

printFreq = 2

#Convert all to png and resize using prepImage.sh
procSet = []
for file in os.listdir("ImgMass"):
	if file.endswith(".jpg"):
		procSet.append(sp.Popen(["func/prepImage.sh", "./ImgMass/"+file]))

startTime = time.time()
while len(procSet) > 0:
	i = 0
	while i < len(procSet):
		if procSet[i].poll() is not None: #If job has finished
			del procSet[i]
		else:	#Not done
			i += 1
	print(str(len(procSet)) + " prepImage procs remaining")
	time.sleep(0.5)


fileSet = []

for file in os.listdir("ImgMass"):
	# print("   " + file)
	if file.endswith(".png") and "matched" not in file:
		fileSet.append(file)

# print(fileSet)
writeF = open("log_dump/multImgDump.txt", "w")


newDir("out/ImgMass")
sp.run("rm out/ImgMass/* -rf".split())

folders =  os.listdir("out/ImgMass")

i = 0
while i < len(fileSet):
	if fileSet[i][:-4] in folders:
		fileSet.pop(i)
	else:
		i +=1

	
for i in fileSet: print(i)

commandSet = ["cpp", "im", "rmim", "rmi", "kill"]

procSet = []
procNames = []
for file in fileSet:
	comm = ["python3", "manager.py"]
	comm = comm + ["ImgMass/"+file[:-4], "ImgMass/"+file, "colors.txt"]
	comm = comm + commandSet
	proc = sp.Popen(comm, stdout = writeF, stderr = sp.STDOUT)
	procSet.append(proc)
	procNames.append(file[:-4])



startTime = time.time()
lastTime = time.time()
while len(procSet) > 0:
	i = 0
	while i < len(procSet):
		if procSet[i].poll() is not None: #If job has finished
			sp.run(["cp", "out/ImgMass/"+procNames[i]+"/matched.png", "ImgMass/"+procNames[i]+"_matched.png"])
			# sp.run(["cp", "out/ImgMass/"+procNames[i]+"/split.png", "ImgMass/"+procNames[i]+"_outputLayers.png"])
			del procSet[i]
			del procNames[i]
		else:	#Not done
			i += 1
	time.sleep(0.1)


	currTime = time.time()

	if currTime - lastTime > printFreq:
		lastTime = currTime

		procCommMap = []
		for i in range(len(commandSet)):
			procCommMap.append([])

		for fooProc in procNames: #Read last tag used
			readFoo = open("out/ImgMass/" + fooProc + "/dat/tags.txt", 'r')
			lastTag = ""
			for lastTag in readFoo: pass

			procCommMap[commandSet.index(lastTag[:-1])].append([fooProc])
			readFoo.close()

			# print(f"Tag:{lastTag[:-1]}")
			# print(f"Index: {commandSet.index(lastTag[:-1])}")
			# print(f"FooProc: {fooProc}")

		# maxInd = -1
		# maxLen = 0
		# for i in range(len(commandSet)):
		# 	if len(procCommMap[i]) > maxLen:
		# 		maxLen = len(procCommMap[i])
		# 		maxInd = i

		# printStrs = []
		# for i in range(maxLen + 1): printStrs.append("")

		# for i in range(len(commandSet)):




		print("Working on:")
		for i in range(1, len(commandSet)):
			print(f"{commandSet[i]}--------")
			for fooPrint in procCommMap[i -1]:
				print(f"   {fooPrint[0]}")

		# print(procCommMap)

		print(str(len(procSet)) + " procs remaining")
		print("")


	if currTime - startTime > timeOut:
		print("Timeout")
		while len(procSet) > 0:
			print("Killing:" + str(procSet[0].pid))
			sp.Popen.kill(procSet[0])
			procSet.pop(0)

print("All Done")