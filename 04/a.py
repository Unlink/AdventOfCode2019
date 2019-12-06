min = 145852
max = 616942


def checkPassword(password):
    lastD = None
    twoSame = False
    sameLen = 0
    for c in str(password):
        if (lastD == None):
            lastD = c
        else:
            if lastD > c:
                return False
            elif c == lastD:
                sameLen += 1
                lastD = c
            else:
                twoSame = twoSame or sameLen == 1
                lastD = c
                sameLen = 0
    twoSame = twoSame or sameLen == 1
    return twoSame
        
counter = 0
for i in range(min, max):
    if checkPassword(i):
        print(i)
        counter += 1
        
print(counter)

#print(checkPassword(111122))