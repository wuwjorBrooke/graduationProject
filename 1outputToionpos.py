import os

def outputToionpos(file):
    with open(file) as f:
        lines = f.readlines()

    n = 0
    i = 0
    elecMini = False
    converge = False

    output = False

    while i < len(lines):
        line = lines[i]
        
        if line[:4] != 'ion ':
            output = False
        elif line[:4] == 'ion ' and not output:
            n += 1
            with open(str(n)+"step.ionpos",'a') as pos:
                pos.write(line) 
            output = True
        elif output:
            with open(str(n)+"step.ionpos",'a') as pos:
                pos.write(line) 
       

        i += 1



  

