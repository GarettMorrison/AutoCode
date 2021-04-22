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


widthStart = 3
widthEnd = 5

expandConst = 1.6

ticks = 720
degPerTick = 2


ang = 0
pNew = (0, 0)
pOld = (0,0)
pExLast = (0,0)
pExOld = (0,0)
pExNew = (0,0)

ri = widthStart
pNew = (ri * cos(ang), ri * sin(ang))
pExNew = pNew

tickPerCirc = m.floor(360/degPerTick)
for i in range(tickPerCirc, ticks+tickPerCirc):
	ang = i*degPerTick
	iLast = i - tickPerCirc
	print(i/tickPerCirc)
	r1 = pow(expandConst,(iLast/tickPerCirc))    #+ (widthEnd - widthStart)*((ang-360)/ticks + widthStart)
	
	r2 = pow(expandConst,(i/tickPerCirc))

	# r2 = (r2-r1)*(4/5+sin(ang*2.5432)/8 + sin(ang*8.132)/15 ) + r1    #+ (widthEnd - widthStart)*((ang)/ticks    + widthStart)-0.5
	
	r2 = (r2-r1)*(0.49 + abs(sin(ang*9.5412)/2)) + r1
	# print(ri)


	pOld = pNew
	pNew = (r1 * cos(ang), r1 * sin(ang))

	pExOld = pExNew
	pExNew = ((r2)*cos(ang), (r2)*sin(ang))
	# r2 = r + 1/3 * widthInit

	# r2 += 2/3 * widthInit * (i%cycle+1)/cycle


	msp.add_line(pOld, pNew, dxfattribs={'layer': 'Inner'})
	msp.add_line(pExOld, pExNew, dxfattribs={'layer': 'Outer'})
	msp.add_line(pNew, pExNew, dxfattribs={'layer': 'Fill'})

	








outString = "out/test_"
i = 0
while  os.path.exists(outString + str(i) + ".dxf"):
	i+=1
print("A")

doc.saveas(outString + str(i) + ".dxf")
print("a")