# with open("input.txt") as f:
    # program = [int(x) for x in f.read().split(",")]
    # print(program)
    
    # program[1] = 12
    # program[2] = 2
    
    # ip = 0
    # while (program[ip] != 99):
        # if (program[ip] == 1):
            # program[program[ip+3]] = program[program[ip+1]] + program[program[ip+2]]
        # elif (program[ip] == 2):
            # program[program[ip+3]] = program[program[ip+1]] * program[program[ip+2]]
        # else:
            # print("Error op code: " + str(program[ip]))
        # ip += 4
        
    # print(program)
    
for i in range(100):
    for j in range(100):
        with open("input.txt") as f:
            program = [int(x) for x in f.read().split(",")]
            #print(program)
            
            program[1] = i
            program[2] = j
            
            ip = 0
            while (program[ip] != 99):
                if (program[ip] == 1):
                    program[program[ip+3]] = program[program[ip+1]] + program[program[ip+2]]
                elif (program[ip] == 2):
                    program[program[ip+3]] = program[program[ip+1]] * program[program[ip+2]]
                else:
                    print("Error op code: " + str(program[ip]))
                ip += 4
                
            #print(program)
            
            if (program[0] == 19690720):
                print("End: "+str(100*i+j))