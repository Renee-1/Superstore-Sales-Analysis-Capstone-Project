# -*- coding: utf-8 -*-
"""Superstore Sales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16qm-LkX8PEEDsUW3PWt2OFYo0gVeFtkq

# Superstore Sales Project

This project involves conducting an Exploratory Data Analysis (EDA) on a Superstore sales dataset spanning four years. The goal is to gain insights and identify sales trends across various dimensions.


____

# Imports
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import seaborn as sns
import plotly
import matplotlib.pyplot as plt

# %matplotlib inline

"""# Get the Data

"""

df = pd.read_csv('/content/drive/MyDrive/Python Project/Superstore Sales Dataset.csv')

df

"""# Exploring & Cleaning Data

"""

df.head() # To display the first 5 rows

df.tail() #To display the last 5 rows

df.shape #To get the dimension of the DataFrame (rows, columns)

"""We can see that there are 9,800 rows and 18 columns in the dataset"""

df.columns #Show the column names

df['Sales'].describe() #generate descriptive statistics of the column 'Sales'

df.info() # Get summary information about the DataFrame

"""There are some null entries in the "Postal Code" column, while all other columns in the dataset are free of null values."""

df['Postal Code'].isnull().sum()     #Check for missing values

(11/9800)*100 # Percentage of null values

df[df["Postal Code"].isnull()] #See NULL rows

"""Rows with postal code NULL are of of Burlington	Vermont.
Deleting/Filling these null cells with 0 may introduce bias or misrepresent the data, especially because 0 is not a valid or meaningful postal code in the dataset, So I'll burlington vermont postal code ie, 5401
"""

df['Postal Code'] =  df['Postal Code'].fillna(5401) # Fill the NULL postal code with 5401

df.isnull().sum()     #Now, there are no NULL values in the dataset.

df[df.duplicated()] #To check the precence of duplicate values

"""There are NO duplicate values found in the dataset."""

df.info()

"""The datatype of Order Date and Ship Date is not datetime, so we need to convert the "Order Date" and "Ship Date" columns from their current data type to the datetime data type."""

df['Order Date']=pd.to_datetime(df['Order Date'])
df['Ship Date']=pd.to_datetime(df['Ship Date'])

df.info()

"""# Visualizations"""

#Histogram - Distribution of Sales
plt.figure(figsize=(8, 4))
sns.histplot(df['Sales'], bins=100, kde=True)
plt.title('Distribution of Sales')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.show()

"""## Timeline"""

# create new columns from the order date , split the date into day, month and year
df['day'] = df['Order Date'].dt.day
df['month'] = df['Order Date'].dt.month
df['year'] = df['Order Date'].dt.year
df.head(3)

# show the sales in each year
year_sales = df.groupby(['year']).sum().sort_values('Sales',ascending=False)
year_sales.reset_index(inplace=True)

# Create the bar plot
plt.figure(figsize=(8, 4))
sns.barplot(year_sales,x='year',y='Sales', palette='crest')

# Label the chart
plt.title('Yearly Sales')
plt.xlabel('year')
plt.ylabel('Sales')

# Rotate the x-labels to prevent overlapping
ax = sns.countplot(x="year", data=year_sales)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

# Group data by year and month, and calculate the sum of sales
monthly_sales = df.groupby(['year', 'month']).sum()

# Reset the index to access the 'Year' and 'Order Date' columns
monthly_sales = monthly_sales.reset_index()

# Create a line plot for each year
plt.figure(figsize=(8, 4))

# Define the colors
colors = ['#FF7F50', '#1E90FF', '#32CD32', '#FFD700']

# Loop through unique years and plot a line for each year
for i, year in enumerate([2015, 2016, 2017, 2018]):
    year_data = monthly_sales[monthly_sales['year'] == year]
    plt.plot(year_data['month'], year_data['Sales'], marker='o', linestyle='-', label=year, color=colors[i])

# Set labels and title
plt.title('Monthly Sales Timeline by Year')
plt.xlabel('Month')
plt.ylabel('Sales')

# Add a legend to differentiate lines by year
plt.legend()

# Display the plot
plt.tight_layout()
plt.show()

"""## Region"""

top_states= df.groupby("State").sum().sort_values("Sales",ascending=False).head(15)
top_states= top_states[['Sales']].round(2)
top_states.reset_index(inplace=True)

