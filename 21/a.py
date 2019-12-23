import math

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
        print("Intcode program halts")
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

class ASCIIScript:
    
    def __init__(self, input, output): 
        self.input = input
        self.output = output
        self.finished = False
        self.waitingForInput = True
        
    def run(self):
        self.waitingForInput = False
        if (self.input.avail()):
            buff = ""
            while self.input.avail():
                val =  self.input.read()
                if (val > 255):
                    print(val)
                    self.finished = True
                    return
                    
                buff += chr(val)
            print(buff)

        if (self.input.closed):
            self.finished = True
            return
        readed = input()
        
        for c in readed:
            val = ord(c)
            self.output.append(val)
        self.output.append(10)
        #self.waitingForInput = True
        
    def blocked(self):
        return self.waitingForInput and not(self.input.closed) and not(self.input.avail())

# def checkProgram(lines):
    # a = Pipe()
    # b = Pipe()
    
    # lines.append("WALK")
    # for instruction in lines:
        # for c in instruction:
            # val = ord(c)
            # b.append(val)
        # b.append(10)
    
    # scheduler = Scheduler()
    # scheduler.addJob(Program(code, b, a))
    # scheduler.start()
    
    # return a.data[-1:]
    
# def generateInstructions(combinations, size):
    # if (size == 0):
        # yield ()
        
    # for sub in generateInstructions(combinations, size-1):
        # for c in combinations:
            # yield sub+(c,)
        
with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]
    
    
    # operations = ["AND", "OR", "NOT"]
    # reg1 = ["A", "B", "C", "D", "T", "J"]
    # reg2 = ["T", "J"]
    
    # combinations = list()
    # for o in operations:
        # for r1 in reg1:
            # for r2 in reg2:
                # combinations.append(o+" "+r1+" "+r2)
                
    # print("Possible instructions: "+str(len(combinations)))
    
    # for i in range(2,11):
        # print(i)
        # for c in generateInstructions(combinations, i):
            # #print(c)
            # val = checkProgram(list(c))
            # #print(val)
            # if (val[0] > 254):
                # print(c)
                # break
        
            
        
    
    a = Pipe()
    b = Pipe()
    
    scheduler = Scheduler()
    scheduler.addJob(Program(code, b, a))
    scheduler.addJob(ASCIIScript(a, b))
    scheduler.start()

#Jump if next is empty
#Jump if #?.#.

# OR C T
# NOT T T
# AND A T
# AND D T
# AND H T
# NOT A J
# OR T J
# RUN


# OR E T
# AND F T
# NOT T T
# AND A T
# AND D T
# AND H T
# NOT A J
# OR T J
# RUN


# OR E T
# AND I T
# OR H T
# OR F J
# AND E J
# OR J T
# NOT D J
# NOT J J
# AND T J
# RUN


# #A Part solution
# OR A T
# NOT C J
# AND J T
# AND D T
# NOT A J
# OR T J
# WALK


# @................
# #####..#.########
 # ABCDEFGH    