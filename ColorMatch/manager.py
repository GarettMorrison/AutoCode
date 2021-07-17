#! /usr/bin/python3
import math as m
import os
import sys
import subprocess as sp
import pty
import time
import re

from pyCommon.getInputFile import moveInputFile, newDir

#Get name of new folder
outFolder = ""
try:
	outFolder = sys.argv[1]
except:
	outFolder = input("Enter a name for the folder to save in:")
outFolder = "out/" + outFolder + '/' 

isNewProject = newDir(outFolder, True)
newDir(outFolder + "bin")
newDir(outFolder + "dat")

# print(isNewProject)

if isNewProject:
	print("Selecting input image:")
	if len(sys.argv) > 2:
		if os.path.exists(sys.argv[2]):
			sp.run(["cp", sys.argv[2], outFolder + "original.png"])
		else:
			print("Image path |" + sys.argv[2] +  "| does not exist")
			sys.exit()
	else:
		moveInputFile(".png", [".","./img"], outFolder + "original.png")



	print("Selecting input colors:")
	if len(sys.argv) > 3:
		if os.path.exists(sys.argv[3]):
			sp.run(["cp", sys.argv[3], outFolder + "dat/colors.txt"])
		else:
			print("File path |" + sys.argv[3] +  "| does not exist")
			sys.exit()
	else:
		moveInputFile(".txt", [".","./col"], outFolder + "dat/colors.txt")





print("Clearing log folder")
for file in os.listdir("log_dump"):
	os.remove("log_dump/" + file)

print("Initializing pyFiles")

#Class is used to manage tags to run scripts in func
class pyFile():
	name = ""
	filePath = ""
	shortHand = ""
	reqTags = []	#tags required to start script
	locks = []		#tags that there can only be one of at a time
	description = ""


	def printData(self):
		print("name: " + self.name)
		print("   filePath: " + self.filePath)
		print("   shortHand:" + self.shortHand)

		print("   reqTags:", end = "")
		for i in self.reqTags: print(" " + i, end = '')
		print("\n   locks:", end = "")
		for i in self.locks: print(" " + i, end = '')
		print("\n   desc: " + self.description + '\n')


	def __init__(self, _filePath):
		self.filePath = _filePath
		self.name = _filePath.split('/')[-1][:-3]
		#Open file for reading to find #TAGS
		readTags = open(_filePath, 'r')
		#Read until hit #TAGS
		while True:
			line =  readTags.readline()
			# print(line)
			if not line: #End of file and no #TAGS
				print("Error Opening " + self.filePath + ": no #TAGS found")
				sys.exit()
			# line.replace('\n', '')
			if line == "#TAGS\n":
				break

		#Actually read tags
		self.shortHand  = readTags.readline().replace('\n', '').split(' ')[1]
		self.reqTags  = readTags.readline().replace('\n', '').split(' ')[1:]
		self.locks    = readTags.readline().replace('\n', '').split(' ')[1:]
		self.description = ' '.join(readTags.readline().replace('\n', '').split(' ')[1:])

		self.printData()
		readTags.close()


pyFiles = []
pyFileIndex = 0

files = os.walk("./func")
for fooScript in next(files)[2]:
	if fooScript[-3:] != ".py":
		continue

	pyFiles.append(pyFile("func/" + fooScript))
	pyFileIndex += 1
#Done with scripts, all loaded



class job:
	def __init__(self, _pyFile, args, _procID):
		self.file = _pyFile
		self.procID = _procID
		self.title = str(self.procID) + '_' + self.file.name

		#Job is good to add
		self.master, self.slave = pty.openpty()
		self.read = os.fdopen(self.master, 'r')

		self.write = open("log_dump/" + self.title + ".txt", "w")

		self.proc = sp.Popen(["python3", self.file.filePath] + args, stdout = self.write, stderr = sp.STDOUT)
		# print("PROC INIT ==============")

	def __del__(self):
		# print("PROC Shutdown ==============")

		self.write.close()

		# self.read.close()
		# os.close(self.master)
		# os.close(self.slave)

		if self.proc is not None:
			self.proc.kill()

# class queuedJob:
# 	def __init__(self, _file, inArgs):
# 		self.file = _pyFile
# 		self.args = inArgs

