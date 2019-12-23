import math

class Scheduler:
    def __init__(self):
        self.jobs = []
        self.currentTick = 0
        
    def addJob(self, job):
        self.jobs.append(job)
        
    def loadAvailJobs(self):
        return sorted([x for x in self.jobs if not(x.finished) and not(x.blocked())], key=lambda x: x.lastTick)
        
    def start(self):
        availableJobs = self.loadAvailJobs()
        while len(availableJobs) > 0:
            availableJobs[0].run(self.currentTick, self.currentTick+25)
            self.currentTick = availableJobs[0].lastTick
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
        self.lastTick = 0
        
    def run(self, currentTick, maxTicks):
        self.waitingForInput = False
        self.lastTick = currentTick
        while (self.mem[self.ip] != 99):
            op = OpCode(self.mem, self.ip, self.relativeBase)
            execResult = op.execute(self.input, self.output)
            self.lastTick += 1
            if op.executed:
                self.ip = execResult
                self.relativeBase = op.relativeBase
            else:
                self.waitingForInput = True
                return
            if (self.lastTick > maxTicks):
                return #yelds exeecution
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
        
        
class Switch:
    def __init__(self, ports):
        self.waitingForInput = False
        self.finished = False
        self.lastTick = 0
        self.sockPorts = []
        self.nat = []
        self.natSends = set()
        for i in range(ports):
            self.sockPorts.append(SockPipe(self, i))
    
    def transmit(self, addr, data):
        if addr == 255:
            self.nat = data
        elif addr >= len(self.sockPorts):
            print("Wrong address: "+str(addr)+" data: "+str(data))
        else:
            self.sockPorts[addr].addData(data)
        # print("Sending to "+str(addr)+": "+str(data))
        
    def getPort(self, num):
        return (self.sockPorts[num], self.sockPorts[num])
        
    def run(self, currentTick, maxTicks):
        self.lastTick = maxTicks+1
        if len(self.nat) == 0:
            return

        iddle = 0
        for s in self.sockPorts:
            if s.iddle:
                iddle += 1
        # print("Iddle count "+str(iddle))
        if iddle == len(self.sockPorts):
            print("Sending "+str(self.nat)+" from NAT to 0")
            self.sockPorts[0].addData(self.nat)
            if self.nat[1] in self.natSends:
                raise Exception("Finish"+str(self.nat))
            self.natSends.add(self.nat[1])
            
    def blocked(self):
        return False
        
        
class SockPipe:
    def __init__(self, switch, adress):
        self.switch = switch
        self.sendBuff = []
        self.recvBuff = [adress]
        self.adress = adress
        self.iddle = False
        
    def addData(self, data):
        self.recvBuff = self.recvBuff + data
        self.iddle = False
        
    def append(self, content):
        self.sendBuff.append(content)
        if len(self.sendBuff) == 3:
            self.switch.transmit(self.sendBuff[0], self.sendBuff[1:])
            self.sendBuff = []
            
    def read(self):
        if len(self.recvBuff) > 0:
            # print("FROM "+str(self.adress)+" readed "+str(self.recvBuff[0]))
            return self.recvBuff.pop(0)
        else:
            # print("FROM "+str(self.adress)+" readed -1")
            self.iddle = True
            return -1
    def avail(self):
        return True
        
    def close(self):
        pass
    
        
with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]

    scheduler = Scheduler()
    switch = Switch(50)
    for i in range(50):
        scheduler.addJob(Program(code, *switch.getPort(i)))
    scheduler.addJob(switch)
    scheduler.start()
