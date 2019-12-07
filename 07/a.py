import math
import itertools

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
        
    def append(self, content):
        self.data.append(content)
    def read(self):
        if self.avail():
            val = self.data[self.position]
            self.position += 1
            return val
        else:
            raise Exception("Data not avail")
    def avail(self):
        return len(self.data) > self.position

class Program:
    
    def __init__(self, instructions, input, output): 
        self.mem = instructions.copy()
        self.input = input
        self.output = output
        self.ip = 0
        self.finished = False
        self.waitingForInput = False
        
    def run(self):
        self.waitingForInput = False
        while (self.mem[self.ip] != 99):
            op = OpCode(self.mem[self.ip], self.ip)
            execResult = op.execute(self.mem, self.input, self.output)
            if op.executed:
                self.ip = execResult
            else:
                self.waitingForInput = True
                return
        self.finished = True
        
    def blocked(self):
        return self.waitingForInput and not(self.input.avail())
    

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
        99: 1
    }

    def __init__(self, code, ip): 
        self.ip = ip
        self.opCode = code % 100
        self.OriginalCode = code
        self.executed = False
        if not(self.opCode) in self.opcodes.keys():
            raise "Wrong opCode "+str(self.OriginalCode)
        
    def getParamMode(self, pos):
        return int(self.OriginalCode / math.pow(10, pos+1)) % 10
        
    def getLength(self):
        return self.opcodes[self.opCode]
        
    def loadParameter(self, position, memory):
        if (self.getParamMode(position) == 0):
            return memory[memory[self.ip+position]]
        else:
            return memory[self.ip+position]
        
    def execute(self, memory, input, output):
        self.executed = True
        if (self.opCode == 1):
            memory[memory[self.ip+3]] = self.loadParameter(1, memory) + self.loadParameter(2, memory)
        elif (self.opCode == 2):
            memory[memory[self.ip+3]] = self.loadParameter(1, memory) * self.loadParameter(2, memory)
        elif (self.opCode == 3):
            if not(input.avail()):
                self.executed = False
                return 0 #Yeld
            memory[memory[self.ip+1]] = input.read()
        elif (self.opCode == 4):
            output.append(self.loadParameter(1, memory))
        #jump-if-true
        elif (self.opCode == 5):
            if (self.loadParameter(1, memory) != 0):
                return self.loadParameter(2, memory)
        #jump-if-false
        elif (self.opCode == 6):
            if (self.loadParameter(1, memory) == 0):
                return self.loadParameter(2, memory)
        #less than
        elif (self.opCode == 7):
            if (self.loadParameter(1, memory) < self.loadParameter(2, memory)):
                memory[memory[self.ip+3]] = 1
            else:
                memory[memory[self.ip+3]] = 0
        #equals
        elif (self.opCode == 8):
            if (self.loadParameter(1, memory) == self.loadParameter(2, memory)):
                memory[memory[self.ip+3]] = 1
            else:
                memory[memory[self.ip+3]] = 0
        return self.ip + self.getLength()

with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]
    
    outputs = []
    
    input = Pipe()
    output = Pipe()
    
    #for p in itertools.permutations([0,1,2,3,4]):##Part1
    for p in itertools.permutations([5,6,7,8,9]):##Part2
        scheduler = Scheduler()
        pipes = []
        pipes.append(Pipe([p[0], 0])) ##input pipe
        
        ##Creation of program chain
        for i in range(5):
            if i < 4:
                pipes.append(Pipe([p[i+1]]))
            else: # Last output is special
                #pipes.append(Pipe())  ##Part1
                pipes.append(pipes[0]) ##Part2 //Back propagation of last output to firtst input
            scheduler.addJob(Program(code, pipes[i], pipes[i+1]))
        
        scheduler.start()
        
        outputs.append(pipes[5].data.pop())
        
    print(max(outputs))
    