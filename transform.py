#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 12:00:25 2019

@author: robertgrant
"""

import numpy as np
from databaker.framework import *
import pandas as pd
from databakerUtils.writers import v4Writer
import re
import requests
import json
import datetime
import math
from datetime import datetime
import glob
import os


list_of_files = glob.glob('*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

df = pd.read_csv(latest_file)

#isolate 12m growth
pc = df.copy(deep = True)
val = df.copy(deep = True)

#create value col 
pc['value'] = pc['12m growth']
val['value'] = val['Index value']

#explainer col
pc['iphrp-variable'] = 'year-change'
val['iphrp-variable'] = 'index'

pc['variable'] = 'Year-on-year change'
val['variable'] = 'Index'


#concatenatae
full = pd.concat([pc, val])

#tidy
full['mmm-yy'] = full['Date']

#change NI code
full['RegionCode'] = full['RegionCode'].replace('N92000001','N92000002')

#add data marking
full['Data_Marking'] = ''

full.loc[full['value'] == '-', 'Data_Marking'] = '.'
full.loc[full['value'] == '-', 'value'] = ''

v4 = full[['value','Data_Marking','mmm-yy','Date','RegionCode','Geography','iphrp-variable','variable']]
v4.columns = ['V4_1','Data_Marking','mmm-yy','time','admin-geography','geography','housing-rental-prices-variable','variable']

output_file = 'v4-iphrp-' + v4['mmm-yy'][-1:].item().lower() + '.csv'
v4.to_csv(output_file, index = False) 

