import pandas as pd
import os

file = 'CONTCAR'

def readCONTCAR(file):

    with open(file) as con:

        lines = con.readlines()
        lattice_CONTCAR = []
        atomsOrder = []
        atomsNum = []
        typeNum = 0
        type = 0
        ionpos_all = []

        for i,line in enumerate(lines):

            line = line.split()
            if i == 2:
                lattice_CONTCAR.append([float(x) for x in line])
                lattice_CONTCAR.append([float(x) for x in lines[i+1].split()])
                lattice_CONTCAR.append([float(x) for x in lines[i+2].split()])
            
            elif i == 5:
                atomsOrder = line

            elif i == 6:
                atomsNum = [int(x) for x in line]
            
            if i >= 9 and i < (9+sum(atomsNum)):
                typeNum += 1
                if typeNum > atomsNum[type]:
                    type += 1
                    typeNum = 1

                if line[-1] == 'T':
                    fix = 1
                else:
                    fix = 0

                pos = line[:3]
                pos = [('%.7f'%float(x)) for x in pos]
                ionpos = ['ion', atomsOrder[type], pos[0], pos[1], pos[2], str(fix)]

                ionpos_all.append(ionpos)

    # print(lattice_CONTCAR)
    return lattice_CONTCAR,ionpos_all
# for i in ionpos_all:
#     print(i)

def latticeTransfer(lattice_CONTCAR):
    lattice_jdftx = []
    df = pd.DataFrame(lattice_CONTCAR)
    # print(df)
    for i in range(3):
        lattice_jdftx.append(list(df[i]*1.8897259886))
    
    return lattice_jdftx

def writeLatticeAndIonpos(lattice_CONTCAR,ionpos_all):
    lattice_jdftx = latticeTransfer(lattice_CONTCAR)

    with open('in.lattice','w') as la:
        la.write('lattice \\'+'\n')
        for i,row in enumerate(lattice_jdftx):
            row = [ '%.11f'%x for x in row]
            if i != len(lattice_jdftx)-1:
                row.append('\\')
            la.write('  '+'  '.join(row)+'\n')
    
    with open('in.ionpos','w') as ip:
        for i in ionpos_all:
            ip.write(' '.join(i)+'\n')

path = '/Users/wuwj/Nutstore Files/毕设/CHNH-CH2NH结构整理'
for i in range(8):
    os.chdir(path+'/'+str(i+1))
    lattice_CONTCAR,ionpos_all = readCONTCAR('CONTCAR')
    writeLatticeAndIonpos(lattice_CONTCAR,ionpos_all)


     


        


