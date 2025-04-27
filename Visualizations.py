import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import re
import arabic_reshaper
from bidi.algorithm import get_display




class Visual:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.df['Year'] = pd.to_datetime(self.df['Year'], format='%Y')
        self.df['Year'] = self.df['Year'].dt.year
       
    #this method is for visualizing the data 
    def comparing_Year_with_Milage_price(self) -> None:
        df_copy = self.df.copy()
        fig,axes = plt.subplots(1,2,figsize=(15,5))
        sns.set_style('whitegrid') 
        sns.set_palette('flare')
        sns.lineplot(data=df_copy, x='Year', y='Milage', ax=axes[0])
        axes[0].set_title('Year vs Milage')
        sns.lineplot(data=df_copy, x='Year', y='Price', ax=axes[1])
        axes[1].set_title('Year vs Price')
    
    #showing the correlation between the numeric columns 
    def heat_map(self,list_numeric_columns : list) -> None:
        df_numeric_columns = self.df[list_numeric_columns].copy()
        plt.figure(figsize=(12, 8))
        sns.heatmap(df_numeric_columns.corr(), annot=True, cmap='crest', fmt='.2f')
        plt.title('Correlation Heatmap')
        plt.show()
    
    #showing the distribution between the year and milage and price
    def Distribution_of_Price_Mileage_Year(self) -> None:
        df_copy = self.df.copy()
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.set_style('whitegrid')
        sns.set_palette('Set2')
        sns.histplot(df_copy['Price'], bins=20, kde=True, ax=axes[0])
        axes[0].set_title('Price Distribution')
        sns.histplot(df_copy['Milage'], bins=20, kde=True, ax=axes[1])
        axes[1].set_title('Mileage Distribution')
        sns.histplot(df_copy['Year'], bins=20, kde=True, ax=axes[2])
        axes[2].set_title('Year Distribution')
    
    #showing the distribution of the Trasnsmission
    def piechart_Transmission(self):
        df_copy = self.df.copy()
        #there are one value of DSG
        df_copy = df_copy.drop(df_copy[df_copy["Transmission"]=='DSG'].index)
        df_copy['Transmission'].groupby(df_copy['Transmission']).count().plot(kind = 'pie',autopct='%1.1f%%',figsize=(10,15),title='Transmission Distribution')  
    
    #showing the highest govermants of the price according to price
    def showing_highest_price(self):
        df_copy = self.df.copy()
        groupby_location_price = df_copy.groupby('Location')['Price'].mean().round().reset_index().sort_values(by = 'Price',ascending=False).head(10)
        groupby_brand_price = df_copy.groupby('Brand')['Price'].mean().round().reset_index().sort_values(by = 'Price',ascending=False).head(10)
        groupby_model_price = df_copy.groupby('Model')['Price'].mean().round().reset_index().sort_values(by = 'Price',ascending=False).head(10)
        fig,axes = plt.subplots(1, 3, figsize=(15, 5))
        sns.barplot(groupby_brand_price, x = 'Brand',y = 'Price',ax=axes[0], palette='viridis',legend=False,hue = 'Brand')
        axes[0].tick_params(axis='x', rotation=90)
        axes[0].set_title('Brand VS Price', fontsize=13)
        sns.barplot(groupby_location_price, x = 'Location',y = 'Price',ax=axes[1], palette='plasma',legend=False,hue = 'Location')
        axes[1].tick_params(axis='x', rotation=90)
        axes[1].set_title('Location VS Price', fontsize=13)
        sns.barplot(groupby_model_price, x = 'Model',y = 'Price',ax=axes[2], palette='inferno',legend=False,hue = 'Model')
        axes[2].tick_params(axis='x', rotation=90)
        axes[2].set_title('Model VS Price', fontsize=13)
    
    #Optional Method
    def regression_plot_price(self):
        df_copy = self.df.copy()
        fig,axes = plt.subplots(1, 2, figsize=(12, 8))
        sns.regplot(data=df_copy.sample(1000), x='Year', y='Price',ax =axes[0])
        axes[0].set_title('Linear Regeression Year')
        sns.regplot(data=df_copy.smaple(1000), x='Milage', y='Price',ax =axes[1])
        axes[1].set_title('Linear Regression Mileage')
    

    def Most_Brands_Purchased(self):
        df_copy = self.df.copy()
        Num_of_cars = df_copy.groupby('Brand')['Model'].count().reset_index().sort_values(by = 'Model',ascending=False).head(20)
        ax = sns.barplot(x=Num_of_cars['Brand'], y=Num_of_cars['Model'], palette='plasma',hue = Num_of_cars['Brand'], legend=False)
        for i, v in enumerate(Num_of_cars['Model']):
           ax.text(i, v + 1, str(v), ha='center', va='bottom')
        plt.title('Most Models Purchased')
        plt.xlabel('Brand')
        plt.ylabel('Number Of Models')
        plt.xticks(rotation=90)
        plt.show()
    
    def violin_plot_price_fuel(self):
        df_copy = self.df.copy()
        sns.set_style('whitegrid')
        sns.set_palette('mako')
        sns.violinplot(data=df_copy, x='Fuel', y='Price')
        plt.title('Price Distribution by Fuel Type')
        plt.show()
    
    def Most_popular_car_colors(self):
        df_copy =self.df.copy()
        color_counts = df_copy['Color'].value_counts()
        sns.barplot(x=color_counts.values, y=color_counts.index, palette='viridis', hue = color_counts)
        plt.title('Most Popular Car Colors')
        plt.xlabel('Number of Cars')
        plt.ylabel('Color')
        plt.show()