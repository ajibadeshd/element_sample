# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import getopt
import sys



def help():
    print("read_coordinate.py -o <output file name format>")
    
def read_write(file, cwd):

    #fin = open("/home/saheed/Downloads/Si_bulk8.out")
    file_name = cwd+"/"+file
    fin = open(file_name)
    read = False
    
    outfile = os.path.join(cwd, "OUTPUT/")
    print(outfile)
    
    fout = open(os.path.join(cwd+"/OUTPUT", file+".txt"), 'w')
    #fout = open(file_name+".txt", 'w')
    
    i = 0
    for line in fin:
        if "# Atom   Kind   Element" in line:
           read = True
        if 'SUM OF ATOMIC FORCES' in line:
            break
        if read:
            i +=1
            if i >1:
                fout.write(line[20:-1])
                fout.write("\n")
                print(line[20:-1])
    fin.close()
    
    #fin = open(file_name)
    fin = open("/home/saheed/Downloads/Si_bulk8.out")
    for line in fin:
        if 'Total FORCE_EVAL' in line:
            fout.write("ENERGY "+line[61:-1])
            print ("ENERGY "+line[61:-1])
            fout.write("\n")
            break
    fin.close()
    fout.close()


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
    
    #Create an OUTPUT dir
    os.system("mkdir "+"OUTPUT")
    
    cwd =  os.getcwd()
    
    # We start looping through the files in the directory
    for file in os.listdir( cwd):
        read_write(file, cwd)
    
if __name__ == "__main__":
   main(sys.argv[1:])
