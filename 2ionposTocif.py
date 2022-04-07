import datetime
import os


def ionposTocif(filename):
    with open(filename) as f:
        lines = f.readlines()

    atomstype = []
    newlines = []

    for line in lines:
        line_list = line.split()
        # print(line_list)
        
        if line_list[1] in atomstype:
            atomindex += 1
        else:
            atomindex = 1
        
        newline = [line_list[1]+str(atomindex),line_list[1]]
        for i in range(3):
            # print(line_list)
            # print(line_list[2+i])
            newline.append(str(round(float(line_list[2+i]),5)))
        
        newline.append('0.00000  Uiso   1.00')
        
        newline_str = ' '.join(newline)
        newlines.append(newline_str)

    # print(newlines)
    newfilename = ''.join(filename.split('.'))+'.cif'
    with open(newfilename,'w') as f:
        f.write('data_'+filename+'\n')

        now = datetime.datetime.now()
        f.write('_audit_creation_date              '+now.strftime("%Y-%m-%d")+'\n')
        
        f.write('_audit_creation_method            \'by wuwj\''+'\n')
        f.write('_symmetry_space_group_name_H-M    \'P1\''+'\n')
        f.write('_symmetry_Int_Tables_number       1'+'\n')
        f.write('_symmetry_cell_setting            triclinic'+'\n')
        f.write('loop_'+'\n')
        f.write('_symmetry_equiv_pos_as_xyz'+'\n')
        f.write('x,y,z'+'\n')
        
        f.write('_cell_length_a                    7.5578'+'\n')
        f.write('_cell_length_b                    7.5578'+'\n')
        f.write('_cell_length_c                    21.0000'+'\n')
        f.write('_cell_angle_alpha                 90.0000'+'\n')
        f.write('_cell_angle_beta                  90.0000'+'\n')
        f.write('_cell_angle_gamma                 120.0000'+'\n')
        
        f.write("""loop_
    _atom_site_label
    _atom_site_type_symbol
    _atom_site_fract_x
    _atom_site_fract_y
    _atom_site_fract_z
    _atom_site_U_iso_or_equiv
    _atom_site_adp_type
    _atom_site_occupancy\n""")

        for line in newlines:
            f.write(line+'\n')

path = '/Users/wuwj/Nutstore Files/毕设/HER-result/'
os.chdir(path)
for stru in os.listdir(path):
    print(stru)
    for volt in os.listdir(path+stru):
        print(volt)
        if os.path.isdir(path+stru+'/'+volt):
            os.chdir(path+stru+'/'+volt)
            for file in os.listdir('./'):
                if '.ionpos' in file:
                    ionposTocif(file)
            
        
    
# path = '/Users/38439/Nutstore/1/毕设/ionpos/1/0.29'
# filename = '55step.ionpos'

# path0 = 'C:/Users/38439/Nutstore/1/毕设'
# print()
# for stru in os.listdir(path0+'/ionpos'):
#     for pot in  os.listdir(path0+'/ionpos/'+stru):

#         path = path0+'/ionpos/'+stru+'/'+pot
#         os.chdir(path)
#         print(path)

#         files = os.listdir(path)
#         for filename in files:
#             if '.ionpos' in filename:
#                 print(filename)
#                 ionposTocif(filename)
        