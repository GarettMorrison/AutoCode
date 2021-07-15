import os
import sys
import subprocess as sp

#TAGS
#shortHand cpp
#reqTags
#locks
#desc make /cpp and copy over the executables


outFolder = sys.argv[1]

#Copy c++ files
print("Copying files")
sp.run(["make", "-C", "cpp"])

files = os.walk("./cpp/o")
for i in next(files)[2]:
	# print(i)
	sp.run(["cp","./cpp/o/"+i, outFolder+"bin/"])