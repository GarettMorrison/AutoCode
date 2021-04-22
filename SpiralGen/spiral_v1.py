import ezdxf
import math
import os
import random

def cos(inputVal):
	return(math.cos(math.radians(inputVal)))

def sin(inputVal):
	return(math.sin(math.radians(inputVal)))

# print(cos(400))

doc = ezdxf.new(setup=True)
msp = doc.modelspace()

doc.layers.new(name='Inner', dxfattribs={'linetype': 'CONTINUOUS', 'color': 2})
doc.layers.new(name='Outer', dxfattribs={'linetype': 'CONTINUOUS', 'color': 1})
doc.layers.new(name='Fill', dxfattribs={'linetype': 'CONTINUOUS', 'color': 3})


lineLen = 1
widthInit = 700
curve = 1

width = widthInit
ang = 0
pNew = (0, 0)
pOld = (0,0)
pExLast = (0,0)
pExOld = (0,0)
pExNew = (0,0)

for i in range(1000):
	pOld = pNew
	pNew = (pOld[0] + lineLen*cos(ang), pOld[1] + lineLen*sin(ang))

	pExOld = pExNew
	# pExOld = (pOld[0] + width*cos(ang -90 - curve/2), pOld[1] + width*sin(ang -90 - curve/2))
	pExNew = (pNew[0] + width*cos(ang -90 + curve/2), pNew[1] + width*sin(ang -90 + curve/2))

	msp.add_line(pOld, pNew, dxfattribs={'layer': 'Inner'})
	msp.add_line(pExOld, pExNew, dxfattribs={'layer': 'Outer'})
	msp.add_line(pNew, pExNew, dxfattribs={'layer': 'Fill'})

	ang += curve
	lineLen += 0.04
	# width = (widthInit/2.5)*(sin((i*3)^2) + 1.5) * (11000-i)/11000








outString = "test_"
i = 0
while  os.path.exists(outString + str(i) + ".dxf"):
	i+=1

doc.saveas(outString + str(i) + ".dxf")