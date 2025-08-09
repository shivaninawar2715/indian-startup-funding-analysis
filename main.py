import pandas as pd

#load the dataset
df=pd.read_csv("/content/startup_funding.csv")
display(df.head())

#Standardize date format
df['Date dd/mm/yyyy']=pd.to_datetime(df['Date dd/mm/yyyy'], errors='coerce')

#Remove or fill null values
df=df.dropna(subset=['Date dd/mm/yyyy','Startup Name'])

#Standardize text columns
if 'City Location' in df.columns:
    df['City Location']=df['City Location'].astype(str).str.strip().str.title()
if 'Industry Vertical' in df.columns:
    df['Industry Vertical']=df['Industry Vertical'].astype(str).str.strip().str.title() # Corrected column name from 'Sector' to 'Industry Vertical'


#Correct typo in column name
df.rename(columns={'InvestmentnType': 'Investment Type'}, inplace=True)

#Clean funding amount(remove commas,convert to float)
df['Amount in USD']=df['Amount in USD'].astype(str).str.replace(',','',regex=True)
df['Amount in USD'] = pd.to_numeric(df['Amount in USD'], errors='coerce')

funding_trend=df.groupby('Date dd/mm/yyyy')['Amount in USD'].sum().reset_index()
display(funding_trend.head())

top_sectors=df['Industry Vertical'].value_counts().head(5)
top_cities=df['City  Location'].value_counts().head(5)
top_startups_by_count=df['Startup Name'].value_counts().head(5)
top_startups_by_funding = df.groupby('Startup Name')['Amount in USD'].sum().sort_values(ascending=False).head(10)

display("Top 5 Sectors by Count:")
display(top_sectors)
display("Top 5 Cities by Count:")
display(top_cities)
display("Top 5 Startups by Count:")
display(top_startups_by_count)
display("Top 10 Startups by Total Funding:")
display(top_startups_by_funding)

from collections import Counter

# Convert 'Investors Name' to string and fill NaNs before splitting
investor_list = df['Investors Name'].astype(str).str.split(', ')

all_investors = [investor.strip() for sublist in investor_list for investor in sublist if investor.strip()]
top_investors = Counter(all_investors).most_common(10)
display(top_investors)

investment_type_counts=df['Investment Type'].value_counts()
display(investment_type_counts)

import matplotlib.pyplot as plt
import seaborn as sns

# Ensure Date dd/mm/yyyy in funding_trend is datetime objects
funding_trend['Date dd/mm/yyyy'] = pd.to_datetime(funding_trend['Date dd/mm/yyyy'])

# Resample to monthly frequency
monthly_funding_trend = funding_trend.set_index('Date dd/mm/yyyy').resample('M')['Amount in USD'].sum().reset_index()


# Funding trend plot
plt.figure(figsize=(10,6))
sns.lineplot(data=monthly_funding_trend, x='Date dd/mm/yyyy', y='Amount in USD')
plt.title("Funding Trend Over Time (Monthly)")
plt.xlabel("Date")
plt.ylabel("Amount in USD")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Top sectors
plt.figure(figsize=(8, 5))
sns.barplot(x=top_sectors.values, y=top_sectors.index, palette='viridis')
plt.title("Top Sectors")
plt.xlabel("Number of Startups")
plt.ylabel("Industry Vertical")
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Convert top_investors list of tuples to a pandas DataFrame for easier plotting
top_investors_df = pd.DataFrame(top_investors, columns=['Investor Name', 'Number of Investments'])

plt.figure(figsize=(12, 6)) # Increased figure size for better readability
sns.barplot(x='Investor Name', y='Number of Investments', data=top_investors_df, palette='viridis')
plt.title("Top 10 Investors by Number of Investments")
plt.xlabel("Investor Name")
plt.ylabel("Number of Investments")
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels
plt.tight_layout()
plt.show()