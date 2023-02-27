# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 14:52:26 2023

@author: rellis
"""

# Clear all
from IPython import get_ipython
get_ipython().magic('reset -sf')

# Import packages
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import statsmodels.api as sm
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation
import seaborn as sns



# Set working directories
datapath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework6'
outputpath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework6\output'

# import csv data
os.chdir(datapath)
ivehicles = pd.read_csv('instrumentalvehicles.csv')
os.chdir(outputpath)

# define the cutoff and create scatterplot
cutoff = 225
plt.scatter(ivehicles['length'] - cutoff, ivehicles['mpg'], s=20, c='navy', alpha=.5, marker='o')
plt.xlabel('length - cutoff')
plt.ylabel('mpg')
plt.title('Looking for discontinuity')
plt.axvline(x=0, color='red',linestyle='--')
plt.savefig('scatterplot.png')
plt.show()


#%%
