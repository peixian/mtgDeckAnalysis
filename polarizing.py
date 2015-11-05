#!/usr/bin/env python3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pprint import pprint 
import scipy.stats as stats
import warnings

#reads the filename, spits out a dataframe
#   
def parse(filename):
    return pd.read_csv(filename, usecols=["Card", "Win", "Loss", "Total", "Win%", "Rarity", "CC", "Color"])

#emperical baysian analysis on the dataframe, spits out a dataframe sorted by the best card
def fit(df):
    #need to find the a distribution that fits the data

    winPercent = df[df.Total >= 0]
    print len(winPercent)
    #histogram is relatively normal, so we can use a beta distribution
    (a, b, loc, scale) = stats.beta.fit(winPercent["Win%"], loc = np.mean(winPercent["Win%"]))
    x = np.linspace(0, 1, 100)
    rv = stats.beta(a, b, loc, scale)
    
    #fig, ax = plt.subplots()
    #ax.hist(winPercent["Win%"], bins = 200)
    #ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')
    #ax.set_xlabel("Win%")
    #ax.set_ylabel("Density")
    
    
    #plt.show()
    #not perfect, but close enough?
    
   
    
    df["ebWin%"] = df[["Win", "Total"]].apply(lambda x: (x[0] + a)/(x[1] + a + b), axis=1)
    return (df.sort("ebWin%", ascending=False))
    
def analyze(df, color = "All Colors", rarity = "All rarities", top = 50):
    if (color == "All Colors" and rarity == "All rarities"):
        df = df
    elif (color == "All Colors"):
        df = df[df.Rarity == rarity]
    elif (rarity == "All rarities"):
        df = df[df.Color == color]
    else:
        df = df[(df.Color == color) & (df.Rarity == rarity)]
    df = df[:top].sort("ebWin%", ascending=False)
   
    fig, ax = plt.subplots()
    ax.set_title("BFZ Top {} for {} at {}".format(top, color, rarity))
    sns.set_style("whitegrid")

    ax = sns.stripplot(x = "ebWin%", y="Card", hue="Color",data=df,orient="h")
    ax.legend_.remove()
    plt.tight_layout()
    plt.savefig("Top_{}_for_{}_at_{}.png".format(top, color, rarity))
    
    return df

#main method
#yes I write bad code, thanks for pointing it out python
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
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
                cList = ["All Colors", "White", "Blue", "Black", "Red", "Green", "0"]
                rList = ["All rarities", "C", "U", "R", "M"]
                for c in cList:
                    for r in rList:
                        analyze(fit(df), color = c, rarity = r, top = 15)

            except IOError:
                print("File doesn't exist.\n")
                exit(-1)