import math
import itertools


from colorama import Fore, Back, Style
import sys
import time

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
        

pos = lambda y, x: '\x1b[%d;%dH' % (y, x)
def getchar():
   #Returns a single character from standard input
   import tty, termios, sys
   fd = sys.stdin.fileno()
   old_settings = termios.tcgetattr(fd)
   try:
      tty.setraw(sys.stdin.fileno())
      ch = sys.stdin.read(1)
   finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
   return ch

class Arkada:
    def __init__(self, input, output): 
        self.input = input
        self.output = output
        self.finished = False
        self.waitingForInput = False
        self.tiles = dict()
        self.lastBallPos = (0,0)
        self.changed = set()
        
    def run(self):
        self.waitingForInput = False
        
        if not(self.input.avail()):
            if (self.input.closed):
                print(Style.RESET_ALL)
                self.finished = True
                return
            else:
                self.waitingForInput = True
                return
            
        score = 0
        remaining = 0
        while b.avail():
            data = (b.read(), b.read(), b.read())
            if data[0] == -1:
                score = data[2]
            else:
                self.tiles[(data[0], data[1])] = data[2]
                self.changed.add((data[0], data[1]))
                
        remaining = len([x for x in self.tiles.values() if x == 2])

        minX = min([x[0] for x in self.tiles.keys()])
        maxX = max([x[0] for x in self.tiles.keys()])
                
        minY = min([x[1] for x in self.tiles.keys()])
        maxY = max([x[1] for x in self.tiles.keys()])
            
        # img = Image.new('RGB', ((maxX+1-minX)*8, (maxY+1-minY)*8))
        # for k in tiles:
            # color = 0
            # if (k[2] == 1): 
                # color = (150,150,150)
            # elif (k[2] == 2):
                # color = (0,150,0)
            # elif (k[2] == 3):
                # color = (0,0,150)
            # elif (k[2] == 4):
                # color = (255,0,0)
                
            # for i in range(64):
                # img.putpixel((int((k[0] - minX)*8 + (i%8)), int((k[1] - minY)*8 + (i/8))), color)
                
        # #d = ImageDraw.Draw(img)
        # #d.text((1,1), str(score), fill=(255,255,255,128))
        # img.save('arkada.png')
        
        ball = (0,0)
        panel = (0,0)
        
        print(pos(1,1)+("Score: "+str(score)+" Remaining: "+str(remaining)).ljust(50))
        for k in self.tiles.keys():
            if not(k in self.changed):
                continue
            consoleColor = Back.BLACK+" "
            if (self.tiles[k] == 1): 
                consoleColor = Back.WHITE+" "
            elif (self.tiles[k] == 2):
                consoleColor = Back.GREEN+" "
            elif (self.tiles[k] == 3):
                consoleColor = Back.YELLOW+"_"+Style.RESET_ALL
                panel = k
            elif (self.tiles[k] == 4):
                consoleColor = Back.RED+" "+Style.RESET_ALL
                ball = k
            print(pos(k[1] - minY+2, k[0] - minX+1)+consoleColor+"", end="")
        print(Style.RESET_ALL)
        self.changed.clear()
        
        direction = 1 if self.lastBallPos[0] < ball[0] else -1
        
        nextBallX = ball[0] + direction
        if ((panel[1] - 1) == ball[1] and panel[0] == ball[0]):
            self.output.append(0)
        elif (panel[0] == nextBallX):
            self.output.append(0)
        elif (panel[0] < nextBallX):
            self.output.append(1)
        else:
            self.output.append(-1)
        
        time.sleep(0.01)
        self.lastBallPos = ball
        # while True:
            # print(Style.RESET_ALL)
            # ch = getchar()
            # if ch == "a":
                # self.output.append(-1)
                # break
            # elif ch == "d":
                # self.output.append(1)
                # break
            # elif ch == "s":
                # self.output.append(0)
                # break
            # elif ch.strip() == '':
                # print(Style.RESET_ALL)
                # self.finished = True
                # return
        
    def blocked(self):
        return self.waitingForInput and not(self.input.avail())
        
 
with open("input.txt") as f:
    code = [int(x) for x in f.read().split(",")]
    
    code[0] = 2  #Part 2
    
    a = Pipe()
    b = Pipe()
    
    #Clear
    print(chr(27) + "[2J")
    
    scheduler = Scheduler()
    scheduler.addJob(Program(code, a, b))
    scheduler.addJob(Arkada(b, a))
    scheduler.start()
       
    
    
print("")