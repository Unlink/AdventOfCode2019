import math
import itertools

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
            raise Exception("Wrong opCode "+str(self.OriginalCode))
        
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
        
def printParameter(op, pos):
    if (op.getParamMode(pos) == 0):
        return "["+str(op.calculateMemoryAdress(pos))+"]"
    elif (op.getParamMode(pos) == 1):
        return str(op.loadParameter(pos))
    elif (op.getParamMode(pos) == 2):
        return "[base + "+str(op.calculateMemoryAdress(pos))+"]"
        
with open("05.txt") as f:
    code = [int(x) for x in f.read().split(",")]
    origLen = len(code)
    ip = 0
    while ip < origLen:
        try:
            op = OpCode(code, ip, 0)
            print(ip, end="\t")
            if (op.opCode == 1):
                print("add "+(printParameter(op, 1)+" "+printParameter(op, 2)+" "+printParameter(op, 3)).ljust(30)+"\t# "+printParameter(op, 3)+" = "+printParameter(op, 1)+" + "+printParameter(op, 2)+"\t## "+printParameter(op, 3)+"="+str(op.loadParameter(1))+" + "+str(op.loadParameter(2)))
            elif (op.opCode == 2):
                print("mull "+(printParameter(op, 1)+" "+printParameter(op, 2)+" "+printParameter(op, 3)).ljust(30)+"\t# "+printParameter(op, 3)+" = "+printParameter(op, 1)+" * "+printParameter(op, 2)+"\t## "+printParameter(op, 3)+"="+str(op.loadParameter(1))+" * "+str(op.loadParameter(2)))
            elif (op.opCode == 3):
                print("read "+printParameter(op, 1))
            elif (op.opCode == 4):
                print("write "+printParameter(op, 1))
            #jump-if-true
            elif (op.opCode == 5):
                print("jIfTrue "+(printParameter(op, 1)+" "+printParameter(op, 2)).ljust(30)+"\t# if("+printParameter(op, 1)+" == 1) goto "+printParameter(op, 2))
            #jump-if-false
            elif (op.opCode == 6):
                print("jIfFalse "+(printParameter(op, 1)+" "+printParameter(op, 2)).ljust(30)+"\t# if("+printParameter(op, 1)+" == 0) goto "+printParameter(op, 2))
            #less than
            elif (op.opCode == 7):
                print("lessThan "+(printParameter(op, 1)+" "+printParameter(op, 2)+" "+printParameter(op, 3)).ljust(30)+"\t# if "+printParameter(op, 1)+" < "+printParameter(op, 2)+" "+printParameter(op, 3)+" == 1 else 0\t## "+printParameter(op, 1)+"<"+str(op.loadParameter(2)))
            #equals
            elif (op.opCode == 8):
                print("equals "+(printParameter(op, 1)+" "+printParameter(op, 2)+" "+printParameter(op, 3)).ljust(30)+"\t# if "+printParameter(op, 1)+" == "+printParameter(op, 2)+" "+printParameter(op, 3)+" == 1 else 0\t## "+printParameter(op, 1)+" == "+str(op.loadParameter(2)))
            elif (op.opCode == 9):
                print("setBase "+(printParameter(op, 1)).ljust(30)+"\t## "+str(op.loadParameter(1)))
            elif (op.opCode == 99):
                print("HALT")
            ip += op.getLength()
        except Exception as e:
            ip += 1
        
    print(len(code))