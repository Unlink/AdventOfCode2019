import math

def findNodes(map):
    entranceCounter = 0
    keys = dict()
    for i, row in enumerate(map):
        for j, c in enumerate(row):
            if c == "@":
                c = str(entranceCounter)
                map[i][j] = c
                entranceCounter += 1
                keys[c] = (i,j)
            elif c.islower() or c.isupper():
                keys[c] = (i,j)
    return keys

def getNextDirections(map, position):
    directions = [(0,-1),(0,1),(-1,0),(1,0)]
    for i, dir in enumerate(directions):
        nextPosition = (position[0]+dir[0], position[1]+dir[1])
        if not(map[nextPosition[0]][nextPosition[1]] == "#"):
            yield nextPosition

def findKeys(graf, currentPositions, actualPath = "", keys = set(), cache = dict()):    
    missingKeys = frozenset([x for x in graf.keys() if x.islower() and not(x in keys)])
    cacheKey = (frozenset(currentPositions), missingKeys)
    if (cacheKey in cache):
        return cache[cacheKey]
    
    minForStep = math.inf
    for node in currentPositions:
        visited = dict()
        visited[node] = 0
        stack = [(node, 0)]
        found = dict()
        #Look for all accesible keys
        while len(stack) > 0:
            currentNode, currentNodeDistance = stack.pop()
            # print(graf[currentNode])
            for c,distance in graf[currentNode].items():
                if not(c in visited) or visited[c] > currentNodeDistance + distance:
                    visited[c] = currentNodeDistance + distance
                    if (c.islower() and c in keys) or (c.isupper() and c.lower() in keys): #doors are open
                        stack.append((c, currentNodeDistance + distance))
                    if c.islower() and not(c in keys) and (not(c in found) or found[c] > currentNodeDistance + distance):
                        found[c] = currentNodeDistance + distance
        
        # print(node+" -> "+str(found))
        # input()
        #print(actualPath)
        if len(found) == 0:
            minForStep = min(minForStep, 0 if len(missingKeys) == 0 else math.inf)
            continue

        items = list(found.items())
        sorted(items, key=lambda x: x[1] )
        minimum = math.inf
        for k,v in items:
            newPositions = set(currentPositions)
            newPositions.remove(node)
            newPositions.add(k)
            value = findKeys(graf, newPositions, actualPath+k, set(list(keys)+[k]), cache) + v
            
            minimum = min(minimum, value)
        
        minForStep = min(minForStep, minimum)
    
    cache[cacheKey] = minForStep
    return minForStep
    
with open("input.txt") as f:
    map = [[c for c in x.strip()] for x in f]
    
    keys = findNodes(map)
    #Part2
    i,j = keys["0"]
    map[i-1][j-1] = "@"
    map[i-1][j] = "#"
    map[i-1][j+1] = "@"
    map[i][j-1] = "#"
    map[i][j] = "#"
    map[i][j+1] = "#"
    map[i+1][j-1] = "@"
    map[i+1][j] = "#"
    map[i+1][j+1] = "@"
    keys = findNodes(map)
    
    
    graf = dict()    
    for k,position in keys.items():
        #print("lookup for: "+k)
        visited = dict()
        visited[position] = 0
        stack = [position]
        found = dict()
        
        while len(stack) > 0:
            currentPos = stack.pop()
            currentSize = visited[currentPos]
            
            for pos in getNextDirections(map, currentPos):
                c = map[pos[0]][pos[1]]
                if c == "." or c.isdigit():
                    if not(pos in visited) or visited[pos] > currentSize+1:
                        visited[pos] = currentSize+1
                        stack.append(pos)
                if (c.islower() or c.isupper() or c.isdigit()):
                    if not(c in found) or found[c] > currentSize+1:
                        found[c] = currentSize+1
        
        graf[k] = found
    #print(keys["0"])
    entrances = set([k for k in keys.keys() if k.isdigit()])
    print(findKeys(graf, entrances))