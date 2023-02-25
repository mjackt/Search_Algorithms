def coordString(x,y):
    return  str(x) +","+str(y)

def mazeToDict(filename):
    #Each row is an array so accesing means you need to flip coords.
    # i.e [y][x]
    Coord2DArray = []
    file = open(filename,mode="r")
    for line in file:
        Coord2DArray.append(line.split())
    #Now we have a full 2D array of coords

    file.close()
    dictionary = {}
    
    for y in range(0,len(Coord2DArray)):
        for x in range(0,len(Coord2DArray[y])):
            if Coord2DArray[y][x] == "-":
                dictionary[coordString(x,y)] = []

                #multiple ifs prevent accessing errors
                #above
                if y>0:
                    if Coord2DArray[y-1][x]=="-":
                        dictionary[coordString(x,y)].append(coordString(x,y-1))
                #below
                if y<len(Coord2DArray)-1:
                    if Coord2DArray[y+1][x]=="-":
                        dictionary[coordString(x,y)].append(coordString(x,y+1))
                #left
                if x>0:
                    if Coord2DArray[y][x-1]=="-":
                        dictionary[coordString(x,y)].append(coordString(x-1,y))
                #right
                if x<len(Coord2DArray[y])-1:
                    if Coord2DArray[y][x+1]=="-":
                        dictionary[coordString(x,y)].append(coordString(x+1,y))

    return dictionary