#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:36:55 2017

@author: shaffer
"""
import pytz
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def drop_constant_cols(df_dropping,n=1):
    ''' This function takes in a data frame name and outputs the dataframe with
        columns removed that only have 'n' unique value. The function prints
        the name of each column deleted along with the unique value.'''
    for name in df_dropping.columns:
        if len(df_dropping[name].unique())<=n:
            print(name+ ' deleted...')
            print(df_dropping[name].unique())
            df_dropping = df_dropping.drop(name, axis=1)
    print('Finished----------------------------------------------------------')
    return df_dropping

def fix_timezones(df,dateTime,timezone):    
    est = pytz.timezone('Etc/GMT+5')
    edt = pytz.timezone('Etc/GMT+4')
    cst = pytz.timezone('Etc/GMT+6')
    cdt = pytz.timezone('Etc/GMT+5')
    
    df.loc[df[timezone]=='EST',[dateTime]] = \
          df.loc[df[timezone]=='EST',['dateTime']].apply(
                  lambda x: x.dt.tz_localize(est).dt.tz_convert('UTC'))
    
    df.loc[df[timezone]=='EDT',[dateTime]] = \
          df.loc[df[timezone]=='EDT',['dateTime']].apply(
                  lambda x: x.dt.tz_localize(edt).dt.tz_convert('UTC'))
          
    df.loc[df[timezone]=='CST',[dateTime]] = \
          df.loc[df[timezone]=='CST',['dateTime']].apply(
                  lambda x: x.dt.tz_localize(cst).dt.tz_convert('UTC'))

    df.loc[df[timezone]=='CDT',[dateTime]] = \
          df.loc[df[timezone]=='CDT',['dateTime']].apply(
                  lambda x: x.dt.tz_localize(cdt).dt.tz_convert('UTC'))
    
    df = df.drop(timezone,axis=1)
    print('Timezone column: '+timezone+' deleted...\n')
    return df

def merge_scale_delete(df,column,scale):
    if scale[0] == 1:
        for i in range(1,len(column)):
            df[column[0]] = df[column[0]].combine_first(scale[i]*df[column[i]])
            print(column[i]+ ' deleted...')
            df.drop(column[i], axis=1,inplace=True)
            
        return df
    else:
        print('List the column to keep, scale=1, first for this function.')
        return
    
def outlier_std(column,stds=3,loops=1,plot=False):
    '''This function trims an input column by a specified number of 
       standard deviations from the mean default of three.'''
    column_int = column.copy()
    for i in range(0,loops):
        std_val = column_int.std(axis = 0)
        mean_val = column_int.mean()

        column_modified = column_int.copy()
        column_modified[column < mean_val - stds*std_val] = np.nan
        column_modified[column > mean_val+stds*std_val]   = np.nan
        column_int = column_modified.copy()
    
    points = column.count() - column_modified.count()
        
    print("Before Mean=%f ----- After Mean=%f" % (column.mean(),column_modified.mean()))
    print("%d points deleted out of %d total.----------------------" % (points, len(column)))
    
    if(plot):
        plt.figure()
        sns.distplot(column.dropna())
        plt.figure()
        sns.distplot(column_modified.dropna())
    
    column = column_modified
    
    return column
