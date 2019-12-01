

def calculateAllFuel(mass): 
    calculated = int(mass/3)-2;
    if (calculated < 0):
        calculated = 0
    if (calculated > 0):
        calculated = calculated + calculateAllFuel(calculated)
    return calculated

with open("input.txt", "r") as f:
    #sum = sum([(int(int(x)/3)-2) for x in f if x.strip() != ""])
    sum = sum([calculateAllFuel(int(x)) for x in f if x.strip() != ""])
    print(sum)