killWhenDone = False
inStr = ""
for i in range(4, len(sys.argv)):
	if sys.argv[i] == "kill": killWhenDone = True
	inStr = inStr + ' ' + sys.argv[i]


#Jobs to be ran
runQueue = []		#listed by index in pyFiles
strQueue = []



#Current jobs
curr_jobs = []		#list of job instances

#Currently applied tags
curr_locks = []		#tags that there can only be one of at a time
curr_doneTags = []	#tags to add when done

#Init procID as 0
nextProcID = 0

print("-------------" + inStr)

if not isNewProject:
	tagLoad = open(outFolder + "dat/tags.txt", 'r')
	for i in tagLoad:
		print(i)
		if i != '':
			curr_doneTags.append(i[:-1])
	print(curr_doneTags)
	tagLoad.close()


tagSave = open(outFolder + "dat/tags.txt", 'w+')

while True:
	if inStr == "": 
		if killWhenDone: sys.exit()
		inStr = input("CM:")

	inComms = inStr.split(' ')
	print("inComms: " + str(inComms))
	if '' in inComms: inComms.remove('')
	for fooComm in inComms:
		if fooComm in {"kill", "KILL","wait", "WAIT"}:
			print("Queue Comm: " + fooComm)
			runQueue.append(-1)
			strQueue.append(fooComm)
		else:
			for i in range(len(pyFiles)): 
				if fooComm == pyFiles[i].shortHand or fooComm == pyFiles[i].name: 
					print("Queue Func: " + fooComm)
					runQueue.append(i)
					strQueue.append(pyFiles[i].shortHand)

	print(inStr)
	inStr = ""
	printEvery = 4
	printIter = 4

	#Loop until queue is empty
	while len(runQueue) > 0 or len(curr_jobs) > 0:
		#Check current jobs, drop if finished
		curr_locks = []
		i = 0
		while i < len(curr_jobs):
			if curr_jobs[i].proc.poll() is not None: #If job has finished
				curr_doneTags = curr_doneTags + [curr_jobs[i].file.shortHand]
				tagSave.write(curr_jobs[i].file.shortHand + '\n')
				del curr_jobs[i]

			else:	#Not done, save locks
				curr_locks = curr_locks + curr_jobs[i].file.locks
				i += 1

		#init new jobs
		i = 0
		while i < len(runQueue):	#Do not add if lock
			addJob = True
			if runQueue[i] == -1:
				fooComm = strQueue[i]

				if fooComm in {"kill", "KILL"}:
					print("EXITING PROGRAM")
					if len(curr_jobs) > 0:
						break
					else:
						sys.exit()

				elif fooComm in {"wait", "WAIT"}:
					print("WAITING")
					if len(curr_jobs) > 0:
						break
					else:
						runQueue.pop(i)
						strQueue.pop(i)
						addJob = False

			else:
				fooFile = pyFiles[runQueue[i]]
				for foo_lock in fooFile.locks: 
					if foo_lock in curr_locks: 
						print("LOCK")
						addJob = False	

				for foo_reqTag in fooFile.reqTags:	#Do not add if reqtags not met
					if foo_reqTag not in curr_doneTags: 
						print("REQ TAG")
						addJob = False

			
			if not addJob:
				i += 1
				continue
			

			args = [outFolder] #Init arguements, first one is always outFolder

			#Job is good to add
			curr_jobs.append(job(fooFile, args, nextProcID))
			nextProcID += 1
			runQueue.pop(i)
			strQueue.pop(i)
			curr_locks = curr_locks + fooFile.locks


		# for i in range(len(curr_jobs)): #Print output
		# 	line = curr_jobs[i].read.readline()
		# 	if line == '':
		# 			break
		# 	print(curr_jobs[i].file.shortHand + ": " + str(line[:-1]))


		print("\nQ:" + str(len(runQueue)) + " R:" + str(len(curr_jobs)) + " D:" + str(len(curr_doneTags)))
		print("Queued:", end="")
		for i in runQueue: print(" " + pyFiles[i].shortHand, end="")
		print("\nRunning:", end="")
		for i in curr_jobs: print(" " + i.title, end="")
		print("\nCompleted:", end="")
		for i in curr_doneTags: print(" " + str(i), end="")
		print("")

		time.sleep(0.5)



tagSave.close()