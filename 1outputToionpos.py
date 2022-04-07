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
        # if "Electronic minimization" in line:
        #     elecMini = True
        # if "Converged" in line:
        #     # print(line)
        #     converge = True
        #     n += 1
        
        # if elecMini and converge and line[:3] == "ion":
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
        
        # if "Forces in Lattice coordinates" in line:
        #     elecMini, converge = False, False

        i += 1

path = '/Users/wuwj/Nutstore Files/毕设/HER-result/'
os.chdir(path)
for stru in os.listdir(path):
    print(stru)
    for volt in os.listdir(path+stru):
        print(volt)
        if os.path.isdir(path+stru+'/'+volt):
            os.chdir(path+stru+'/'+volt)
            for file in os.listdir('./'):
                if '.out' in file:
                    outputToionpos(file)

# path0 = 'C:/Users/38439/Desktop/ionpos/1/0.76'
# os.chdir(path0)
# outputToionpos('output.out')
# print(os.getcwd())
# print()
# for stru in os.listdir(path0+'/ionpos'):
#     for pot in  os.listdir(path0+'/ionpos/'+stru):
#         path = path0+'/ionpos/'+stru+'/'+pot
#         os.chdir(path)
#         print(path)
#         outputToionpos('output.out')
        
        

  

