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


widthInit = 5
cycle = 15

width = widthInit
ang = 0
pNew = (0, 0)
pOld = (0,0)
pExLast = (0,0)
pExOld = (0,0)
pExNew = (0,0)


for i in range(2000):
	theta = 1 * i
	r =  widthInit*i/360

	pOld = pNew
	pNew = (r*cos(theta), r*sin(theta))

	pExOld = pExNew

	r2 = r + 1/3 * widthInit

	r2 += 2/3 * widthInit * (abs(cycle/2-(i%cycle))) * 2/cycle

	pExNew = ((r2)*cos(theta), (r2)*sin(theta))

	msp.add_line(pOld, pNew, dxfattribs={'layer': 'Inner'})
	msp.add_line(pExOld, pExNew, dxfattribs={'layer': 'Outer'})
	msp.add_line(pNew, pExNew, dxfattribs={'layer': 'Fill'})

	








outString = "test_"
i = 0
while  os.path.exists(outString + str(i) + ".dxf"):
	i+=1

doc.saveas(outString + str(i) + ".dxf")