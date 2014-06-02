# -*- coding: utf-8 -*-
"""
Created on Thu May 15 13:31:10 2014

@author: ross
"""

import matplotlib.pyplot as plt
import pandas
import numpy
import datetime

data_path = "./data/"

data = pandas.io.parsers.read_csv(data_path + "unimelb_training.csv",low_memory=False)

data.columns = map(lambda x: 'Astar' + x[3:] if x[0:3] == "A.." else x.replace(".",""), data.columns)

# <codecell>

#plt.figure()
#ax = plt.subplot(1,1,1)
#ax.plot(range(1,10,1))

# see the number of uniques for each column
data.apply(lambda x: x.nunique())

#fill in values for contract value and WithPHD fields
#fill in values for contract value and WithPHD fields
a = data.ContractValueBandseenoteA.fillna('-1')
data.loc[:,'ContractValueBandseenoteA_withnull'] = data.loc[:,'ContractValueBandseenoteA']
data.loc[:,'ContractValueBandseenoteA'] = a

a = data.GrantCategoryCode.fillna('-1')
data.loc[:,'GrantCategoryCode_withnull'] = data.loc[:,'GrantCategoryCode']
data.loc[:,'GrantCategoryCode'] = a

a = data.SponsorCode.fillna('-1')
data.loc[:,'SponsorCode_withnull'] = data.loc[:,'SponsorCode']
data.loc[:,'SponsorCode'] = a

for i in range(1,14):
    col = "WithPHD" + str(i)
    a = data[col].fillna('No')
    data.loc[:,col+"_withnull"] = data.loc[:,col]
    data.loc[:,col] = a
    
# fill in values for nonexistant publications    
"""
for i in range(1,14):
    for j in ['Astar','A','B','C']:
        col = j + str(i)
        #print col
        a = data[col].fillna(0)
        data.loc[:,col] = a 
"""
for i in range(1,14):
    for j in ['NumberofUnsuccessfulGrant','NumberofSuccessfulGrant','Astar','A','B','C']:
        col = j + str(i)
        #print col
        a = data[col].fillna(-1)
        data.loc[:,col + "_withnull"] = data.loc[:,col]
        data.loc[:,col] = a    
        
a = data.Startdate.apply(lambda x: datetime.datetime.strptime(x,'%d/%m/%y'))
data.loc[:,'Startdate'] = a



# See if there is any relationship between grant size and appliation status
grouped = data.groupby('ContractValueBandseenoteA')
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# category code and grant status

grouped = data.groupby('GrantCategoryCode')
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# research area and grant status
# research area and grant status
def broadRFCD(x, digits):
    if pandas.isnull(x):
        return -1
    return int(x/(pow(10,floor(log10(x))+1-digits)))
    
data['RFCDCode1'].apply(lambda x: broadRFCD(x,2)).nunique()

grouped = data.groupby(data['RFCDCode1'].apply(lambda x: broadRFCD(x,2)))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

grouped = data.groupby([data['RFCDCode1'].apply(lambda x: broadRFCD(x,2)),data['ContractValueBandseenoteA']])
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# does how focused the application is matter? (one area versus many)
grouped = data.groupby(data.RFCDPercentage1.apply(lambda x: x >= 80))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

def maxValue(x):
    if(pandas.isnull(x) or x == '-1'):
        return -1
    x = x.strip()
    if(len(x) > 1):
        print "what? " + str(x) + "length: " + str(len(x))
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
grouped = data.groupby(pandas.cut(data.ContractValueBandseenoteA.apply(maxValue),[0,100000,1000000,100000001],labels=["small","med","large"]))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})


# Are there any sponsors that are particularly good indicators
grouped = data.groupby('SponsorCode')
result = grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})
result[(result['Total applications'] > 30) & ((result['Success Rate'] > 0.75) | (result['Success Rate'] < 0.25)) ]

# Does having a PhD among the first 3 investigators help?
grouped = data.groupby(data[['WithPHD1','WithPHD2','WithPHD3']].apply(lambda x: \
x['WithPHD1'].strip() == 'Yes' or x['WithPHD2'].strip() == 'Yes' or x['WithPHD3'].strip() == 'Yes',axis=1))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# Does having a PhD among the first 3 investigators help?
grouped = data.groupby(data[['Astar1','A1','Astar2','A2','Astar3','A3']].apply(lambda x: \
logical_or.reduce(x.apply(lambda y: y > 0)).Astar1,axis=1))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# does month matter
grouped = data.groupby(data.Startdate.apply(lambda x: x.month))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

