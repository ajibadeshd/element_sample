# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import getopt
import sys
#from periodictable import elements as el
import numpy as np


def help():
    print("read_coordinate.py -o <output file name format>")

def CP2K(infile, outfile_path):
    pass


def crystal(infile, outfile):
    print("\n\tFOUND  A CRYSTAL FILE: ", infile)

    
    # Here we want to count the number of times for which the atomic charges
    # are measured because we only want to make use of the last one.
    fin = open( infile)
    charge_count = 0
    for line in fin:
        if "TOTAL ATOMIC CHARGES" in line:
            charge_count +=1
    fin.close()
    ###################################################
    
    fin = open(infile)
    fout = open(outfile, 'w')
    
    coordinate = [] # CARTESIAN COORDINATES - PRIMITIVE CELL
    lattice = [] # DIRECT LATTICE VECTORS CARTESIAN COMPONENTS
    atomic_number = [] 
    force = [] #CARTESIAN FORCES IN HARTREE/BOHR
    atomic_charge = [] # TOTAL ATOMIC CHARGES:
    
    read_lattice = False
    read_coordinate = False
    read_charge = False
    read_force = False

    a = 0
    b = 0
    c = 0
    d = 0
    
    i = 0
    j = 0
    k = 0

    for line in fin:
        ###### Conditions for extracting the coordinates ############
        if "CARTESIAN COORDINATES - PRIMITIVE CELL" in line:
            read_coordinate = True
            a +=1
        if line == "\n":
            read_coordinate = False
        if (read_coordinate == True) and (a ==1):
            i +=1
        if (i >=5) and (read_coordinate == True) and (a ==1):
            coordinate.append([line[12:14], line[18:36], line[38:56], line[58:-1]])

        ########### Conditions for extracting the lattice ###############
        if "DIRECT LATTICE VECTORS CARTESIAN COMPONENTS" in line:
            read_lattice = True
            b +=1
        if line == "\n":
            read_lattice = False
        if (read_lattice == True) and (b ==1):
            j +=1
        if (j >=3) and (read_lattice == True) and (b ==1):
            lattice.append( [line[:21], line[21:42],  line[42:-1]])
        
        ###### Conditions for extracting the Partial charge ############
        if "TOTAL ATOMIC CHARGES" in line:
            read_charge= True
            c +=1
        if "TTTTTTTTT" in line:
            read_charge = False
        if read_charge == True and c == charge_count:
            k +=1
        if (k >1) and (read_charge == True) and (c ==charge_count):
            atomic_charge.append([line[:12], line[12:24], line[24:36],
                                  line[36:48], line[48:60], line[60:-1]])

        ###### Conditions for extracting the Force ############
        if "CARTESIAN FORCES IN HARTREE/BOHR" in line:
            read_force = True
        if line == "\n":
            read_force = False
        if (read_force == True):
            d +=1
        if (d >=3) and (read_force == True):
            force.append([line[21:-1]])
            atomic_number.append(float( line[7:9]))
            

	########## conveting to Partial Charge ##########
    atomic_charge = (np.array(atomic_charge)).astype(float)
    atomic_charge = atomic_charge.flatten()
    partial_charge = atomic_number - atomic_charge
    
    ########## Converting lattice to BOHR ##########
    lattice = (np.array(lattice)) .astype(float)* 1.88973
    
    ########## Convert the coordinate to BOHR ##########
    for i in range (len( coordinate)):
        temp = (np.array(coordinate[i][1:])).astype(float)
        temp = temp * 1.88973
        coordinate[i][1:] = temp
    
	########## Printing to file ##########
    for i in range (len(lattice)):
        print(*lattice[i][0:], file = fout)

    for i in range (len(coordinate)):  
        print(*coordinate[i][0:],
              partial_charge[i],
              "0.0000",
              force[i][0], file = fout
              )
	########## Closing the files ##############
    fin.close()
    fout.close()

    

def read_write(file, cwd):
    infile = os.path.join(cwd,file)
    outfile = file+".txt"
    outdir = os.path.join(cwd, "OUTPUT")
    outfile_path = os.path.join(outdir, outfile)
    fin = open(infile);global crystal_count
    for line in fin:
        if "CP2K" in line:
            fin.close()
            CP2K(infile, outfile_path)
            break
        if "CRYSTAL" in line:
            	crystal_count += 1;crystal(infile, outfile_path);break


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"o:h",["odir =","help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if (opt == '-h') or (opt =="help"):
            help()
            sys.exit()
        elif opt in ("-o", "--odir"):
            output_dir = arg
    
    # Check if there is an OUTPUT folder already exists
    if "OUTPUT" in (os.listdir()):
        pass
    else:
        #Create an OUTPUT dir
        os.system("mkdir OUTPUT")
    
    cwd = os.getcwd()  
    print("\n\tCURRENT WORKING DIRECTORY: ", cwd)
    
    crystal_count = 0
    # We start looping through the files in the directory
    total_files = 0
    for file in os.listdir():
        if ".out" in file:
            read_write(file, cwd)
            total_files +=1
            
    
    print("\n\n\t", " Total file found: ", total_files)
    print("\n\t", " Total Crystal file processed: ", crystal_count )
  
if __name__ == "__main__":
    main(sys.argv[1:])
    ##########https://stackoverflow.com/questions/52448773/the-number-of-times-a-function-gets-called
