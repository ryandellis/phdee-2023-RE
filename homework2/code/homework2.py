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


#KDE plot
sns.kdeplot(data=data, x='electricity', hue='retrofit', bw_adjust=.5)


