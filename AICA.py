from time import process_time
import math
import glob

#takes array returns index with a dash
def findDash(line):
    for i in range(0,len(line)):
        if line[i] == "-":
            return i

#Takes a graph in the form of a dictionary as created by mazeToDict
def depthFirstSearch(graph,start,goal):
    explored = 0
    visited = set()
    #The stack stores tuples containg the nodes that need to be visted and the path that got to said node
    #This eliminates need for having checks to remove nodes from path when backtracking which was slowing it down massively

    #i.e a stack value for node G could be ('G',['A','D','E','G'])
    stack = [(start, [start])]

    while len(stack) != 0:
        explored += 1
        (current, route) = stack.pop()
        if current not in visited:
            if current == goal:
                return (route,explored)
            visited.add(current)
            for neighbor in graph[current]:
                stack.append((neighbor, route + [neighbor]))
    #if the stack becomes empty every accesible node has been visited and no path has been found
    return None

def greedySearch(graph,start,goal):
    explored = 0
    visited = set()

    #toLook will be a list sorted by distance to the goal node.
    #the node with smallest distance to goal will be picked first
    #initial start distance is irrelavant hence the 10**9
    toLook = [(start, [start], 10**9)]

    while len(toLook) != 0:
        explored += 1
        #takes first element which will always be smallest distance
        (current, route, n) = toLook.pop(0)
        if current not in visited:
            if current == goal:
                return (route,explored)
            visited.add(current)
            for neighbor in graph[current]:
                absx = abs(goal[0]-current[0])
                absy = abs(goal[1]-current[1])
                distance = absx + absy

                toLook = insertToListOfTuples(toLook,(neighbor, route + [neighbor],distance))
                                     
    #if toLook becomes empty every accesible node has been visited and no path has been found
    return None

#takes tuples with (any,any,int) and sorts by int value
def insertToListOfTuples(list,insertion):
    for i in range(0,len(list)):
        if insertion[2]<list[i][2]:
            list.insert(i,insertion)
            return list
        
    if len(list)==0:
        list.insert(0,insertion)
        return list
    
    list.append(insertion)
    return list
        

#returns tuple containing a dictionary, and coords of start and end
#dictionary uses a key for every position that has a - in the maze
#each key's value is an array of accessible neighbours
def mazeToDict(filename):
    #Each row is an array so accesing means you need to flip coords.
    # i.e [y][x]
    Coord2DArray = []
    file = open(filename,mode="r")
    for line in file:
        Coord2DArray.append(line.split())
    #Now we have a full 2D array of coords
    startx = findDash(Coord2DArray[0])
    start = (startx,0)

    goalx = findDash(Coord2DArray[-1])
    goal = (goalx,len(Coord2DArray)-1)

    file.close()
    dictionary = {}
    
    for y in range(0,len(Coord2DArray)):
        for x in range(0,len(Coord2DArray[y])):
            if Coord2DArray[y][x] == "-":
                dictionary[(x,y)] = []

                #multiple ifs prevent accessing errors
                #above
                if y>0:
                    if Coord2DArray[y-1][x]=="-":
                        dictionary[(x,y)].append((x,y-1))
                #below
                if y<len(Coord2DArray)-1:
                    if Coord2DArray[y+1][x]=="-":
                        dictionary[(x,y)].append((x,y+1))
                #left
                if x>0:
                    if Coord2DArray[y][x-1]=="-":
                        dictionary[(x,y)].append((x-1,y))
                #right
                if x<len(Coord2DArray[y])-1:
                    if Coord2DArray[y][x+1]=="-":
                        dictionary[(x,y)].append((x+1,y))
    return (dictionary,start,goal)

#path is the result from the search
#origin maze is the original .txt file
def outputMaze(path,originMaze,outFile):
    file = open(originMaze)

    #is a 2D array where each array is a line - access backwards i.e [y][x] not [x][y]
    rows = []
    for line in file:
        chars = line.split()
        rows.append(chars)
    for i in range(0,len(path)):
        currentx = path[i][0]
        currenty = path[i][1]
        rows[currenty][currentx] ="?"
    #writing to .txt section
    searchResult = open("results/"+outFile[5:],'w')
    #taking each row of characters and converting back to one string seperated by spaces
    for line in rows:
        line = ' '.join(line)
        line = line + "\n"
        searchResult.write(line)
    #now rows is just a list of strings
    searchResult.close()

def main():
    maze=(input("Place all mazes in the mazes folder\nThey must be of .txt format\nWhen this is done press enter\n"))
    foundMazes=[]
    for name in glob.glob('mazes/*.txt'):
        foundMazes.append(name)
    
    for maze in foundMazes:
        graph,start,goal = mazeToDict(maze)

        startTime = process_time() 
        depthResult = depthFirstSearch(graph,start,goal)
        endTime = process_time()
        depthTime = endTime-startTime
        outputMaze(depthResult[0],maze,maze+"_DFS_RESULT.txt")

        startTime = process_time()
        greedyResult = greedySearch(graph,start,goal)
        endTime = process_time()
        greedyTime = endTime-startTime
        outputMaze(greedyResult[0],maze,maze+"_GREEDY_RESULT.txt")

        print("\n----"+maze+"----\n")
        print("####Depth First Search####\nStatistics:\nNodes explored: "+str(depthResult[1])+"\nTime taken: "+str(depthTime)+"\nPath length: "+str(len(depthResult[0]))+"\n\n")
        print("####Greedy Search####\nStatistics:\nNodes explored: "+str(greedyResult[1])+"\nTime taken: "+str(greedyTime)+"\nPath length: "+str(len(greedyResult[0]))+"\n")
if __name__ == "__main__":
    main()