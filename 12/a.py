moons = []
with open("input2.txt") as f:
    for riadok in f:
        riadok  = riadok.replace("<", "").replace("x=", "").replace("y=", "").replace("z=", "").replace(">", "")
        vektor = [int(x) for x in riadok.split(",")]
        moons.append(vektor)
        
velocities = [[0 for i in range(3)] for j in range(len(moons))]

print(moons)
print(velocities)

# for i in range(1001):
    # print("After: "+str(i))
    # for j in range(len(moons)):
        # print(str(moons[j]) + "   " + str(velocities[j]))
        
    # energy = sum([sum([abs(x) for x in moons[i]]) * sum([abs(x) for x in velocities[i]]) for i in range(len(moons))])
    # print(energy)
    
    # for j in range(len(moons)):
        # for v in range(3):
            # velocities[j][v] += sum([(0 if moons[j][v] == moons[x][v] else (moons[x][v]-moons[j][v])/abs(moons[x][v]-moons[j][v])) for x in range(len(moons))])
            
    # for j in range(len(moons)):
        # for p in range(3):
            # moons[j][p] += velocities[j][p]
            
def rozdiel(a, b):
    if a == b:
        return 0
    elif a < b:
        return 1
    else:
        return -1
          
i = 0
suradnica = 0
zaciatok = list([x[suradnica] for x in moons])
print(zaciatok)
while True:
    print("After: "+str(i))
    for j in range(len(moons)):
        print(str(moons[j]) + "   " + str(velocities[j]))
    i += 1
    for j in range(len(moons)):
        velocities[j][suradnica] += sum([rozdiel(moons[j][suradnica], moons[x][suradnica]) for x in range(len(moons))])
            
    sameCoords = 0
    for j in range(len(moons)):
        # for p in range(3):
        moons[j][suradnica] += velocities[j][suradnica]
        if moons[j][suradnica] == zaciatok[j]:
            sameCoords += 1
        
    if (sameCoords == len(moons) and sum([abs(x[suradnica]) for x in velocities]) == 0):
        for x in velocities:
            print(x)
        print(suradnica)
        print([abs(x[suradnica]) for x in velocities])
        print(i)
        
        print("FINAL")
        for j in range(len(moons)):
            print(str(moons[j]) + "   " + str(velocities[j]))
        for j in range(len(moons)):
            velocities[j][suradnica] += sum([rozdiel(moons[j][suradnica], moons[x][suradnica]) for x in range(len(moons))])
        break;
            
            
