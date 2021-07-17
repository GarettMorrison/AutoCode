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


procSet = []
procNames = []
for file in fileSet:
	comm = ["python3", "manager.py"]
	comm = comm + ["ImgMass/"+file[:-4], "ImgMass/"+file, "colors.txt"]
	comm = comm + ["cpp", "im", "rmim", "rmi", "kill"]
	proc = sp.Popen(comm, stdout = writeF, stderr = sp.STDOUT)
	procSet.append(proc)
	procNames.append(file[:-4])



startTime = time.time()
while len(procSet) > 0:
	i = 0
	while i < len(procSet):
		if procSet[i].poll() is not None: #If job has finished
			sp.run(["cp", "out/ImgMass/"+procNames[i]+"/matched.png", "ImgMass/"+procNames[i]+"_matched.png"])
			del procSet[i]
			del procNames[i]
		else:	#Not done
			i += 1
	print(str(len(procSet)) + " procs remaining")
	time.sleep(1)

	currTime = time.time()
	if currTime - startTime > timeOut:
		print("Timeout")
		while len(procSet) > 0:
			print("Killing:" + str(procSet[0].pid))
			sp.Popen.kill(procSet[0])
			procSet.pop(0)

print("All Done")