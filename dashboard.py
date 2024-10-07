#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 13:49:26 2024

@author: rajatthakur
"""

# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from numerize import numerize
import squarify
import seaborn as sb

# Load the data
data = pd.read_csv("/Users/rajatthakur/Desktop/SuperDataScienceML/CollaborationProjects/SDS-CP010-tech-companies-analysis/data/tech-companies.csv")

# Data Preprocessing
for i, marketCap in enumerate(data['Market Cap']):
    marketCap = marketCap.replace('$', '')

    if 'T' in marketCap:
        marketCap = float(marketCap.replace('T', '')) * 1e12
    elif 'B' in marketCap:
        marketCap = float(marketCap.replace('B', '')) * 1e9
    elif 'M' in marketCap:
        marketCap = float(marketCap.replace('M', '')) * 1e6
    else:
        marketCap = float(marketCap)

    data['Market Cap'][i] = marketCap

# Dashboard Layout
st.title("Tech Companies Analysis Dashboard")
st.markdown("This project seeks to analyze a dataset encompassing their rankings, market capitalization, countries of operation, and industry affiliations. Our goal is to uncover insights into market trends, regional variations in market capitalization, and competitive dynamics within different sectors and industries. This analysis will provide a comprehensive overview of the global tech landscape, highlighting key players and trends that can inform strategic decisions, investment strategies, and market positioning.")

# Market Cap Statistics
st.header("Market Cap Statistics")
averageMarketCap = numerize.numerize(data['Market Cap'].mean())
marketCapVariation = numerize.numerize(data['Market Cap'].std())
medianMarketCap = numerize.numerize(data['Market Cap'].median())

st.write(f"**Average Market Cap:** {averageMarketCap}")
st.write(f"**Market Cap Variation:** {marketCapVariation}")
st.write(f"**Median Market Cap:** {medianMarketCap}")

# Top Ten Companies by Market Cap
st.header("Top Ten Companies by Market Cap")
topTenCompanies = data[['Company', 'Market Cap']].sort_values(by='Market Cap', ascending=False).head(10)
formattedTopTenCompanies = topTenCompanies.copy()
formattedTopTenCompanies['Market Cap'] =formattedTopTenCompanies['Market Cap'].apply(numerize.numerize)
st.dataframe(formattedTopTenCompanies)

# Bar Chart: Top Ten Companies
st.subheader("Top Ten Companies Market Cap Bar Chart")
st.markdown("the below bar chart ranks the top ten companies by market capitalization.")
plt.figure(figsize=(15, 8))
ax = sns.barplot(x=topTenCompanies['Company'], y=topTenCompanies['Market Cap'], palette='viridis')
numerized_values = [numerize.numerize(val) for val in topTenCompanies['Market Cap']]
for i, val in enumerate(numerized_values):
    ax.text(i, topTenCompanies['Market Cap'][i], val, ha='center', va='bottom', fontsize=11, color='black')

plt.title('Top Ten Companies according to their market cap', fontsize=16)
plt.xlabel('Company Name', fontsize=12)
plt.ylabel('Market Cap (in Trillion)', fontsize=12)
plt.xticks(rotation=85)
st.pyplot(plt)

# Top Ten Industry by Market Cap
st.header("Top Ten Industries by Market Cap")
topTenIndustries = data.groupby('Industry')['Market Cap'].sum().reset_index()
topTenIndustries = topTenIndustries.sort_values(by='Market Cap', ascending=False).head(10)
formattedTopTenIndustries = topTenIndustries.copy()
formattedTopTenIndustries['Market Cap'] =formattedTopTenIndustries['Market Cap'].apply(numerize.numerize)
st.dataframe(formattedTopTenIndustries)

# Bar chart Top Ten Industry
st.subheader("Top Ten Industry Market Cap Bar Chart")
st.markdown("the below bar chart ranks the top ten industries by market capitalization. The x-axis displays the industry names, while the y-axis represents their market cap in trillions.")
plt.figure(figsize=(15, 8))
ax = sns.barplot(x=topTenIndustries['Industry'], y=topTenIndustries['Market Cap'], palette='viridis')
numerized_values = [numerize.numerize(val) for val in topTenIndustries['Market Cap']]
for i, val in enumerate(numerized_values):
    ax.text(i, topTenCompanies['Market Cap'][i], val, ha='center', va='bottom', fontsize=11, color='black')

plt.title('Top Ten Industry according to their market cap', fontsize=16)
plt.xlabel('Industry Name', fontsize=12)
plt.ylabel('Market Cap (in Trillion)', fontsize=12)
plt.xticks(rotation=85)
st.pyplot(plt)




# Plotly: Market Cap by Country
st.header("Market Cap by Country")
st.markdown("The interactive map visually represents market capitalization by country, using color-coding to highlight variations. Hovering over a country reveals its name and specific market cap value, enabling easy comparison and analysis of regional economic data.")
country_grouped = data.groupby('Country')['Market Cap'].sum().reset_index()
country_grouped['Market Cap'] = country_grouped['Market Cap'].apply(numerize.numerize)
fig = px.choropleth(country_grouped, locations='Country', locationmode='country names',
                    color='Market Cap', hover_name='Country',
                    color_continuous_scale=px.colors.sequential.Viridis)
fig.update_layout(title='Market Cap by Country', title_x=0.5)
st.plotly_chart(fig)

# =============================================================================
# # Bar Chart: Industries by Country
# st.header("Industries by Country with Market Cap")
# country_grouped = data.groupby(['Country', 'Industry'])['Market Cap'].sum().unstack()
# plt.figure(figsize=(15, 5))
# country_grouped.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
# plt.title('Industries by Country with Market Cap', fontsize=16)
# plt.xlabel('Country', fontsize=12)
# plt.ylabel('Total Market Cap', fontsize=12)
# plt.xticks(rotation=80)
# plt.legend(title='Industry', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.tight_layout()
# st.pyplot(plt)
# =============================================================================

# Market Cap Table
st.header("Market Cap Table by Industry and Country")
st.markdown("The table below presents the market capitalization for particular industry and country. Countries without companies in a given industry are indicated with a '0,' while countries with companies in the industry show their total market capitalization. The countries are listed alphabetically from A to Z. The 'ALL' column shows the total market capitalization for each industry across all countries. The 'Total' column at the bottom displays the combined market capitalization of all industries within a specific country.")
pivot_table = data.pivot_table(values='Market Cap', index='Industry', columns='Country', aggfunc='sum',  margins=True)
pivot_table = pivot_table.applymap(lambda x: numerize.numerize(x) if x > 0 else '0')
pivot_table.index = pivot_table.index.map(lambda x: 'Total' if x == 'All' else x)
pivot_table = pivot_table.fillna(0)
st.dataframe(pivot_table)

# Plotly Pie Chart: Market Cap per Industry
st.header("Market Cap per Industry")
st.markdown("The pie chart below illustrates the market capitalization distribution among industries as a percentage. Hovering over each segment of the pie chart will display the industry name, its market capitalization, and its corresponding percentage of the total market capitalization.")
industry_market_cap = data.groupby('Industry')['Market Cap'].sum().reset_index()
fig = go.Figure(
    data=[go.Pie(
        labels=industry_market_cap['Industry'],
        values=industry_market_cap['Market Cap'],
        hoverinfo='label+percent+value',
        textinfo='percent',
        textfont_size=14,
        hole=0.4
    )]
)
fig.update_layout(
    title_text='Market Cap per Industry',
    annotations=[dict(text='Market Cap', x=0.5, y=0.5, font_size=20, showarrow=False)]
)
st.plotly_chart(fig)

# Treemap: Companies Distribution by Industries
st.header("Companies Distribution by Industries")
st.markdown("The treemap below illustrates the distribution of companies across industries. Larger rectangles represent industries with a greater number of companies, while smaller rectangles indicate industries with fewer companies.")
groupedIndustDF = pd.DataFrame(data)
industry_count = groupedIndustDF['Industry'].value_counts().reset_index()
industry_count.columns = ['Industry', 'Count']
industry_abbrevations ={
    'Software—Application' : 'Software App.',
    'Semiconductors' : 'Semiconductors',
    'Information Technology Services' : 'IT Services',
    'Electronic Components' : 'Elec. Components',
    'Software—Infrastructure' : 'Software Infra.',
    'Semiconductor Equipment & Materials' : 'Semi. Equ. & Mats',
    'Communication Equipment' : 'Comm. Equipment',
    'Computer Hardware' : 'Comp. Hardware',
    'Scientific & Technical Instruments' : 'Sci. & Tech. In.',
    'Consumer Electronics' : 'Cons. Elect.',
    'Solar' : 'Solar',
    'Electronics & Computer Distribution' :  'Elec. \n & C.D.'
}
industry_count['Short Industry'] = industry_count['Industry'].map(industry_abbrevations)
labels = [f"{abbr}\n({count})" for abbr, count in zip(industry_count['Short Industry'], industry_count['Count'])]
plt.figure(figsize=(10,9))
squarify.plot(sizes=industry_count['Count'], label=labels,pad = 0.2,
              text_kwargs = {'fontsize': 10, 'color': 'white'},
              color=sb.color_palette("rocket"))
plt.axis('off')
plt.title('Companies Distribution by industries')
legend_text = "\n".join([f"{abbr}: {full}" for full,abbr in industry_abbrevations.items()])
plt.figtext(1,  0.5, legend_text, fontsize=12, bbox={"facecolor":"lightgrey", "alpha":0.5,"pad":5})
st.pyplot(plt)

# =============================================================================
# 
# 
# st.header("Companies Distribution by Industries with Market Cap")
# 
# groupedIndustDF = pd.DataFrame(data)
# 
# industry_count = groupedIndustDF.groupby('Industry').agg(
#                     Company_Count = ('Company','size'),
#                     Market_Cap = ('Market Cap','sum')).reset_index()
# 
# #groupedIndustDF['Industry'].value_counts().reset_index()
# #industry_count.columns = ['Industry', 'Count']
# 
# industry_abbrevations ={
#     'Software—Application' : 'Software App.',
#     'Semiconductors' : 'Semiconductors',
#     'Information Technology Services' : 'IT Services',
#     'Electronic Components' : 'Elec. Components',
#     'Software—Infrastructure' : 'Software Infra.',
#     'Semiconductor Equipment & Materials' : 'Semi. Equ. & Mats',
#     'Communication Equipment' : 'Comm. Equipment',
#     'Computer Hardware' : 'Comp. Hardware',
#     'Scientific & Technical Instruments' : 'Sci. & Tech. In.',
#     'Consumer Electronics' : 'Cons. Elect.',
#     'Solar' : 'Solar',
#     'Electronics & Computer Distribution' :  'Elec. \n & C.D.'
#     
# }
# 
# 
# 
# industry_count['Short Industry'] = industry_count['Industry'].map(industry_abbrevations)
# industry_count['Formatted Market Cap'] = industry_count['Market_Cap'].apply(numerize.numerize)
# 
# 
# labels = [f"{abbr} ({count})\nMarket Cap: {market_cap}" for abbr, count, market_cap
#           in zip(industry_count['Short Industry'], industry_count['Company_Count'],
#                                                                   industry_count['Formatted Market Cap'])]
# 
# 
# fig, ax = plt.subplots(figsize=(12, 8))
# squarify.plot(sizes=industry_count['Market_Cap'], label=labels,pad = 1.5,  
#               text_kwargs = {'fontsize': 10, 'color': 'white', 'weight': 'bold'},
#               color=sb.color_palette("rocket"))
# 
# plt.axis('off')
# plt.title('Companies Distribution by Industry (Market Cap)')
# 
# #legend_text = "\n".join([f"{abbr}: {full}" for full,abbr in industry_abbrevations.items()])
# legend_text = "\n".join(
#     [
#         f"{abbr}: {full}, Market Cap: {market_cap}"
#         for full, abbr, market_cap in zip(
#             industry_count['Industry'],
#             industry_count['Short Industry'],
#             industry_count['Formatted Market Cap']
#         )
#     ]
# )
# plt.figtext(1,  0.5, legend_text, fontsize=10, bbox={"facecolor":"lightgrey", "alpha":0.5,"pad":5})
# 
# st.pyplot(fig)
# 
# 
# =============================================================================

# Bar Chart: Industry Comparison
st.header("Industry Comparison")
st.markdown("The bar chart below compares industries based on their total market capitalization and company count. Hovering over a bar will display the industry name, its total market capitalization, and the number of companies associated with it.")
industry_stats = data.groupby('Industry').agg(Total_Market_Cap=('Market Cap', 'sum'), Company_Count=('Company', 'count')).reset_index()
industry_stats['Total_Market_Cap'] = industry_stats['Total_Market_Cap'].apply(numerize.numerize)
fig2 = px.bar(
    industry_stats, 
    y='Industry', 
    x='Total_Market_Cap', 
    text='Company_Count',
    orientation='h',
    title='Industry Comparison: Total Market Cap vs Company Count',
    labels={'Total_Market_Cap': 'Total Market Cap', 'Industry': 'Industry'},
    hover_data=['Company_Count']
)
st.plotly_chart(fig2)

# Show individual industry data
st.header("Individual Industry Data")
st.markdown("Select an Industry to view its companies listed in descending order by their market capitalization.")
industry_selection = st.selectbox("Select an Industry", data['Industry'].unique())
industry_data = data[data['Industry'] == industry_selection]
industry_data['Market Cap'] = industry_data['Market Cap'].apply(numerize.numerize)
st.dataframe(industry_data[['Company', 'Market Cap', 'Industry']])


# Show individual country data
st.header("Individual Country Data")
st.markdown("Select a Country to explore its companies, including their market capitalization and industry. The market cap column lists companies in descending order by their highest market capitalization, so the company with the largest market cap will be at the top, followed by other relevant details." )
country_selection = st.selectbox("Select a Country", data['Country'].unique())
icountry_data= data[data['Country'] == country_selection]
icountry_data['Market Cap'] = icountry_data['Market Cap'].apply(numerize.numerize)
st.dataframe(icountry_data[['Company', 'Market Cap', 'Industry']])












