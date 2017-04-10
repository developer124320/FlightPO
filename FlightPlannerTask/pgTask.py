

f = file("D:/obstacle_ESSA_-_Copy.csv")
myList = []

for line in f:

    myList.append(line)

print(myList)
f.close()