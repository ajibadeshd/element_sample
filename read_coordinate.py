# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import getopt
import sys
from periodictable import elements as el


def help():
    print("read_coordinate.py -o <output file name format>")


                
def cp2k():
    pass
    
def read_write(file, cwd):
    
    file_name = os.path.join(cwd,file)
    outdir = os.path.join(cwd, "OUTPUT")
    outfile = os.path.join(outdir, file+".txt")
    fin = open(file_name)
    fout = open(outfile, 'w')
    read = False

    # Check file format type
    for line in fin:
        if "CRYSTAL" in line:
            print(outfile)
            i = 0
            for line in fin:
                print(line+"fahafkafljlj")
                if "# Atom   Kind   Element" in line:
                    read = True
                if 'SUM OF ATOMIC FORCES' in line:
                    break
                if read:
                    print("What is going on")
                    i +=1
                    if i >1:
                        fout.write(line[20:-1])
                        print(fout.write(line[20:-1]))
                        fout.write("\n")
                        print(line[20:-1])
                #fin.close()
                break
            break
            
        


                
'''    # THIS IS FOR CRYSTAL FILE FORMAT       
    if "CARTESIAN FORCES IN HARTREE/BOHR" in line:
        read = True
    if 'RESULTANT FORCE' in line:
        #break
        pass
    if read:
        i +=1
        if i >2:
            fout.write(line[20:-1])
            fout.write("\n")
            print(line[20:-1])
    fin.close()
    #fout.close()
    
    #fin = open(file_name)
    #fout = open(os.path.join(cwd+"/OUTPUT", file+".txt"), 'w')
    fin = open(file_name)
    for line in fin:
        # THIS IS FOR THE FIRST FILE FORMAT
        if 'Total FORCE_EVAL' in line:
            fout.write("ENERGY "+line[61:-1])
            print ("ENERGY "+line[61:-1])
            fout.write("\n")
            break
        
        # THIS IS FOR THE CRYSTAL FILE FORMAT
        if 'Total FORCE_EVAL' in line:
            fout.write("ENERGY "+line[61:-1])
            print ("ENERGY "+line[61:-1])
            fout.write("\n")
            break
    fin.close()
    fout.close()
    print(file_name)
    # Delete an empty files in the OUTPUT FOLDER
    if os.stat(outfile).st_size == 0:
        os.system("rm "+outfile)

    '''
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
    
    # Check if there is an OUTPUT folder already
    if "OUTPUT" in (os.listdir()):
        pass
    else:
        #Create an OUTPUT dir
        os.system("mkdir "+"OUTPUT")
    

    cwd = os.getcwd()  
    # We start looping through the files in the directory
    for file in os.listdir():
        if ".out" in file:
            read_write(file, cwd)
  
if __name__ == "__main__":
    main(sys.argv[1:])
