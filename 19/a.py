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

def checkPixel(i,j):
    a = Pipe([i,j])
    b = Pipe()
            
    scheduler = Scheduler()
    scheduler.addJob(Program(code, a, b))
    scheduler.start()
    
    return b.read() == 1
        
with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]

    
    img = Image.new('RGB', (5000,5000))
    map = [[0 for i in range(5000)] for j in range(5000)]
    
    count = 1
    minPixel = 4
    maxPixel = 4
    for i in range(5,2000): #beam starts on line 5        
        while not(checkPixel(i,minPixel)):
            minPixel += 1
            
        while checkPixel(i,maxPixel):
            maxPixel += 1
        
        count += (maxPixel-minPixel)
        for j in range(minPixel, maxPixel):
            map[i][j] = 1
            img.putpixel((i,j), (255,255,255))
        print([i,minPixel, maxPixel])
        
        if (i > 100 and map[i-99][minPixel] == 1 and map[i-99][minPixel+99] == 1):
            print([i-99, minPixel+99, minPixel + (i-99)*10000])
            break
        
       
    print(count)
    img.save('beam.png')
    
    # 9051045
    # 9161058
    # 9201063
    