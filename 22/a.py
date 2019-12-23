def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

with open("input.txt") as f:
    suffleCount = 101741582076661
    deckSize = 119315717514047 
    position = 2020
    # deckSize = 10 
    # position = 5
    # deckSize = 10007 
    # position = 2019
    # deckSize = 10007 
    # position = 7545
    # deck = [i for i in range(deckSize)]
    
    steps = []
    stepsF = []
    
    for line in f:
        steps.append(line)
        if line.startswith("cut"):
            num = line[4:-1]
            if (num[0:1] == "-"):
                stepsF.append((lambda n: lambda x: ((x-n)%deckSize))(int(num[1:])))
            else:
                stepsF.append((lambda n: lambda x: ((x+n)%deckSize))(int(num)))
        elif line.startswith("deal into new stack"):
            stepsF.append(lambda x: deckSize-1-x % deckSize)
        elif line.startswith("deal with increment"):
            increment = int(line[20:-1])
            g,x,y = xgcd(increment, deckSize)
            stepsF.append((lambda x, g: lambda z: int(((x*z)/g) % deckSize))(x,g))
            
        # if line.startswith("cut"):
            # num = line[4:-1]
            # if (num[0:1] == "-"):
                # cut = -int(num[1:])
            # else:
                # cut = int(num)
            # deck = deck[cut:] + deck[:cut]
        # elif line.startswith("deal into new stack"):
            # deck.reverse()
        # elif line.startswith("deal with increment"):
            # increment = int(line[20:-1])
            # newDeck = [-1 for i in deck]
            # #index = 0
            # for i, c in enumerate(deck):
                # newDeck[(i*increment) % len(deck)] = c
                # #index = (index + increment) % len(deck)
            # deck = newDeck
        # #print(line.strip())
        # #print(deck)
    # print(deck.index(position))
    # print(deck[position])
    
    steps.reverse()
    stepsF.reverse()
    card = position
    card2 = position
    
    # for line in steps:
        # print([card])
        # if line.startswith("cut"):
            # num = line[4:-1]
            # if (num[0:1] == "-"):
                # card = ((card-int(num[1:]))%deckSize)
            # else:
                # card = ((card+int(num))%deckSize)
        # elif line.startswith("deal into new stack"):
            # card = deckSize-1-card % deckSize
        # elif line.startswith("deal with increment"):
            # increment = int(line[20:-1])
            # g,x,y = xgcd(increment, deckSize)
            # card = int(((x*card)/g) % deckSize)
            
            
    shuffes = list()
    stepc = 0
    last = position
    for i in range(23249):
        for step in stepsF:
            card = step(card)
        
        # print(card)
        # print((card - last) % deckSize
        stepc += 1
        
        if (abs(last - card) in shuffes):
            print("repeating in "+str(stepc))
            #print(shuffes[(101741582076661 % len(shuffes))])
            break
            
        shuffes.append(abs(last - card))
        last = card
            
    print(card)
    