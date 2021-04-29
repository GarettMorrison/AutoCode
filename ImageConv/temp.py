import ezdxf
from PIL import Image
import math
import os
import sys
import random as r
import time


n = 100

arr = [0,]*n

for i in range(10000):
	m = i
	while m >= n:
		m -= n
	arr[m] += 1

maxVal = 0
for i in arr:
	if i > maxVal:
		maxVal = i

for i in range(len(arr)):
	print(str(i), end=" ")
	for j in range(math.floor(20 * arr[i]/maxVal)):
		print("+", end = "")
	print("")
