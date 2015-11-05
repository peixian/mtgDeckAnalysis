#!/usr/bin/env python3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json 
from pprint import pprint 

#reads the filename, adds the colors, spits out a dataframe
#   
def parse(filename):
    df = pd.read_csv(filename)
    with open("BFZ.json") as json_data:
        data = json.load(json_data)
    
   

#emperical baysian analysis on the dataframe


#main method

if __name__ == '__main__':
    from sys import argv, exit
    usage = """
    USAGE: python {0} filesheet
    
    WHERE: filesheet is the name of the xlsx of interest
    (note that this is currently only designed for the sheet of bfz that was posted on /r/lrcast, see source.txt for more details)
    """
    
    if (len(argv) != 2):
        print(usage.format(argv[0]))
        
    else:
        try: 
            df = parse(argv[1])
            #print(df) 
            
        except IOError:
            print("File doesn't exist.\n")
            exit(-1)