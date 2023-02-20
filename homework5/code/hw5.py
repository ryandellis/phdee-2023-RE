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
from stargazer.stargazer import Stargazer


# Set working directories
datapath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework5'
outputpath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework5\output'

# import csv data
os.chdir(datapath)
ivehicles = pd.read_csv('instrumentalvehicles.csv')

##############################################################################
# Question 1: naive regression
X = sm.add_constant(ivehicles[['mpg', 'car']])
model = sm.OLS(ivehicles['price'], X).fit()
print(model.summary())
print('Coefficient of "mpg": {:.2f} (SE = {:.2f})'.format(model.params['mpg'], model.bse['mpg']))

##############################################################################
# Question 2: interpretation
print("We should be concerned primarily with omitted variable bias, or equivalently, the possibility that 'mpg' is a confounder correlated with both 'price' and the error term. It's unlikely that we have measurement error or simultaneity in this particular application.")

##############################################################################
# Question 3: IV
# Part a)
# first stage and save fitted values
Z_a = sm.add_constant(ivehicles[['car','weight']])
firststage_a = sm.OLS(ivehicles['mpg'], Z_a).fit()
print(firststage_a.summary())
mpg_hat_a = pd.Series(firststage_a.fittedvalues, name='mpg_hat_a')

# compute first-stage F-statistic for weight
weight_index_a = list(Z_a.columns).index('weight')
f_stat_a = firststage_a.wald_test(np.eye(Z_a.shape[1])[weight_index_a])
print('First-stage F-statistic for weight: {:.2f}'.format(f_stat_a.fvalue[0][0]))

# second stage
X_hat_a = pd.concat([mpg_hat_a, ivehicles['car']], axis=1)
X_hat_a = sm.add_constant(X_hat_a)
secondstage_a = sm.OLS(ivehicles[['price']], X_hat_a).fit()
print(secondstage_a.summary())

##############################################################################
# Part b)
# construct weight_sq
ivehicles['weight_sq'] = ivehicles['weight']**2

# first stage and save fitted values
Z_b = sm.add_constant(ivehicles[['car','weight_sq']])
firststage_b = sm.OLS(ivehicles['mpg'], Z_b).fit()
print(firststage_b.summary())
mpg_hat_b = pd.Series(firststage_b.fittedvalues, name='mpg_hat_b')

# compute first-stage F-statistic for weight
weight_index_b = list(Z_b.columns).index('weight_sq')
f_stat_b = firststage_b.wald_test(np.eye(Z_b.shape[1])[weight_index_b])
print('First-stage F-statistic for weight_sq: {:.2f}'.format(f_stat_b.fvalue[0][0]))

# second stage
X_hat_b = pd.concat([mpg_hat_b, ivehicles['car']], axis=1)
X_hat_b = sm.add_constant(X_hat_b)
secondstage_b = sm.OLS(ivehicles[['price']], X_hat_b).fit()
print(secondstage_b.summary())

##############################################################################
# Part c)

# first stage and save fitted values
Z_c = sm.add_constant(ivehicles[['car','height']])
firststage_c = sm.OLS(ivehicles['mpg'], Z_c).fit()
print(firststage_c.summary())
mpg_hat_c = pd.Series(firststage_c.fittedvalues, name='mpg_hat_c')

# compute first-stage F-statistic for height
height_index_c = list(Z_c.columns).index('height')
f_stat_c = firststage_c.wald_test(np.eye(Z_c.shape[1])[height_index_c])
print('First-stage F-statistic for height: {:.2f}'.format(f_stat_c.fvalue[0][0]))

# second stage
X_hat_c = pd.concat([mpg_hat_c, ivehicles['car']], axis=1)
X_hat_c = sm.add_constant(X_hat_c)
secondstage_c = sm.OLS(ivehicles[['price']], X_hat_c).fit()
print(secondstage_c.summary())

##############################################################################





