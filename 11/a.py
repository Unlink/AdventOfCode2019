import math
import itertools

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
        if self.closed:
            raise Exception("Pipe closed")
        elif self.avail():
            val = self.data[self.position]
            self.position += 1
            return val
        else:
            raise Exception("Data not avail")
    def avail(self):
        return len(self.data) > self.position
        
    def close(self):
        self.closed = True

class Program:
    
    def __init__(self, instructions, input, output): 
        self.mem = instructions.copy()
        self.input = input
        self.output = output
        self.ip = 0
        self.finished = False
        self.waitingForInput = False
        self.relativeBase = 0
        
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

        
class PaintRobot:
    
    def __init__(self, input, output): 
        self.input = input
        self.output = output
        self.finished = False
        self.waitingForInput = False
        self.currentPosition = (0,0)
        self.direction = 0 #0 up, 1 right, 2 down 3 left
        self.visited = dict()
        self.dirVectors = [(0,-1), (1,0), (0, 1), (-1, 0)]
        
    def run(self):
        self.waitingForInput = False
        
        while not(self.input.closed):
            if not(self.input.avail()):
                self.waitingForInput = True
                return
            
            color = self.input.read()
            #print("Printing "+str(self.currentPosition)+" to " + str(color))
            self.visited[self.currentPosition] = color
            
            direction = self.input.read()
            if (direction == 0): #Left
                self.direction = self.direction - 1
                if (self.direction < 0):
                    self.direction = 3
            elif (direction == 1):
                self.direction = (self.direction + 1) % 4
            else:
                print("Wrong direction")
            
            self.currentPosition = (self.currentPosition[0] + self.dirVectors[self.direction][0], self.currentPosition[1] + self.dirVectors[self.direction][1])
            if not(self.currentPosition in self.visited):
                self.visited[self.currentPosition] = 0 #black
            self.output.append(self.visited[self.currentPosition])
        
        self.output.append(len(self.visited))
        
        minX = min([x[0] for x in self.visited.keys()])
        maxX = max([x[0] for x in self.visited.keys()])
        
        minY = min([x[1] for x in self.visited.keys()])
        maxY = max([x[1] for x in self.visited.keys()])
        
        self.output.append(minX)
        self.output.append(minY)
        self.output.append(maxX)
        self.output.append(maxY)
        
        img = Image.new('L', ((maxX+1-minX)*4, (maxY+1-minY)*4))
        for k in self.visited.keys():
            for i in range(4):
                img.putpixel((int((k[0] - minX)*4 + (i%2)), int((k[1] - minY)*4 + (i/2))), 255 if self.visited[k] == 1 else 0)
            #draw = ImageDraw.Draw(img)
            #draw.ellipse((px-2, py-2, px+2, py+2), fill = 'white', outline ='white')
        img.save('malovanie2.png')
        
        self.finished = True
        
    def blocked(self):
        return self.waitingForInput and not(self.input.avail())
        
with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]
    a = Pipe()
    b = Pipe()
    
    #a.append(0) #First is black
    a.append(1) #First is White
    
    scheduler = Scheduler()
    scheduler.addJob(Program(code, a, b))
    scheduler.addJob(PaintRobot(b, a))
    scheduler.start()
       
        
    #print(a.data)
    