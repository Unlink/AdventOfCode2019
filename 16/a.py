
def generatePattern(count, index):
    seq = [0, 1, 0, -1]
    seqPointer = 0
    seqCounter = 1
    while count > 0:
        if seqCounter > index:
            seqCounter = 0
            seqPointer = (seqPointer + 1) % len(seq)
        yield seq[seqPointer]
        count -= 1
        seqCounter += 1

with open("input.txt", "r") as f:
    signal = [int(x) for x in f.read()]
    #print(signal)
    
    # for j in range(len(signal)):
        # print(list(generatePattern(len(signal), j))) 
        
    # for i in range(100):
        # signal = [abs(sum([s*p for s,p in zip(signal, generatePattern(len(signal), j))])) % 10 for j in range(len(signal))]
        # print(i)
   
   
        # print("After "+str(i+1))
        # print(signal)
        
        
        
    signal = signal * 10000
    offset = int("".join(str(x) for x in signal[:7]))
    print(offset)
    print(len(signal))
    print(len(signal) - offset)
    
    #print(sum(list(generatePattern(len(signal), offset))))

    trimmedSignal = signal[offset:]
    trimmedSignalLen = len(trimmedSignal)
    for i in range(100):
        buff = 0
        for j in range(trimmedSignalLen):
            buff = (buff + trimmedSignal[trimmedSignalLen-1-j]) % 10
            trimmedSignal[trimmedSignalLen-1-j] = buff
        print("After "+str(i+1))
        print(trimmedSignal[:8])