grouped = data.groupby(data.Startdate.apply(lambda x: x.dayofweek))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

# Does having a PhD among the first 3 investigators help?
cols = []
for i in range(1,3):
    for col in ['WithPHD']:
        cols.append(col + str(i))
grouped = data.groupby(data[cols].apply(lambda x: numpy.logical_or.reduce(\
x.apply(lambda y: y.strip() == 'Yes'))[0],axis=1))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

def successful(x, pubThresh, grantThresh):
    pubcols = []
    pubcols += [col for col in x.index if ((col.startswith('A') or col.startswith('B') or col.startswith('C'))\
    and len(col) < 7 and '14' not in col and '15' not in col)]
    #pubcols += [col for col in x.index if col.startswith('B')]
    #pubcols += [col for col in x.index if col.startswith('C') and len(col) < 6]
    successfulGrantsCols = []
    successfulGrantsCols += [col for col in x.index if 'NumberofSuccess' in col and '14' not in col and '15' not in col]
    unsuccessfulGrantsCols = []
    unsuccessfulGrantsCols += [col for col in x.index if 'NumberofUnsuccess' in col and '14' not in col and '15' not in col]
    return(numpy.add.reduce(x[pubcols])[0] >= pubThresh and numpy.add.reduce(x[successfulGrantsCols])[0] >= grantThresh)
    #return(numpy.add.reduce(x[pubcols])[0] > pubThresh )
    
grouped = data.groupby(data.apply(successful,axis=1,args=[1,1]))
grouped['GrantStatus'].agg({'Total applications': len, 'Success Rate': mean})

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
encoded = le.fit_transform(data.ContractValueBandseenoteA)
data['ContractValueBandseenoteA_enc'] = encoded

encoded = le.fit_transform(data.GrantCategoryCode)
data['GrantCategoryCode_enc'] = encoded

encoded = le.fit_transform(data.SponsorCode)
data['SponsorCode_enc'] = encoded

data['Month'] = data.Startdate.apply(lambda x: x.month)
data['DayofWeek'] = data.Startdate.apply(lambda x: x.dayofweek)
data['DayofMonth'] = data.Startdate.apply(lambda x: x.day)

from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score

#cross_val_score(dt,data[['ContractValueBandseenoteA_enc','GrantCategoryCode_enc','SponsorCode_enc']].values,data['GrantStatus'].values,cv=10)

# Add in NoGrants
cols = []
for i in range(1,4):
    for col in ['NumberofUnsuccessfulGrant']:
        cols.append(col + str(i))
data['NoGrants'] = data[cols].apply(lambda x: numpy.logical_and.reduce(x.apply(lambda y: y == 0))[0],axis=1)
encoded = le.fit_transform(data.NoGrants)
data['NoGrants_enc'] = encoded

#mean(cross_val_score(dt,data[['ContractValueBandseenoteA_enc','GrantCategoryCode_enc','SponsorCode_enc','DayofMonth','DayofWeek','NoGrants_enc']].values,data['GrantStatus'].values,cv=10))

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10)
mean(cross_val_score(clf,data[['ContractValueBandseenoteA_enc','GrantCategoryCode_enc','SponsorCode_enc','DayofMonth','DayofWeek','NoGrants_enc']].values,data['GrantStatus'].values,cv=10))

from sklearn.ensemble import ExtraTreesClassifier
clf = ExtraTreesClassifier(n_estimators=10, max_depth=None, min_samples_split=1, random_state=0)
mean(cross_val_score(clf,data[['ContractValueBandseenoteA_enc','GrantCategoryCode_enc','SponsorCode_enc','DayofMonth','DayofWeek','NoGrants_enc']].values,data['GrantStatus'].values,cv=10))

encoded = le.fit_transform(data.Role1)
data['Role1_enc'] = encoded

# See if last day of the month matters ??

# Test if Binarizing it helps
from sklearn.preprocessing import LabelBinarizer
lb = LabelBinarizer()
lb.fit_transform(data['SponsorCode_enc'].values)
sponsorCodeBDF = pandas.DataFrame(lb.fit_transform(data['SponsorCode_enc'].values),columns = map(str,lb.classes_))
newData = pandas.concat([data, sponsorCodeBDF], axis=1)

newData.iloc[:,newData.columns.get_loc('0'):]
mean(cross_val_score(clf,newData[['SponsorCode_enc']].values,data['GrantStatus'].values,cv=20))
mean(cross_val_score(clf,newData.iloc[:,newData.columns.get_loc('0'):].values,data['GrantStatus'].values,cv=20))



