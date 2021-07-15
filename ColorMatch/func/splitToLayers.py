from PIL import Image
import math as m
import os
import sys
import subprocess as sp

sys.path.append('pyCommon')
from bin_customLib import newBinArr, saveBinArr, loadBinArr
from getInputFile import newDir
from makeImg import saveColMapImg, savePixImg

#TAGS
#shortHand stl
#reqTags cpp im
#locks matched
#desc WIP Remove small areas from image


outFolder = sys.argv[1]

newDir(outFolder + "bin/layers/")
sp.run(["./splitLayers.o", "colMap.bin", "layers/"], cwd=outFolder +"bin/")


# in1 = loadBinArr(outFolder + "bin/layers/l1.bin")

# cols = loadBinArr(outFolder + "dat/cols/")

# saveColMapImg(path, colMap, colors)

print("DONE")