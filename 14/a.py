import math

recepts = {}

def parseItem(data):
    parts = data.strip().split(" ")
    return (parts[1].strip(), int(parts[0].strip()))

with open("input.txt") as f:
    for line in f:
        inputs, output = line.split("=>")
        x = parseItem(output)
        recepts[x[0]] = [x[1], []]
            
        for input in inputs.split(","):
            recepts[x[0]][1].append(parseItem(input))
        
opf = 0        
fuel = 0               
req = [("FUEL", 1)]
buffer = {}
ore = 0
limit = 1000000000000

while ore <= limit and len(req) > 0:
    while len(req) > 0:
        currentRequest = req.pop()
        ingedient, amount = currentRequest
        if ingedient == "FUEL":
            fuel += amount
        if (currentRequest[0] in buffer):
            if (buffer[ingedient] > amount):
                buffer[ingedient] -= amount
                amount = 0
            else:
                amount -= buffer[ingedient]
                buffer[ingedient] = 0

        if amount > 0:
            recept = recepts[ingedient]
            count = math.ceil(amount / recept[0])
            preparedCount = recept[0] * count
            
            if amount < preparedCount:
                buffer[ingedient] = preparedCount - amount
                
            for item in recept[1]:
                if item[0] == "ORE":
                    ore += item[1] * count
                else:
                    req.append((item[0], item[1] * count))
    if (opf == 0):
        opf = ore
    nextRequest = int((limit - ore) / opf)
    #Try one more
    if (ore<limit and nextRequest == 0):
        nextRequest = 1
    print("Current ore amount: "+str(ore)+" Fuel: "+str(fuel)+" Ore per fuel: "+str(opf)+" Next amount: "+str(nextRequest))
    if (nextRequest > 0):
        req.append(("FUEL", nextRequest))
    
print(buffer)