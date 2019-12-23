import math
from PIL import Image, ImageDraw

def findNodes(map):
    portals = dict()
    for i, row in enumerate(map):
        for j, c in enumerate(row):
            if c == ".":
                for pos in getNextDirections(map, (i,j)):
                    pos = pos[0] #ignore level
                    c = map[pos[0]][pos[1]]
                    if c.isupper():
                        #print("Found upper"+c+" for "+str((i,j))+" on "+str(pos)+ " next pos "+str((pos[0] + (pos[0]-i),pos[1] + (pos[1]-j))))
                        c2 = map[pos[0] + (pos[0]-i)][pos[1] + (pos[1]-j)]
                        if ((pos[0]-i) < 0 or (pos[1]-j) < 0):
                            portal = c2+c
                        else:
                            portal = c+c2
                        if not(portal in portals):
                            portals[portal] = []
                        direction = -1 if pos[0] < 3 or pos[1] < 3 or pos[0] > (len(map)-4) or pos[1] > (len(map[pos[0]])-4) else 1
                        portals[portal].append(((i,j), direction))
    return portals

def getNextDirections(map, position, portals=None, level=0):
    directions = [(0,-1),(0,1),(-1,0),(1,0)]
    for i, dir in enumerate(directions):
        curLevel = level
        nextPosition = (position[0]+dir[0], position[1]+dir[1])
        if nextPosition[0] >= 0 and nextPosition[0] < len(map) and nextPosition[1] >= 0 and nextPosition[1] < len(map[nextPosition[0]]) and not(map[nextPosition[0]][nextPosition[1]] == "#"):
            if (portals != None and map[nextPosition[0]][nextPosition[1]].isupper()):
                for portaList in portals.values():
                    if len(portaList) == 2:
                        if (portaList[0][0] == position):
                            # print("Jumping from "+str(position)+" to "+str(portaList[1]))
                            curLevel += portaList[0][1]
                            nextPosition = portaList[1][0]
                        elif (portaList[1][0] == position):
                            # print("Jumping from "+str(position)+" to "+str(portaList[0]))
                            nextPosition = portaList[0][0]
                            curLevel += portaList[1][1]
            yield (nextPosition, curLevel)
    
with open("input.txt") as f:
    map = [[c for c in x] for x in f]
    
    nodes = findNodes(map)
    for k,v in nodes.items():
        print(str(k)+" -> "+str(v))
    
    start = nodes["AA"][0][0]
    end = nodes["ZZ"][0][0]
    
    position = start
    
    visited = dict()
    visited[(position,0)] = 0
    stack = [(position,0)]
    found = dict()
        
    while len(stack) > 0:
        currentPos, level = stack.pop()
        currentSize = visited[(currentPos, level)]
        # input()
        # print("Visiting "+str(currentPos)+"["+str(level)+"] distance "+str(currentSize))
            
        for next in getNextDirections(map, currentPos, nodes, level):
            # print(next)
            pos, l = next
            c = map[pos[0]][pos[1]]
            if c == ".":
                if next[1] >= 0 and next[1] < 30 and (not(next in visited) or visited[next] > currentSize+1): #max 30 levels
                    visited[next] = currentSize+1
                    stack.append(next)
    
    print(visited[(end, 0)])
    
    w = len(map[0])
    h = len(map)
    for level in range(10):
        size = 40
        img = Image.new('RGB', (w*size, h*size))
        for i in range(len(map)):
            for j,v in enumerate(map[i]):    
                color = 0
                if (v == "#"): 
                    color = (0,0,0)
                elif (v == "A"): 
                    color = (0,255,0)
                elif (v == "Z"): 
                    color = (255,0,0)
                elif (v.isupper()): 
                    color = (0,0,255)
                elif (v == "."):
                    color = (100,100,100)
                elif (v == " "):
                    color = (255,255,255)
                for z in range((size-1)*(size-1)):
                    img.putpixel((j*size + (z%(size-1)), i*size + int(z/(size-1))), color)
                    
                
        d = ImageDraw.Draw(img)
        for i in range(len(map)):
            for j,v in enumerate(map[i]):    
                if (v.isupper()):
                    d.text((j*size+2, i*size+2), v, fill=(255,255,255))
                if ((i,j), level) in visited:
                    d.text((j*size+2, i*size+2), str(visited[((i,j), level)]), fill=(0,255,0))
        img.save('mapa-'+str(level)+'.png')
    
    
    # for k,v in visited.items():
        # if (k[1] == 0):
            # print(str(k[0])+" "+str(v))