from lib2to3.pgen2.token import AT
import os
from re import A
# cif文件的位置
# path = 'D:/LAB/ACE-Cu/+H2O/CN-CHN/CH3CN/'

# path = 'D:/LAB/ACE-Cu/+H2O/CHN-CHNH/CHNH'
# path = 'D:/LAB/ACE-Cu/+H2O/CHN-CHNH/CHN'

# path = 'D:/LAB/ACE-Cu/+H2O/CH2NH-CH2NH2/OH-CH2NH2'
# path = 'D:/LAB/ACE-Cu/+H2O/CH2NH-CH2NH2/H2O-CH2NH'

# path = 'D:/LAB/ACE-Cu/+H2O/CHNH-CH2NH/H2O-CHNH'

# path = 'D:/LAB/ACE-Cu/+H2O/CH2NH2desorption/CH2NH2-H2O'
# path = 'D:/LAB/ACE-Cu/+H2O/CH2NH2desorption/mol-CH2NH2-H2O'
# path = 'D:/LAB/ACE-Cu/+H2O/mol-CN-H2O'
# path = 'D:\LAB\ACE-Cu\参考CHE模型做反应自由能变化曲线\PAW-PW91\moleAdop'

# path = 'D:/LAB/ACE-Cu/结构优化/NotAdsorb'
# path = 'C:/Users/38439/Desktop'
# path = "D:/LAB/ACE-Cu/searchforTS/HER/"
path = '0.29--opt.cif'




#晶格参数
# lat =  "20.0000000000000000  0.0000000000000000  0.0000000000000000 \n"
# lat += " 0.0000000000000000 20.0000000000000000  0.0000000000000000 \n"
# lat += " 0.0000000000000000  0.0000000000000000 20.000000000000000 "

# lat =  " 7.5578400000000000 0.0000000000000000 0.0000000000000000 \n"
# lat += "-3.7789200000000000 6.5452800000000000 0.0000000000000000 \n"
# lat += " 0.0000000000000000 0.0000000000000000 21.000000000000000 "

lat = " 6.5452800000000000 -3.7789200000000000 0.0000000000000000 \n"
lat += " 0.0000000000000000 7.5578400000000000 0.0000000000000000 \n"
lat += " 0.0000000000000000 0.0000000000000000 21.000000000000000 "

#PAW-PW91
# lat =  " 7.7054800000000000 0.0000000000000000 0.0000000000000000 \n"
# lat += "-3.8527400000000000 6.6731400000000000 0.0000000000000000 \n"
# lat += " 0.0000000000000000 0.0000000000000000 21.291500000000000 "
# slab的元素
slab = 'Cu'
# 没有固定的slab层数/
first_fix_lay = 3
# AtomOrder = ["Cu","C","N","H","O"]
# AtomOrder = ["Cu"]
# AtomOrder = ["Cu","C","N","H"]
# AtomOrder = ["Cu","H","O"]
AtomOrder = ['C','H','N','Cu','O']


def pre_lines(line):
    i_line = line.split(' ')
    f_line = []
    for i in i_line:
        if i != '':
            f_line.append(i)
    return f_line


def listTostr(line):
    j = ''
    for i in line:
        if type(i) is float:
            if i > 0 or "{:.6f}".format(i) == '0.000000':
                i = ' ' + "{:.6f}".format(i)
            else:
                i = "{:.6f}".format(i)
        j = j + str(i)+' '
    return j


def cifToPOSCAR(filename,lat,slab,first_fix_lay,AtomOrder):
    
    with open(filename, 'r') as f:
        lines = f.readlines()

    pos = {}
    z_slab = []
    in_loop = False

    for line in lines:
        if line.find("_atom_site_occupancy") != -1:
            in_loop = True
            continue
        if in_loop:
            if line.find("loop_") != -1:
                break
            j = line.strip().split()
            xyz = (float(j[2]), float(j[3]), float(j[4]))

            if j[1] == slab and float(j[4]) not in z_slab:
                z_slab.append(float(j[4]))
            if j[1] in pos:
                pos[j[1]].append(xyz)
            else:
                pos[j[1]] = [xyz]
    
    all_num = []
    # atoms = list(pos.keys())
    atoms = AtomOrder
    for i in atoms:
        num = len(pos[i])
        all_num.append(num)
    
    if slab in pos.keys():
        pos[slab].sort(key=lambda x: -x[2]) # sorted by z lable 
    # print(list(pos.keys()),"key")
    # print(atoms,"atoms")
    
    

    with open(filename+'.POSCAR', 'w') as POS:
        POS.write('XYZ '+listTostr(atoms)+'\n')
        POS.write('1.00000000000000'+'\n')
        POS.write(lat+'\n')

        POS.write(listTostr(atoms)+'\n')
        POS.write(listTostr(all_num)+'\n')

        POS.write('Selective dynamics'+'\n'+'Direct'+'\n')

        slab_layer = 0
        z = [] # store previous layer z label
        for i in atoms:
            for j in pos[i]:
                if slab in pos.keys():
                    
                    if i == slab:
                        if z == []:
                            z.append(j[2])
                            slab_layer = slab_layer + 1
                        else:
                            zz = list(map(lambda x: x-j[2],z))
                            new_z = list(map(abs,zz))
                            new_z.sort()
                            min_z = new_z[0]
                            if min_z > 0.05:
                                slab_layer = slab_layer + 1
                                z.append(j[2])
                        # print(z)
                        if slab_layer >= first_fix_lay:
                            POS.write(listTostr(j)+'F F F'+'\n')
                        else:
                            POS.write(listTostr(j)+'T T T'+'\n')
                    else:
                        POS.write(listTostr(j)+'T T T'+'\n')
                       
                else:
                    POS.write(listTostr(j)+'T T T'+'\n')
    

cifToPOSCAR("0.29--opt.cif",lat,slab,first_fix_lay,AtomOrder)
# os.chdir(path)
# all_file = os.listdir(path)
# for filename in all_file:
    
#     if filename[-3:] == "cif":
    
#         cifToPOSCAR(filename,lat,slab,first_fix_lay,AtomOrder)
