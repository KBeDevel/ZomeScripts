#! /usr/bin/env python3
#! c:/Python/ python

"""
AUTHOR:  KBeDeveloper (https://github.com/KBeDeveloper), (https://gitlab.com/KBeDeveloper)
DATE:    October 12, 2019
LICENSE: MIT
"""

import os
import sys
import json
from ruamel.yaml import YAML

def printHelp():
    print('\nScript usage:\n')
    print(' [ -in | --in | in ]          YAML file path            Ex:  -in /path/to/file')
    print(' [ -out | --out | out ]       JSON file path            Ex: -out /path/to/file')
    print('\n')

try:

    sh_params = (sys.argv)
    innerFile = None
    outerFile = None

    if len(sh_params) is 1:

        print("\nNo files specified!\n")
        printHelp()
        quit()
        

    for index in range(len(sh_params)): # Get CLI params

        if sh_params[index] == '-help' or sh_params[index] == '--help' or sh_params[index] == 'help':

            printHelp()

        if sh_params[index] == '-in' or sh_params[index] == '--in' or sh_params[index] == 'in':

            innerFile = sh_params[index+1]

        if sh_params[index] == '-out' or sh_params[index] == '--out' or sh_params[index] == 'out':

            outerFile = sh_params[index+1]


    if innerFile is not None:

        ext = os.path.splitext(innerFile)[-1].lower()

        if ext is not ".yml" or ext is not ".yaml":

            print("The file specified is not a YAML file")

        else:
            if outerFile is not None:

                yamlFile = open(innerFile, mode='r')

                if yamlFile is None or len(str(yamlFile)) is 0 : raise Exception("YAML file is empty")

                try:

                    yaml = YAML(typ='safe')
                    
                    data = yaml.load(yamlFile)

                    with open(outerFile, 'w') as outfile :
                        
                        json.dump(data, outfile, indent=4)

                    print("Script finished")

                except : print("Error dumping items")

                finally : quit()
                
            else:

                print("JSON file not specified")            

    else:
        print("YAML file not specified")    

except Exception as error :
    
    print(error)

finally :
    
    quit()
