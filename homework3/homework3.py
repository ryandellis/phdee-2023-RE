# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 13:17:57 2023

@author: rellis
"""
import os
import scypi
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