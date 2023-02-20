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
import statsmodels.api as sm
from stargazer.stargazer import Stargazer as stargazer
from stargazer.stargazer import LineLocation



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
os.chdir(outputpath)

plt.plot(treat_grouped.index, treat_grouped['bycatch'], label='Treated')
plt.plot(control_grouped.index, control_grouped['bycatch'], label='Control')
plt.axvline(x=12.5, color = 'red', linestyle = 'dashed')
plt.legend()
plt.xlabel('Month')
plt.ylabel('Mean Bycatch (kg)')
plt.savefig('image1.png')
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

## Treatment group and treated variables
bycatch['treatgroup'] = bycatch['treated'] 
bycatch['treated2'] = np.where((bycatch['treated'] == 1) & (bycatch['month']>12) & (bycatch['month']<25), 1, 0)
bycatch['treated3'] = np.where((bycatch['month']>24), 1, 0)
bycatch['treated'] = bycatch['treated2'] + bycatch['treated3']
bycatch = bycatch.drop(columns = ['treated2', 'treated3'])


## Setup DID
bycatch = bycatch.reset_index(drop=True)
bycatch3a = bycatch[(bycatch['month'] == 12) | (bycatch['month'] == 13)]
pre = pd.get_dummies(bycatch3a['month'],prefix = 'pre', drop_first = True)
bycatch3a = pd.concat([bycatch3a,pre],axis=1)

yvar3a = bycatch3a['bycatch']
xvar3a = bycatch3a[['treatgroup','treated','pre_13']]

# create a new variable for the interaction of treatment and period
# bycatch3a['treat_post'] = bycatch3a['treated'] * bycatch3a['post']

#X = bycatch3a[['pre','treated','treat_post']]
#y = bycatch3a['bycatch']
#X = sm.add_constant(X)

# fit the regression model
model3a = sm.OLS(yvar3a,sm.add_constant(xvar3a, prepend = False)).fit(cov_type='HC1')


# print the regression results
print(model3a.summary())

# full sample, 3b

yvar3b = bycatch['bycatch']
tvars3b = pd.get_dummies(bycatch['month'],prefix = 'time',drop_first = True)
xvar3b = pd.concat([bycatch[['treatgroup','treated']],tvars3b],axis = 1)

# fit the regression model
model3b = sm.OLS(yvar3b, sm.add_constant(xvar3b, prepend = False)).fit(cov_type='HC1')

# print the regression results
print(model3b.summary())


# now with all covariates, 3c

yvar3c = bycatch['bycatch']
tvars3c = pd.get_dummies(bycatch['month'],prefix = 'time',drop_first = True)
xvar3c = pd.concat([bycatch[['treatgroup','treated','shrimp','salmon','firmsize']],tvars3c],axis = 1)

# fit the regression model
model3c = sm.OLS(yvar3c, sm.add_constant(xvar3c, prepend=False)).fit(cov_type='HC1')

# print the regression results
print(model3c.summary())

# new csv for dataframe
os.chdir(datapath)
bycatch.to_csv('bycatch_stata.csv', index=None, header=True)

# Stargazer
os.chdir(outputpath)
star = stargazer([model3a,model3b,model3c])

star.rename_covariates({'treatgroup':'Treatment Group', 'treated':'Treated', 'pre_13':'Pre-treatment', 'shrimp':'Shrimp', 'salmon':'Salmon', 'firmsize':'Firm Size'})
star.significant_digits(2)
star.show_degrees_of_freedom(False)
star.add_line('Month indicators',['Y','Y','Y'], LineLocation.FOOTER_TOP)

latex_star = star.render_latex()
with open('my_table.tex', 'w') as f:
    f.write(latex_star)




