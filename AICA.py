#used to measure process time
from time import process_time
#used to find files
import glob

#takes array of characters -> returns index with a '-'
def findDash(line):
    for i in range(0,len(line)):
        if line[i] == "-":
            return i

#Takes a graph in the form of a dictionary as created by mazeToDict as well as the start and goal nodes
#Returns the path and number of nodes explored, both in a tuple
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
            #Every discovered neighbour goes to the top of the stack
            for neighbor in graph[current]:
                stack.append((neighbor, route + [neighbor]))
    #if the stack becomes empty every, accesible node has been visited and no path has been found
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
        #pops first element which will always have the smallest estimate distance
        (current, route, n) = toLook.pop(0)
        if current not in visited:
            if current == goal:
                return (route,explored)
            visited.add(current)
            for neighbor in graph[current]:
                #absx and absy are the absolute values of the differnce in x and y values between the current and goal nodes
                absx = abs(goal[0]-current[0])
                absy = abs(goal[1]-current[1])
                distance = absx + absy

                #inserting discovered node into toLook using the estimate distance as a sorting key
                toLook = insertToListOfTuples(toLook,(neighbor, route + [neighbor],distance))
                                     
    #if toLook becomes empty every accesible node has been visited and no path has been found
    return None

#takes a sorted list of tuples with type(any,any,int) and and a tuple of the same type to insert
#returns the list with the tuple inserted
def insertToListOfTuples(list,insertion):
    #iterating up the list until a value bigger than the insert value is found. Same as any standard insertion algrotithm
    for i in range(0,len(list)):
        if insertion[2]<list[i][2]:
            list.insert(i,insertion)
            return list
        
    if len(list)==0:
        list.insert(0,insertion)
        return list
    
    #if this point is reached it means the insert tuple has the largest value so must be appended
    list.append(insertion)
    return list
        
#takes a filename for a relevant maze
#returns tuple containing a dictionary, and coords of start and end
#dictionary uses a key for every position that has a - in the maze
#each key's value is an array of accessible neighbours
#Example:
#[3,2] : [[3,3],[4,2]] 
def mazeToDict(filename):
    #Each row is an array so accesing means you need to flip coords.
    # i.e [y][x]
    Coord2DArray = []
    file = open(filename,mode="r")
    for line in file:
        Coord2DArray.append(line.split())
    #Now we have a full 2D array of coords

    #Creating start and goal coords using findDash()
    startx = findDash(Coord2DArray[0])
    start = (startx,0)

    goalx = findDash(Coord2DArray[-1])
    goal = (goalx,len(Coord2DArray)-1)

    file.close()
    dictionary = {}
    
    for y in range(0,len(Coord2DArray)):
        for x in range(0,len(Coord2DArray[y])):
            #If a dash is found it is added to the dictionary
            if Coord2DArray[y][x] == "-":
                #The next step is adding all of it's neighbours as values to the key in the dictionary.
                dictionary[(x,y)] = []

                #multiple ifs prevent accessing errors. don't touch
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

            #if to detect invalid file formats
            if Coord2DArray[y][x] not in ["-","#"," "]:
                raise Exception()
    return (dictionary,start,goal)

#path is the result from the search
#origin maze is the original .txt file
#outFile is the desired output file name
#nothing is returned
def outputMaze(path,originMaze,outFile):
    file = open(originMaze)

    #rows is a 2D array where each array is a line - access backwards i.e [y][x] not [x][y]
    rows = []
    #splits each line into array of characters excluding spaces and adds it to rows
    for line in file:
        chars = line.split()
        rows.append(chars)
    #goes through path and updates every path coord to a ? in the text representation of the maze
    for i in range(0,len(path)):
        currentx = path[i][0]
        currenty = path[i][1]
        rows[currenty][currentx] ="?"


    searchResult = open("results/"+outFile[6:],'w')
    #taking each row of characters and converting back to one string seperated by spaces
    for line in rows:
        line = ' '.join(line)
        line = line + "\n"
        searchResult.write(line)
    #now rows is just a list of strings
    searchResult.close()

def main():
    maze=(input("Place all mazes in the mazes folder\nThey must be of .txt format\nPlease also ensure there is an accompaning folder called results\nWhen this is done press enter\n"))
    foundMazes=[]
    for name in glob.glob('mazes/*.txt'):
        foundMazes.append(name)
    
    for maze in foundMazes:
        try:
            graph,start,goal = mazeToDict(maze)
        except:
            print("Seems like there was an issue with "+maze[6:]+"\nIt could be an invalid filename or the structure of the maze isn't recognised\n")
            continue
        
        #if any exceptions get raised it will continue with the next maze
        try:
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

        except Exception as e:
            print(e)
            continue

    print("All done.\nTo see your solutions head to the results folder")
        
if __name__ == "__main__":
    main()