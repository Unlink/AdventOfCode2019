import math
from PIL import Image, ImageDraw

class Scheduler:
    def __init__(self):
        self.jobs = []
        
    def addJob(self, job):
        self.jobs.append(job)
        
    def loadAvailJobs(self):
        return [x for x in self.jobs if not(x.finished) and not(x.blocked())]
        
    def start(self):
        availableJobs = self.loadAvailJobs()
        while len(availableJobs) > 0:
            availableJobs[0].run()
            
            availableJobs = self.loadAvailJobs()
        

class Pipe:
    def __init__(self, input = None):
        if (input == None):
            input = []
        self.data = input
        self.position = 0
        self.closed = False
        
    def append(self, content):
        self.data.append(content)
    def read(self):
        if self.avail():
            val = self.data[self.position]
            self.position += 1
            return val
        elif self.closed:
            raise Exception("Pipe closed")
        else:
            raise Exception("Data not avail")
    def avail(self):
        return len(self.data) > self.position
        
    def close(self):
        self.closed = True

class Program:
    
    def __init__(self, instructions, input, output, closeOutput=True): 
        self.mem = instructions.copy()
        self.input = input
        self.output = output
        self.ip = 0
        self.finished = False
        self.waitingForInput = False
        self.relativeBase = 0
        self.closeOutput = closeOutput
        
    def run(self):
        self.waitingForInput = False
        while (self.mem[self.ip] != 99):
            op = OpCode(self.mem, self.ip, self.relativeBase)
            execResult = op.execute(self.input, self.output)
            if op.executed:
                self.ip = execResult
                self.relativeBase = op.relativeBase
            else:
                self.waitingForInput = True
                return
        if (self.closeOutput):
            self.output.close()
        self.finished = True
        
    def blocked(self):
        return self.waitingForInput and not(self.input.closed) and not(self.input.avail())
    

class OpCode:
    opcodes = {
        1: 4,
        2: 4,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 4,
        9: 2,
        99: 1
    }

    def __init__(self, memory, ip, relativeBase): 
        self.memory = memory
        self.ip = ip
        self.opCode = memory[ip] % 100
        self.OriginalCode = memory[ip]
        self.executed = False
        self.relativeBase = relativeBase
        if not(self.opCode) in self.opcodes.keys():
            raise "Wrong opCode "+str(self.OriginalCode)
        
    def getParamMode(self, pos):
        return int(self.OriginalCode / math.pow(10, pos+1)) % 10
        
    def getLength(self):
        return self.opcodes[self.opCode]
    
    #because advent of code thinks that writing to not alocated memory is ok :)
    def checkMemory(self, position):
        while position >= len(self.memory):
            self.memory.append(0)
        
    def calculateMemoryAdress(self, position):
        self.checkMemory(self.ip+position)
        ##Absolute adressing
        if (self.getParamMode(position) == 0):
            self.checkMemory(self.memory[self.ip+position])
            return self.memory[self.ip+position]
        ##Relative addresing
        elif (self.getParamMode(position) == 2):
            self.checkMemory(self.relativeBase+self.memory[self.ip+position])
            return self.relativeBase+self.memory[self.ip+position]
        ##Direct value
        else:
            return self.ip+position
    
    def loadParameter(self, position):
        return self.memory[self.calculateMemoryAdress(position)]
        
    def write(self, position, value):
        self.memory[self.calculateMemoryAdress(position)] = value
        
    def execute(self, input, output):
        self.executed = True
        if (self.opCode == 1):
            self.write(3, self.loadParameter(1) + self.loadParameter(2))
        elif (self.opCode == 2):
            self.write(3, self.loadParameter(1) * self.loadParameter(2))
        elif (self.opCode == 3):
            if not(input.avail()):
                self.executed = False
                return 0 #Yeld
            self.write(1,input.read())
        elif (self.opCode == 4):
            #print([self.ip, self.loadParameter(1), self.calculateMemoryAdress(1)])
            output.append(self.loadParameter(1))
        #jump-if-true
        elif (self.opCode == 5):
            if (self.loadParameter(1) != 0):
                return self.loadParameter(2)
        #jump-if-false
        elif (self.opCode == 6):
            if (self.loadParameter(1) == 0):
                return self.loadParameter(2)
        #less than
        elif (self.opCode == 7):
            if (self.loadParameter(1) < self.loadParameter(2)):
                self.write(3,1)
            else:
                self.write(3,0)
        #equals
        elif (self.opCode == 8):
            if (self.loadParameter(1) == self.loadParameter(2)):
                self.write(3,1)
            else:
                self.write(3,0)
        elif (self.opCode == 9):
            #if (self.getParamMode(1) == 2):
            self.relativeBase += self.loadParameter(1)
            #else:
            #    self.relativeBase += self.loadParameter(1)
        return self.ip + self.getLength()

def isPath(map, x,y):
    return x >= 0 and y >= 0 and y < len(map) and x < len(map[y]) and map[y][x] != "."