# Create the bar plot
plt.figure(figsize=(8, 4))
sns.barplot(top_states,x='State',y='Sales', palette='mako')

# Label the chart
plt.title('Top 15 States')
plt.xlabel('State')
plt.ylabel('Sales')

# Rotate the x-labels to prevent overlapping
ax = sns.countplot(x="State", data=top_states)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

"""California have the most sales"""

top_cities= df.groupby("City").sum().sort_values("Sales",ascending=False).head(15)
top_cities= top_cities[['Sales']].round(2)
top_cities.reset_index(inplace=True)

# Create the bar plot
plt.figure(figsize=(8, 4))
sns.barplot(top_cities,x='City',y='Sales', palette='mako')

# Label the chart
plt.title('Top 15 Cities')
plt.xlabel('City')
plt.ylabel('Sales')

# Rotate the x-labels to prevent overlapping
ax = sns.countplot(x="City", data=top_cities)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

"""New york city have the most sales"""

# Group the data by shipment mode and calculate the sum of sales
region = df.groupby("Region")["Sales"].sum()

# Create the pie chart
plt.figure(figsize=(5, 5))
plt.pie(region, labels=region.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('crest'))

# Add a title to the chart
plt.title("Sales by Region")

# Display the chart
plt.axis('equal')
plt.show()

# Box plot - Sales by Region
plt.figure(figsize=(8, 4))
sns.boxplot(x='Region', y='Sales', data=df, palette='crest')
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales')
plt.show()

"""## Category"""

# Group the data by shipment mode and calculate the sum of sales
Category_sales = df.groupby("Category")["Sales"].sum()

# Create the pie chart
plt.figure(figsize=(5, 5))
plt.pie(Category_sales, labels=Category_sales.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('crest'))

# Add a title to the chart
plt.title("Category Distribution by Sales")

# Display the chart
plt.axis('equal')
plt.show()

"""The Pie Chart clearly depict that the highest sales are observed in the "Technology" category, followed by "Furniture," while the "Office Supplies" category exhibits the lowest sales.


"""

sub_category= df.groupby("Sub-Category").sum().sort_values("Sales",ascending=False)
sub_category= sub_category[['Sales']].round(2)
sub_category.reset_index(inplace=True)

# Create the bar plot
plt.figure(figsize=(8, 4))
sns.barplot(sub_category,x='Sub-Category',y='Sales', palette='mako')

# Label the chart
plt.title('Sub Categories wise Sales')
plt.xlabel('Sub Category')
plt.ylabel('Sales')

# Rotate the x-labels to prevent overlapping
ax = sns.countplot(x="Sub-Category", data=sub_category)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

"""## Customer"""

top_customers = df.groupby(['Customer Name']).sum().sort_values('Sales', ascending=False).head(10)
top_customers = top_customers[['Sales']].round(2)
top_customers.reset_index(inplace=True)

# Create the bar plot
plt.figure(figsize=(8, 4))
sns.barplot(top_customers,x='Customer Name',y='Sales', palette='mako')

# Label the chart
plt.title('Sales by Top 10 Customers')
plt.xlabel('Customer Name')
plt.ylabel('Sales')

# Rotate the x-labels to prevent overlapping
ax = sns.countplot(x="Customer Name", data=top_customers)
ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()
plt.show()

"""## Ship Mode"""

# Group the data by shipment mode and calculate the sum of sales
shipment_mode_sales = df.groupby("Ship Mode")["Sales"].sum()

# Create the pie chart
plt.figure(figsize=(5, 5))
plt.pie(shipment_mode_sales, labels=shipment_mode_sales.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('crest'))

# Add a title to the chart
plt.title("Shipment Mode Distribution by Sales")

# Display the chart
plt.axis('equal')
plt.show()

"""Standard Class is the most common ship mode

## Segment
"""

# Group the data by shipment mode and calculate the sum of sales
segment_sales = df.groupby("Segment")["Sales"].sum()

# Create the pie chart
plt.figure(figsize=(5, 5))
plt.pie(segment_sales, labels=segment_sales.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('crest'))

# Add a title to the chart
plt.title("Segment Distribution by Sales")

# Display the chart
plt.axis('equal')
plt.show()

"""Most orders are from consumers

_______________________________________
"""