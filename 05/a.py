import math

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
        if not(self.opCode) in self.opcodes.keys():
            raise "Wrong opCode "+str(self.OriginalCode)
        
    def getParamMode(self, pos):
        return int(self.OriginalCode / math.pow(10, pos+1)) % 10
        
    def getLength(self):
        return self.opcodes[self.opCode]
        
    def loadParameter(self, position, memory):
        if (self.getParamMode(position) == 0):
            return memory[memory[ip+position]]
        else:
            return memory[ip+position]
        
    def execute(self, memory, io):
        if (self.opCode == 1):
            memory[memory[self.ip+3]] = self.loadParameter(1, memory) + self.loadParameter(2, memory)
        elif (self.opCode == 2):
            memory[memory[self.ip+3]] = self.loadParameter(1, memory) * self.loadParameter(2, memory)
        elif (self.opCode == 3):
            memory[memory[self.ip+1]] = io[0]
        elif (self.opCode == 4):
            io[1] = self.loadParameter(1, memory)
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
    
        
op = OpCode(1002, 0)

with open("input.txt") as f:
    program = [int(x) for x in f.read().split(",")]
    print(program)
    
    io = [5, 0]
    
    ip = 0
    while (program[ip] != 99):
        op = OpCode(program[ip], ip)
        ip = op.execute(program, io)
        print(io[1])
  