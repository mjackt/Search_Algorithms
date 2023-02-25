underground = {
    'Bond Street': ['Oxford Circus', 'Green Park'],
    'Oxford Circus': ['Bond Street', 'Green Park', 'Tottenham Court Road', 'Piccadilly Circus'],
    'Tottenham Court Road': ['Oxford Circus', 'Leicester Square'],
    'Green Park' : ['Bond Street', 'Oxford Circus', 'Piccadilly Circus', 'Charing Cross'],
    'Piccadilly Circus': ['Green Park', 'Oxford Circus', 'Leicester Square', 'Charing Cross'],
    'Leicester Square': ['Piccadilly Circus', 'Tottenham Court Road', 'Charing Cross'],
    'Charing Cross': ['Green Park', 'Piccadilly Circus', 'Leicester Square']}

leGraph ={
    'A': ['C'],
    'B': ['C','D'],
    'C': ['B','F','E'],
    'D': ['F','B'],
    'E': ['C','G','H'],
    'F': ['C','D'],
    'G': ['E','I'],
    'H': ['E','I'],
    'I': ['H','G']
}

def depthFirst(graph,start,goal):
    visited = []
    route =[]
    stack = [start]
    while(len(stack) != 0):
        current = stack.pop()
        print("exploring: "+current)
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

print(depthFirst(leGraph,'A','D'))