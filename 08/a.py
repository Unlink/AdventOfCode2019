width = 25
height = 6
layerSize = width*height

with open("input.txt") as f:
    imageData = [int(x) for x in f.read().strip()]
    layers = int(len(imageData)/layerSize)
    
    layerZeros = [(x, imageData[x*layerSize:(x+1)*layerSize]) for x in range(layers)]    
    #print(layerZeros)
    
    minZeroLayer = min(layerZeros, key=lambda x: x[1].count(0))
    print(minZeroLayer[1].count(1) * minZeroLayer[1].count(2))
    
    imageBuffer = [0 for x in range(layerSize)]
    
    for l in range(layers):
        for i in range(layerSize):
            imageBuffer[i] = imageBuffer[i] if imageData[(layers-l-1)*layerSize+i] == 2 else imageData[(layers-l-1)*layerSize+i]
            
            
    for i in range(height):
        for j in range(width):
            print("*" if imageBuffer[i*width + j] == 1 else " ", end ="")
        print()