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


# Set working directories
datapath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework5'
outputpath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework5\output'

# import csv data
os.chdir(datapath)
ivehicles = pd.read_csv('instrumentalvehicles.csv')

# Question 1: regression
X = sm.add_constant(ivehicles[['mpg', 'car']])
model = sm.OLS(ivehicles['price'], X).fit()
print(model.summary())
print('Coefficient of "mpg": {:.2f} (SE = {:.2f})'.format(model.params['mpg'], model.bse['mpg']))


# Question 2: interpretation
print("We should be concerned primarily with omitted variable bias, or equivalently, the possibility that 'mpg' is a confounder correlated with both 'price' and the error term. It's unlikely that we have measurement error or simultaneity in this particular application.")

# Question 3a: IV

# first stage and save fitted values
Z = sm.add_constant(ivehicles[['car','weight']])
firststage = sm.OLS(ivehicles['mpg'], Z).fit()
print(firststage.summary())
mpg_hat = pd.Series(firststage.fittedvalues, name='mpg_hat')

# compute first-stage F-statistic for weight
weight_index = list(Z.columns).index('weight')
f_stat = firststage.wald_test(np.eye(Z.shape[1])[weight_index])
print('First-stage F-statistic for weight: {:.2f}'.format(f_stat.fvalue[0][0]))

# second stage
X_hat = pd.concat([mpg_hat, ivehicles['car']], axis=1)
X_hat = sm.add_constant(X_hat)
secondstage = sm.OLS(ivehicles[['price']], X_hat).fit()
print(secondstage.summary())








