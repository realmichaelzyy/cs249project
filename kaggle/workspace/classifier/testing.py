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

# category code and grant status

grouped = data.groupby('GrantCategoryCode')
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# research area and grant status
def broadRFCD(x):
    if pandas.isnull(x):
        return -1
    return int(x/10000)
    
data['RFCDCode1'].apply(lambda x: broadRFCD(x)).nunique()

grouped = data.groupby(data['RFCDCode1'].apply(lambda x: broadRFCD(x)))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

grouped = data.groupby([data['RFCDCode1'].apply(lambda x: broadRFCD(x)),data['ContractValueBandseenoteA']])
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# does how focused the application is matter? (one area versus many)
grouped = data.groupby(data.RFCDPercentage1.apply(lambda x: x >= 80))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

def maxValue(x):
    if(pandas.isnull(x)):
        return -1
    x = x.strip()
    if(len(x) > 1):
        print "what? " + x + "length: " + len(x)
    if(x == "A"):
        return 50000
    elif(ord(x)-ord("A") < 6):
        return (ord(x)-ord("A"))*100000
    elif(ord(x)-ord("F") < 11):
        return (ord(x)-ord("F"))*1000000
    elif(x == "Q"):
        return 100000000
    else:
        return -1
pandas.cut(data.ContractValueBandseenoteA.apply(maxValue),[0,10000,100000,100000001],labels=["small","med","large"])




