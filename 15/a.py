import math
import itertools
from collections import deque

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
        

class ReparRobotController:
    def __init__(self, input, output): 
        self.input = input
        self.output = output
        self.finished = False
        self.waitingForInput = False
        self.visited = dict()
        self.trace = deque()
        self.way = []
        self.trace.append((0,0)) #Starting point
        
    def run(self):
        self.waitingForInput = False
        
        if not(self.input.avail()):
            self.waitingForInput = True
            return
            
        value = self.input.read()
        self.visited[self.trace[-1]] = value
        
        #print("Visiting: "+str(self.trace[-1])+" -> "+str(value))
        
        if value == 0: #wall
            self.trace.pop()
        elif value == 2:
            print("Found it at:"+str(self.trace[-1])+" with length: "+str(len(self.trace)-1))
            
        dir = self.getNextUnknownDirection()
        if dir == None and len(self.trace) > 1:
            dir = self.getBackwardsFrom(self.trace.pop())    
        elif (dir == None):
            self.finished = True
            self.drawMap()
            self.fillWithOxigen()
            return
        else:
            self.trace.append(dir[1]) #Append to trace only when not backtracked
            
        self.output.append(dir[0])
        self.way.append(dir[1])
        #yelds execution
            
        
    def blocked(self):
        return self.waitingForInput and not(self.input.avail())
    def getBackwardsFrom(self, oldPosition):
        newPosition = self.trace[-1]
        directions = [(0,-1),(0,1),(-1,0),(1,0)]
        for i, dir in enumerate(directions):
            if (oldPosition[0]+dir[0], oldPosition[1]+dir[1]) == newPosition:
                return (i+1, newPosition)
        return None
        
    def getNextUnknownDirection(self):
        currentPosition = self.trace[-1]
        directions = [(0,-1),(0,1),(-1,0),(1,0)]
        for i, dir in enumerate(directions):
            nextTile = (currentPosition[0]+dir[0], currentPosition[1]+dir[1])
            if not(nextTile in self.visited):
                return (i+1, nextTile)
        return None
        
    def drawMap(self):
        minX = min([x[0] for x in self.visited.keys()])
        maxX = max([x[0] for x in self.visited.keys()])
                
        minY = min([x[1] for x in self.visited.keys()])
        maxY = max([x[1] for x in self.visited.keys()])
            
        img = Image.new('RGB', ((maxX+1-minX)*8, (maxY+1-minY)*8))
        for k, v in self.visited.items():
            color = 0
            if (k == (0,0)): 
                color = (0,255,0)
            elif (v == 2):
                color = (255,0,0)
            elif (v == 0): 
                color = (255,255,255)
            elif (v == 1):
                color = (50,50,50)
                
            for i in range(64):
                img.putpixel((int((k[0] - minX)*8 + (i%8)), int((k[1] - minY)*8 + (i/8))), color)
        img.save('mapa.png')
        
    def fillWithOxigen(self):
        start = next(k for k, v in self.visited.items() if v == 2)
        locations = set(k for k, v in self.visited.items() if v == 1)
        borderline = [start]
        counter = 0
        
        while len(locations) > 0 and len(borderline) > 0:
            newBordeline = []
            for l in borderline:
                directions = [(0,-1),(0,1),(-1,0),(1,0)]
                for dir in directions:
                    nextLocation = (l[0]+dir[0], l[1]+dir[1])
                    if nextLocation in locations:
                        locations.remove(nextLocation)
                        newBordeline.append(nextLocation)
            counter+=1
            borderline = newBordeline
            
        print("Oxigen fils in: "+str(counter))


with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]

    a = Pipe()
    b = Pipe()
    b.append(1) #first is just empty tile
    
    scheduler = Scheduler()
    scheduler.addJob(Program(code, a, b))
    scheduler.addJob(ReparRobotController(b, a))
    scheduler.start()
