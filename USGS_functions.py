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
    ''' This function takes in a dataframe name and outputs a copy of the 
        dataframe with columns removed that only have 'n' unique values. 
        The function prints the name of each column deleted along with 
        the unique value.
    '''
    for name in df_dropping.columns:
        if len(df_dropping[name].unique())<=n:
            print(name+ ' deleted...')
            print(df_dropping[name].unique())
            df_dropping = df_dropping.drop(name, axis=1)
    print('Finished----------------------------------------------------------')
    return df_dropping

def fix_timezones(df,dateTime,timezone):
    ''' This function takes a pandas dataframe, column name, and timezone column
        as an input. The column name must be in a datetime format. The funcion
        outputs a copy of the dataframe with the specified column converted to 
        UTC.
        The timezone column currently must be in the format used by the USGS for
        water quality data, ```EST, EDT, CST, CDT```. Other formats may need to
        be added when data from other state is used.
    '''
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

def merge_scale_delete(df,columns,scale):
    '''
        This function takes a dataframe, column names, and scaling list as an 
        input. The column names are names of columns to be combined and scaled
        by the specified scaling factor. The first column name in the list
        will be used to store the merged columns. The scaling array must be
        the same length as the columns list as the values for scale relate to 
        corresponding column names. The function outputs a copy of the input
        dataframe with the columns merged and extra columns deleted.
        Deleted column names are printed.
    '''
    if len(columns) != len(scale):
        print('List of scales must be the same length as the list of columns')
        # command to exit funciton and give error
    if scale[0] == 1:
        for i in range(1,len(columns)):
            df[columns[0]] = df[columns[0]].combine_first(scale[i]*df[columns[i]])
            print(columns[i]+ ' deleted...')
            df.drop(columns[i], axis=1,inplace=True)
            
        return df
    else:
        print('List the column to keep, scale=1, first for this function.')
        return
    
def outlier_std(column,stds=3,loops=1,plot=False):
    ''' This function trims an input column by a specified number of 
        standard deviations from the mean default of three. The function
        will loop a specified number of times, default of only one.
        This serves to remove outliers from the data however a more robust
        and general algorithm will eventually replace it.
        
        The number of values deleted is printed along with the mean before
        and after outlier reduction.
        
        The plot flag can be used to generate distribution plots for the 
        data before and after outlier reduction.
    '''
    column_int = column.copy()
    for i in range(0,loops):
        std_val = column_int.std(axis = 0)
        mean_val = column_int.mean()

        column_modified = column_int.copy()
        column_modified[column < mean_val - stds*std_val] = np.nan
        column_modified[column > mean_val+stds*std_val]   = np.nan
        column_int = column_modified.copy()
    
    points = column.count() - column_modified.count()
        
    print("Before Mean=%f ----- After Mean=%f" \
                             % (column.mean(),column_modified.mean()))
    print("%d points deleted out of %d total.----------------------" \
                                              % (points, len(column)))
    # if the plot flag is true then print a dist plot before and after
    if(plot):
        plt.figure()
        sns.distplot(column.dropna())
        plt.figure()
        sns.distplot(column_modified.dropna())
    
    column = column_modified
    
    return column
