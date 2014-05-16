# -*- coding: utf-8 -*-
"""
Created on Thu May 15 13:31:10 2014

@author: ross
"""

import matplotlib.pyplot as plt
import pandas

data_path = "./data/"

data = pandas.io.parsers.read_csv(data_path + "unimelb_training.csv",low_memory=False)

# <codecell>

data.columns = map(lambda x: x.replace(".",""), data.columns)

plt.figure()
ax = plt.subplot(1,1,1)
ax.plot(range(1,10,1))