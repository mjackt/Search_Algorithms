#takes array returns index with a dash
def findDash(line):
    for i in range(0,len(line)):
        if line[i] == "-":
            return i

def depthFirst(graph,start,goal):
    visited = []
    route =[]
    stack = [start]
    while(len(stack) != 0):
        current = stack.pop()
        if current not in route:
            route.append(current)
        
        if current not in visited:
            newDiscover = False
            for neighbour in graph[current]:
                stack.append(neighbour)
                if neighbour not in visited:
                    newDiscover = True

                if neighbour == goal:
                    route.append(goal)
                    return route
            
            #if newDiscover is true it means that a new node has been found meaning the search hasnt reached a dead end.
            #if newDisover is false a dead end has been reached and it must begin 'backtracking'
            if (newDiscover==False):
                route.pop()

            visited.append(current)

        #checking whether the search is currently 'backtracking' through nodes already fully visited or if the search has discovered a cycle
        #if it is then the current node shouldn't be part of the route

        else:
            remove = True
            for neighbour in graph[current]:
                if neighbour not in visited:
                    remove = False

            if(remove):
                route.pop()
        
    return "nope"

def coordString(x,y):
    return  str(x) +","+str(y)

#returns tuple containing a dictionary, and coords of start and end
def mazeToDict(filename):
    #Each row is an array so accesing means you need to flip coords.
    # i.e [y][x]
    Coord2DArray = []
    file = open(filename,mode="r")
    for line in file:
        Coord2DArray.append(line.split())
    #Now we have a full 2D array of coords
    startx = findDash(Coord2DArray[0])
    start = coordString(startx,0)

    goalx = findDash(Coord2DArray[-1])
    goal = coordString(goalx,len(Coord2DArray)-1)

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
    return (dictionary,start,goal)

graph,start,goal = mazeToDict("maze-Large.txt")
print(depthFirst(graph,start,goal))