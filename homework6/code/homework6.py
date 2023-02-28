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
import pandas as pd
import matplotlib.pyplot as plt
from rdrobust import rdplot, rdrobust, rdbwselect
from rdd import rdd
import statsmodels.api as sm

#%%
# Set working directories
datapath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework6'
outputpath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework6\output'

# import csv data
os.chdir(datapath)
ivehicles = pd.read_csv('instrumentalvehicles.csv')
os.chdir(outputpath)

#%%
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
# first order polynomial RD

plot1=rdplot(y=ivehicles[['mpg']],x=ivehicles[['length']], c=cutoff, p=1,ci=95, title="RD: 1st-order polynomial")
y = ivehicles[['mpg']]
x = ivehicles[['length']]
rdrobust(y, x, 225)

#%%
plot2=rdplot(y=ivehicles[['mpg']],x=ivehicles[['length']], c=cutoff, p=2,ci=95, title="RD: 2nd-order polynomial")
rdrobust(y, x, 225, p=2)
#%%
plot3=rdplot(y=ivehicles[['mpg']],x=ivehicles[['length']], c=cutoff, p=5,ci=95, title="RD: 5th-order polynomial")
rdrobust(y,x,225,p=5)

#%%
# let's try rdd package
first_stage = rdd.rdd(ivehicles, 'length', 'mpg', cut=225).fit()
print(first_stage.summary())
mpg_hat = pd.Series(first_stage.fittedvalues, name='mpg_hat')

X_hat = pd.concat([mpg_hat, ivehicles['car']], axis=1)
X_hat = sm.add_constant(X_hat)
secondstage = sm.OLS(ivehicles[['price']], X_hat).fit()
print(secondstage.summary())



