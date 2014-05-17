# -*- coding: utf-8 -*-
"""
Created on Thu May 15 13:31:10 2014

@author: ross
"""

import matplotlib.pyplot as plt
import pandas
import numpy

data_path = "./data/"

data = pandas.io.parsers.read_csv(data_path + "unimelb_training.csv",low_memory=False)

data.columns = map(lambda x: x.replace(".",""), data.columns)

# <codecell>

plt.figure()
ax = plt.subplot(1,1,1)
ax.plot(range(1,10,1))

# see the number of uniques for each column
data.apply(lambda x: x.nunique())

# See if there is any relationship between grant size and appliation status
grouped = data.groupby('ContractValueBandseenoteA')
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

grouped = data.groupby('GrantCategoryCode')
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

def broadRFCD(x):
    if pandas.isnull(x):
        return -1
    return int(x/10000)
    
data['RFCDCode1'].apply(lambda x: broadRFCD(x)).nunique()

grouped = data.groupby(data['RFCDCode1'].apply(lambda x: broadRFCD(x)))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

grouped = data.groupby([data['RFCDCode1'].apply(lambda x: broadRFCD(x)),data['ContractValueBandseenoteA']])
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})