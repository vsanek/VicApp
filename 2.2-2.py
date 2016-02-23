from array import *

def clrs2_2_2(n, myList):
	for j in range(0, n-2, 1):
		key = j
		for i in range(j+1, n-1, 1):
			if myList[i] < myList[j]:
				key = i
		if key>j:
			temp = myList[j]
			myList[j] = myList[key]
			myList[key] = temp
	return myList

myArray = array('i',[1,3,2,4,5])
sortedArray = clrs2_2_2(5, myArray)
print (sortedArray)