def countNearby(map, point):
    directions = [(1,0), (-1, 0), (0, 1), (0, -1)]
    sum = 0
    for d in directions:
        newX = d[0] + point[0]
        newY = d[1] + point[1]
        
        if isPath(map, newX, newY):
            sum += 1
            
    return sum
    
def drawMap(map, path = ""):
        w = max(len(x) for x in map)
        h = len(map)
        
        img = Image.new('RGB', (w*8, w*8))
        for i in range(len(map)):
            for j,v in enumerate(map[i]):    
                color = 0
                if (v == "#"): 
                    color = (255,255,255)
                elif (v == "*"): 
                    color = (180,0,0)
                elif (v == "?"): 
                    color = (0,0,180)
                elif (v == "^"):
                    color = (0,255,0)
                elif (v == "|"):
                    color = (0,126,126)
                for z in range(36):
                    img.putpixel((j*8 + (z%6), i*8 + int(z/6)), color)
        img.save('mapa'+path.replace(",", "")+'.png')

class Robot:
    
    def __init__(self, map, currentPosition, direction): 
        self.currentPosition = currentPosition
        self.direction = direction #0 up, 1 right, 2 down 3 left
        self.dirVectors = [(0,-1), (1,0), (0, 1), (-1, 0)]
        self.map = map
        
    def tryPath(self, path, symbol):
        m = [[x for x in row] for row in self.map]
        path = path.split(",")
        for i in range(0, len(path), 2):
            dir = path[i]
            count = int(path[i+1])
            self.rotate(dir)
            for j in range(count):
                self.currentPosition = (self.currentPosition[0] + self.dirVectors[self.direction][0], self.currentPosition[1] + self.dirVectors[self.direction][1])
                if (isPath(self.map, *self.currentPosition)):
                    m[self.currentPosition[1]][self.currentPosition[0]] = symbol
                else:
                    return None
        return m
        
    def rotate(self, dir):
        if dir == "L":
            self.direction -= 1
            if self.direction < 0:
                self.direction = 3
        elif dir == "R":
            self.direction = (self.direction+1)%4
            
def lookForPath(map, path, symbol):
    m = [[x for x in row] for row in map]
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] != ".":
                for d in range(4):
                    robot = Robot(m, (j,i), d)
                    result = robot.tryPath(path, symbol)
                    if (result != None):
                        m = result
    return m

with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]

    code[0] = 2
    a = Pipe()
    b = Pipe()
    
    pathA = "R,6,L,10,R,8,R,8"
    pathB = "R,12,L,8,L,10"
    pathC = "R,12,L,10,R,6,L,10"
    main = "A,B,A,C,B,C,A,B,A,C"
    
    for c in main:
        b.append(ord(c))
    b.append(10)
    
    for c in pathA:
        b.append(ord(c))
    b.append(10)
    
    for c in pathB:
        b.append(ord(c))
    b.append(10)
    
    for c in pathC:
        b.append(ord(c))
    b.append(10)
    
    b.append(ord("n"))
    b.append(10)
    
    scheduler = Scheduler()
    scheduler.addJob(Program(code, b, a))
    scheduler.start()
    
    print(a.data)
    
    # with open("input2.txt") as f2:
        # a.data = (ord(x) for x in f2.read())
    
    map = [[]]
    for v in (chr(x) for x in a.data):
        print(v, end="")
        if v == chr(10): #new line
            map.append([])
        else:
            map[len(map)-1].append(v)
    
    sum = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "^":
                startPos = (j,i)
            if map[i][j] == "#" and countNearby(map, (j,i)) > 2:
                print("Intersection in: "+str((j,i)))
                sum += i*j
    print(sum)
    
    
    drawMap(map)
    
    
    m = [[x for x in row] for row in map]
    robot = Robot(m, startPos, 0)
    
    m = robot.tryPath(pathA, "*")
    robot.map = m
    drawMap(m, "step1")
    
    m = robot.tryPath(pathB, "?")
    robot.map = m
    drawMap(m, "step2")
    
    m = robot.tryPath(pathA, "*")
    robot.map = m
    drawMap(m, "step3")
    
    m = robot.tryPath(pathC, "|")
    robot.map = m
    drawMap(m, "step4")
    
    m = robot.tryPath(pathB, "?")
    robot.map = m
    drawMap(m, "step5")
    
    m = robot.tryPath(pathC, "|")
    robot.map = m
    drawMap(m, "step6")
    
    m = robot.tryPath(pathA, "*")
    robot.map = m
    drawMap(m, "step7")
    
    m = robot.tryPath(pathB, "?")
    robot.map = m
    drawMap(m, "step8")
    
    m = robot.tryPath(pathA, "*")
    robot.map = m
    drawMap(m, "step9")
    
    m = robot.tryPath(pathC, "|")
    robot.map = m
    drawMap(m, "step10")
    
    
    