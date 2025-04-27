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
import arabic_reshaper
from bidi.algorithm import get_display
class Modify:
    #this constructor takes the dataframe and the list that have columns name that you want to modify
    def __init__ (self,df:pd.DataFrame):
        self.df = df
    
    #drop duplicated rows and remove the illogical data 
    def remove_illogical(self) -> pd.DataFrame:
        df_copy = self.df.copy()
        df_copy = df_copy.drop(df_copy[(df_copy['Year']==2026)|(df_copy['Year']==0)].index)
        df_copy = df_copy.drop_duplicates()
        df_copy = df_copy.drop('Options',axis=1)
        return df_copy
    
    #using regular expression remove the spaces in Brand and Model
    def remove_spaces(self) ->pd.DataFrame:
        df_copy = self.remove_illogical().copy()
        df_copy['Brand'] = df_copy['Brand'].apply(lambda x: re.sub(r'\s*\|\|\s*', ' || ', x))
        df_copy['Model'] = df_copy['Model'].apply(lambda x: re.sub(r'\s*\|\|\s*', ' || ', x))
        return df_copy
    #there are shifting between three columns
    def Fix_shifting(self) ->pd.DataFrame:
        df = self.remove_spaces()
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
            list_means.append(df_copy[col_Mileage].loc[(df_copy[col_year]==year)&(df_copy[col_Mileage].notna())&(df_copy[col_Mileage]!=0)].astype('int64').mean().round())
        dict = {col_year:list_years,col_Mileage:list_means}
        return pd.DataFrame(dict)
    
    #inside this data there are null values about these null values we will fill it with the mean of each car according to the year
    def fill_na_mileage(self,df :pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        list_years = df_copy['Year'].unique()
        list_index_na = df_copy.loc[df_copy['Milage'].isna()].index.to_list()
        for Year in list_years:
           for index_Na in list_index_na:
               if df_copy.loc[index_Na, 'Year'] == Year:
                   mean_milage = df_copy.loc[(df_copy['Year'] == Year) & (df_copy['Milage'].notna()), 'Milage'].astype('int64').mean().round()
                   df_copy.loc[index_Na, 'Milage'] = mean_milage
        df_copy['Milage'] = df_copy['Milage'].astype('int64')
        return df_copy
    
    #fill Zero milage with the mean of year
    def fill_zero_mileage(self,df : pd.DataFrame) -> pd.DataFrame:
        df_copy = df
        df_means = self.getting_mean_of_Mileage_for_every_year('Year','Milage')
        index_zero_values_mileage = df_copy.loc[df_copy['Milage']==0].index.to_list()
        for year in df_means['Year']:
           for index in index_zero_values_mileage:
              if df_copy.loc[index, 'Year'] == year:
                mean_milage = df_means.loc[df_means['Year'] == year, 'Milage'].iloc[0]  # Get the mean Milage for the year
                df_copy.loc[index, 'Milage'] = mean_milage
        return df_copy 
    
    # fill the mileage less than 10000
    def fill_mileage_less_10k(self,df : pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        Group_By_brand_Mileage = df_copy.groupby(['Brand','Year'])['Milage'].mean().round().reset_index()
        Mileage_less_10000 = df_copy[(df_copy['Milage']<10000)&(df_copy['Year']<2024)].index
        for index_1 in Group_By_brand_Mileage.index:
           for index_2 in Mileage_less_10000:
              if (Group_By_brand_Mileage.loc[index_1, 'Brand'] == df_copy.loc[index_2, 'Brand']) and (Group_By_brand_Mileage.loc[index_1, 'Year'] == df_copy.loc[index_2, 'Year']):
                 df_copy.loc[index_2, 'Milage'] = Group_By_brand_Mileage.loc[index_1, 'Milage']
        return df_copy
    
    #replace the price with the mean of each car's brand      
    def fill_price_with_mean_brand(self,df:pd.DataFrame) -> pd.DataFrame:
        df_copy = df.copy()
        df_copy['Price'] = df_copy['Price'].astype('int64')
        Group_by_Brand_Price = df_copy.groupby('Brand')['Price'].mean().round().reset_index()
        Price_than_10000_index = df_copy[df_copy['Price']<100000].index
        for index_1 in Group_by_Brand_Price.index:
            for index_2 in Price_than_10000_index:
                if (Group_by_Brand_Price.loc[index_1, 'Brand'] == df_copy.loc[index_2, 'Brand']):
                   df_copy.loc[index_2, 'Price'] = Group_by_Brand_Price.loc[index_1, 'Price']
        return df_copy 

    #the reshape function       
    def reshape_arabic(self,text : str):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        return bidi_text
    
    #after all of this we need to reshape to arabic font
    def data_reshape_arabic(self,df : pd.DataFrame)-> pd.DataFrame:
        df_copy = df.copy()
        for column in ['Brand','Model','Location','Transmission','Color','Fuel']:
            df_copy[column] = df_copy[column].apply(self.reshape_arabic)
        return df_copy
    
    #filter data from the outliers
    def data_without_outliers(self,df:pd.DataFrame,numeric_cols : list):
        df_copy = df.copy()
        for col in numeric_cols:
            Q1 = df_copy[col].quantile(0.25)
            Q3 = df_copy[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_limit = Q1 - 1.5 * IQR
            upper_limit = Q3 + 1.5 * IQR
            df_copy = df_copy[(df_copy[col] >= lower_limit) & (df_copy[col] <= upper_limit)]
        return df_copy




    
        
    
   
