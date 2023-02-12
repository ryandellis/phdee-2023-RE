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

# Set working directories and seed
datapath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4'
outputpath = r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-RE\homework4\output'

bycatch = pd.read_csv(r'C:\Users\rellis\Dropbox (GaTech)\PHD_AND_COURSES\SPRING 2023\ENVIRO 2\phdee-2023-db\homework4\fishbycatch.csv')

bycatch = pd.wide_to_long(bycatch,('shrimp', 'salmon','bycatch'), i=['firm'], j='month')

bycatch = bycatch.sort_values(by=['firm','month'])