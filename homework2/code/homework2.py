# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:17:57 2023

@author: rellis
"""
import os
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import scipy
from scipy import stats
import matplotlib
import matplotlib.pyplot as pp
import math
import seaborn as sns
import statsmodels.api as sm
from tabulate import tabulate




data = pd.read_csv("C:\\Users\\rellis\\Dropbox (GaTech)\\PHD_AND_COURSES\\SPRING 2023\\ENVIRO 2\\phdee-2023-db\\homework2\\kwh.csv")
data.head()

#define treatment 
treated = data[data.retrofit == 1]
control = data[data.retrofit == 0]

#t-tests
test_elec = stats.ttest_ind(treated.electricity, control.electricity,).pvalue
test_sqft = stats.ttest_ind(treated.sqft, control.sqft).pvalue
test_retro = stats.ttest_ind(treated.retrofit, control.retrofit).pvalue
test_temp = stats.ttest_ind(treated.temp, control.temp).pvalue

tests = np.around([test_elec, test_sqft, test_retro, test_temp], decimals=3)
tests = pd.DataFrame(tests)

zero = [' ',' ',' ',' ']
zero = pd.DataFrame(zero)

d1_mean = treated.mean()
d1_std = treated.std()
d0_mean = control.mean()
d0_std = control.std()

d1_mean = d1_mean.map('{:.2f}'.format)
d1_std = d1_std.map('({:.2f})'.format)
d0_mean = d0_mean.map('{:.2f}'.format)
d0_std = d0_std.map('({:.2f})'.format)

#using tabulate
"""
table = [["Electricity", treated.electricity.mean(), control.electricity.mean(), test_elec], ["Square Footage", treated.sqft.mean(), control.sqft.mean(), test_sqft], ["Retrofit", '1', '0', '-'], ["Temperature", treated.temp.mean(), control.temp.mean(), test_temp]]

headers = ["Variable", "Treatment Sample Mean", "Control Sample Mean", "P-value, difference-in-means"]

from tabulate import tabulate
print(tabulate(table, headers, tablefmt="grid"))
"""

#other way
rownames = pd.concat([pd.Series(['Electricity','Square Footage', 'Retrofit', 'Temperature',]),pd.Series([' ',' ',' ',' '])],axis = 1).stack()

colnames = pd.concat([pd.Series(['Treatment', 'Control', 'Diff-in-means'])])

col0 = pd.concat([d1_mean,d1_std],axis=1).stack()
col0.index = rownames

col1 = pd.concat([d0_mean,d0_std],axis=1).stack()
col1.index = rownames

col2 = pd.concat([tests, zero],axis=1).stack()
col2.index = rownames


df_col0 = pd.DataFrame(col0)
df_col1 = pd.DataFrame(col1)
df_col2 = pd.DataFrame(col2)

df_all = pd.concat([df_col0, df_col1, df_col2], axis=1)
df_all.columns = colnames


## Output to LaTeX folder
os.chdir("C:\\Users\\rellis\\Dropbox (GaTech)\\PHD_AND_COURSES\\SPRING 2023\\ENVIRO 2\\phdee-2023-RE\\homework2\output")

df_all.style.to_latex('comp_of_means.tex')

headers = ["Variable", "Treatment Sample Mean", "Control Sample Mean", "P-value, difference-in-means"]

print(tabulate(df_all, headers, tablefmt="grid"))
print(tabulate(df_all, headers, tablefmt="latex_longtable"))



#KDE plot
sns.kdeplot(data=data, x='electricity', hue='retrofit', bw_adjust=.5)

#OLS from scratch
truexvars = np.array([data.sqft, data.retrofit, data.temp, np.ones(1000)])
truexvars = truexvars.transpose()
trueyvar = np.array(data.electricity)

betahat = np.dot(np.linalg.inv(np.dot(truexvars.T, truexvars)),np.dot(truexvars.T, trueyvar))

print(betahat)


#simulated OLS
beta = [1, .1, .5, .4]

def f(beta):
    return np.sum((trueyvar - np.dot(truexvars, beta))**2)

res = scipy.optimize.minimize(f, beta)
print(res)


#canned OLS
results = sm.formula.ols('electricity ~ sqft + retrofit + temp', data=data).fit()
print(results.summary())

#creating table


rownames2 = pd.concat([pd.Series(['sqft','retrofit','temp','Intercept'])])
colnames2 = pd.concat([pd.Series(['By hand', 'Simulation', 'Canned'])])

df_betahat = pd.DataFrame(betahat)
df_betahat.index = rownames2
df_res = pd.DataFrame(res.x)
df_res.index = rownames2
df_results = pd.DataFrame(results.params)

df_betahat.reindex_like(df_results)
df_res.reindex_like(df_results)

df_betahat = df_betahat.sort_index()
df_res = df_res.sort_index()

df_3b = pd.concat([df_betahat, df_res, df_results], axis = 1)
df_3b.columns = colnames2

print(tabulate(df_3b, headers = colnames2, tablefmt='latex_longtable'))

df_3b.style.to_latex('OLS_methods.tex')