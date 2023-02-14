# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 11:26:04 2023

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


# Set working directories and seed
datapath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4'
outputpath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4\output'

bycatch = pd.read_csv(r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-db\homework4\fishbycatch.csv')

# reshaping, sorting
bycatch = pd.wide_to_long(bycatch,('shrimp', 'salmon','bycatch'), i=['firm'], j='month')
bycatch = bycatch.sort_values(by=['firm','month'])

# Add a constant to the dataframe
bycatch = sm.add_constant(bycatch)

# treatment and control
treat = bycatch[bycatch['treated']==1]
treat = treat.sort_values(by=['firm','month'])
control = bycatch[bycatch['treated']==0]
control = control.sort_values(by=['firm','month'])
treat = treat.reset_index()
control = control.reset_index()

# monthly means
treat_grouped = treat.groupby('month').mean()
control_grouped = control.groupby('month').mean()

# plotting treatment and control by monthly means
plt.plot(treat_grouped.index, treat_grouped['bycatch'], label='Treated')
plt.plot(control_grouped.index, control_grouped['bycatch'], label='Control')

plt.legend()
plt.xlabel('Month')
plt.ylabel('Mean Bycatch (kg)')

plt.show()


# difference-in-differences (2-month period around treatment), q2
bycatch = bycatch.reset_index()

treat_before = treat[treat['month'] ==12].mean()
treat_after = treat[treat['month'] ==13].mean()
control_before = control[control['month'] ==12].mean()
control_after = control[control['month'] ==13].mean()

dd_estimate_1 = (treat_after['bycatch'] - treat_before['bycatch']) - (control_after['bycatch'] - control_before['bycatch'])

print(dd_estimate_1)


# indicator variables, 3a

bycatch = bycatch.reset_index(drop=True)
bycatch3a = bycatch[(bycatch['month'] == 12) | (bycatch['month'] == 13)]
bycatch3a = bycatch3a.reset_index(drop=True)
bycatch3a['pre'] = (bycatch3a['month']==12).astype(int)
bycatch3a['post'] = (bycatch3a['month']==13).astype(int)



# create a new variable for the interaction of treatment and period
bycatch3a['treat_post'] = bycatch3a['treated'] * bycatch3a['post']

X = bycatch3a[['pre','treated','treat_post']]
y = bycatch3a['bycatch']
X = sm.add_constant(X)

# fit the regression model
model3a = sm.OLS(y, X).fit(cov_type='HC1')


# print the regression results
print(model3a.summary())

# full sample, 3b

bycatch['pre'] = (bycatch['month'] < 13).astype(int)
bycatch['post'] = (bycatch['month'] >= 13).astype(int)
bycatch['treat_post'] = bycatch['treated'] * bycatch['post']

X = bycatch[['pre','treated','treat_post']]
y = bycatch['bycatch']
X = sm.add_constant(X)

# fit the regression model
model3b = sm.OLS(y, X).fit(cov_type='HC1')

# print the regression results
print(model3b.summary())


# now with all covariates, 3c

X = bycatch[['pre','treated','treat_post','firmsize','shrimp','salmon']]
y = bycatch['bycatch']
X = sm.add_constant(X)

# fit the regression model
model3c = sm.OLS(y, X).fit(cov_type='HC1')

# print the regression results
print(model3c.summary())





