import ezdxf
import math as m
import os
import random

def cos(inputVal):
	return(m.cos(m.radians(inputVal)))

def sin(inputVal):
	return(m.sin(m.radians(inputVal)))

# print(cos(400))

doc = ezdxf.new(setup=True)
msp = doc.modelspace()

doc.layers.new(name='Inner', dxfattribs={'linetype': 'CONTINUOUS', 'color': 2})
doc.layers.new(name='Outer', dxfattribs={'linetype': 'CONTINUOUS', 'color': 1})
doc.layers.new(name='Fill', dxfattribs={'linetype': 'CONTINUOUS', 'color': 3})


widthInit = 5
cycle = 15

width = widthInit
r =  widthInit

ang = 0
pNew = (0, 0)
pOld = (0,0)
pExLast = (0,0)
pExOld = (0,0)
pExNew = (0,0)




for j in range(360):
	print(j)
	xCent = (j%19)*widthInit*2.1
	yCent = m.floor(j/19)*widthInit*2.1
	
	pNew = (xCent + widthInit, yCent)
	for i in range(361):
		theta = i*j

		pOld = pNew

		# print(str((j%60)*widthInit*2.1) + ' - ' + str(m.floor(j/60)*widthInit*2.1))

		pNew = (r*cos(theta) + xCent, r*sin(theta) + yCent)

		# pExOld = pExNew

		# r2 = r + 1/3 * widthInit

		# r2 += 2/3 * widthInit * (i%cycle+1)/cycle

		# pExNew = ((r2)*cos(theta), (r2)*sin(theta))

		msp.add_line(pOld, pNew, dxfattribs={'layer': 'Outer'})
		# msp.add_line(pExOld, pExNew, dxfattribs={'layer': 'Outer'})
		# msp.add_line(pNew, pExNew, dxfattribs={'layer': 'Fill'})

	








outString = "out/test_"
i = 0
while  os.path.exists(outString + str(i) + ".dxf"):
	i+=1
print("A")

doc.saveas(outString + str(i) + ".dxf")
print("a")