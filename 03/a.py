wires = []
with open("input.txt") as f:
    for wire in f:
        wires.append([(x[0], int(x[1:])) for x in wire.strip().split(",")])
    
#print(wires)

occupiedPositions = dict()
crossedPositions = set()
crossingsLengths = list()
wireNum = 0
for wire in wires:
    position = (0,0)
    counter = 0
    for step in wire:
        vector = (0, 0)
        if (step[0] == "R"):
            vector = (1, 0)
        elif (step[0] == "L"):
            vector = (-1, 0)
        elif (step[0] == "U"):
            vector = (0, 1)
        elif (step[0] == "D"):
            vector = (0, -1)
            
        for i in range(step[1]):
            counter += 1
            position = (position[0] + vector[0], position[1] + vector[1])
            if (wireNum == 0):
                if not(position in occupiedPositions.keys()):
                    occupiedPositions[position] = counter
            else:
                if (position in occupiedPositions.keys()):
                    crossedPositions.add(position)
                    crossingsLengths.append(counter+occupiedPositions[position])
    wireNum += 1
                
print(crossedPositions)

print(min([abs(x[0]) + abs(x[1]) for x in crossedPositions]))
print(min(crossingsLengths))