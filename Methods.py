"""
this file is for creating methods that we will use in the main file
first class is for the cleaning the data and second class is for visualizing the data 
the third class is for storing data into database

"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import re
class Modify:
    #this constructor takes the dataframe and the list that have columns name that you want to modify
    def __init__ (self,df:pd.DataFrame):
        self.df = df
    
    #there are shifting between three columns
    def Fix_shifting(self) ->pd.DataFrame:
        df = self.df.copy()
        index= df[(df['Transmission'] != 'أتوماتيك\u200e') & (df['Transmission'] != 'مانيوال') & (df['Transmission'] !='DSG')].index
        color = ['بترولي', 'أسود', 'بني', 'فضي', 'أبيض', 'رمادي', 'احمر',
       'الأزرق الداكن', 'أزرق', 'فيراني', 'برونزي', 'احمر غامق', 'شمبان',
       'سماوى', 'أخضر', 'ذهبي', 'موكا', 'زيتوني', 'برتقالى', 'اخضر غامق',
       'بنفسجي', 'بيج', 'اصفر', 'باذنجاني']
        for i in index:
           if df.at[i,'Location'] in color: 
              df.at[i,'Color'] = df.at[i,'Location']
           if df.at[i,'Transmission'] not in ['أتوماتيك\u200e','مانيوال','DSG']:
              df.at[i,'Location'] = df.at[i,'Transmission']
           if df.at[i,'Milage'] in ['أتوماتيك\u200e','مانيوال']:
              df.at[i,'Transmission'] = df.at[i,'Milage']
              df.at[i,'Milage'] = None
        return df

    #our data has a string inside int column and we want to extract this string
    def Extract_int(self,col_names : list) -> pd.DataFrame:
        df_copy  = self.Fix_shifting()
        for col_name in col_names:
           num_of_non_int = 0
           list = []
           df_copy[col_name] = df_copy[col_name].astype(str)
           for value in df_copy[col_name]:
               match = re.match(r'\d{1,3}(?:,\d{3})*',value)
               if match:
                  number = match.group().replace(',','')
                  list.append(number)
               else:
                  list.append(None)
                  num_of_non_int+=1
           print(f"The Number of values that don't have a number is : {num_of_non_int}\n")
           df_copy[col_name] = list
        return df_copy
      
    #getting the mean of every year 
    def getting_mean_of_Mileage_for_every_year(self,col_year : str, col_Mileage : str) -> pd.DataFrame:
        df_copy = self.Extract_int([col_Mileage])
        list_years = sorted(df_copy[col_year].unique())
        list_means = []
        for year in  list_years:
            list_means.append(df_copy[col_Mileage].loc[(df_copy[col_year]==year)&(df_copy[col_Mileage].notna())].astype('int64').mean().round())
        dict = {col_year:list_years,col_Mileage:list_means}
        return pd.DataFrame(dict)
    
    #inside this data there are null values about these null values we will fill it with the mean of each car according to the year
    def fill_na_mileage(self,df :pd.DataFrame,col_year_name : str, col_mileage : str) -> pd.DataFrame:
        df_copy = df.copy()
        list_years = df_copy['Year'].unique()
        list_index_na = df_copy.loc[df_copy[col_mileage].isna()].index.to_list()
        for Year in list_years:
           for index_Na in list_index_na:
               if df_copy.loc[index_Na, 'Year'] == Year:
                   mean_milage = df_copy.loc[(df_copy['Year'] == Year) & (df_copy['Milage'].notna()), 'Milage'].astype('int64').mean().round()
                   df_copy.loc[index_Na, 'Milage'] = mean_milage
        df_copy[col_mileage] = df_copy[col_mileage].astype('int64')
        return df_copy

    def fill_zero_mileage(self,df : pd.DataFrame,col_year : str , col_mileage :str) -> pd.DataFrame:
        df_copy = df
        df_means = self.getting_mean_of_Mileage_for_every_year(col_year,col_mileage)
        index_zero_values_mileage = df_copy.loc[df_copy['Milage']==0].index.to_list()
        for year in df_means['Year']:
           for index in index_zero_values_mileage:
              if df_copy.loc[index, 'Year'] == year:
                mean_milage = df_means.loc[df_means['Year'] == year, 'Milage'].iloc[0]  # Get the mean Milage for the year
                df_copy.loc[index, 'Milage'] = mean_milage
        return df_copy 
    
    

     
    
    
   
