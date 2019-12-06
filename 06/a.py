class MapObject:
    def __init__(self, name, orbitCount, parent): 
        self.name = name
        self.parent = parent
        self.orbitCount = orbitCount

map = {}
inputs = []

with open("input.txt") as f:
    for con in f:
        inputs.append(con.strip().split(")"))
        

map["COM"] = MapObject("COM", 0, None)

while len(inputs) > 0:
    for e in inputs:
        if e[0] in map.keys():
            map[e[1]] = MapObject(e[1], map[e[0]].orbitCount+1, map[e[0]])
            inputs.remove(e)
            break
            
            
print(sum([x.orbitCount for x in map.values()]))

StepCount = 0
You = map["YOU"]
Santa = map["SAN"]

#Look for common accesor
if You.orbitCount > Santa.orbitCount:
    StepCount += You.orbitCount - Santa.orbitCount
    for i in range(StepCount):
        You = You.parent
elif You.orbitCount < Santa.orbitCount:
    StepCount += Santa.orbitCount - You.orbitCount
    for i in range(StepCount):
        Santa = Santa.parent
#Check     
print([StepCount, You.orbitCount == Santa.orbitCount])

while You != Santa:
    StepCount += 2
    You = You.parent
    Santa = Santa.parent
    

print(StepCount-2)