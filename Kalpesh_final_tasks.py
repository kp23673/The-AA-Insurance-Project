#!/usr/bin/env python
# coding: utf-8

# # Kalpesh_Patil_Tasks

# ## Objectives

# 
# - The primary objective of this project is to analyze customer renewal patterns and performance metrics for The AA Company, with a focus on improving save rates, understanding discount utilization, and identifying key factors influencing customer retention. 
# 
# 
# - This involves calculating and comparing save rates and discount rates for specific months, evaluating team and agent performance, analyzing the impact of tenure mix on renewals, and identifying month-to-month changes in customer behavior. 
# 
# 
# - The insights derived from this analysis aim to help the company optimize its strategies for retaining customers, enhancing team performance, and aligning discounts and pricing with customer preferences, ultimately driving higher renewal rates and long-term loyalty.

# ## Importing necessary libraries

# In[1]:


import numpy as np
import pandas as pd
from warnings import filterwarnings
filterwarnings('ignore')

import matplotlib.pyplot as plt
import seaborn as sns


# ## Extracting Data-Frame from the Excel file sheets

# In[2]:


file = 'TestData for Analyst Interview.xlsx'

data_sheet = pd.read_excel(file, sheet_name=None)

print("Sheet names:", data_sheet.keys())


# In[3]:


data = data_sheet['Dummy Data']
data.head()


# In[4]:


data.shape


# - There are 1,98,989 rows and 18 columns in this dataset.

# ## Main data

# In[5]:


data.head()


# In[6]:


data.info()


# ## Checking Missing Values:

# In[7]:


data.isnull().sum()


# Here we do not need to explicitly handle null values separately for this task because:
# 
# - The condition RENEWAL_PREMIUM > 0 automatically excludes rows where RENEWAL_PREMIUM is null.
# - The volume of transactions (denominator) includes only valid rows that have data for the month and can potentially have a RENEWAL_PREMIUM.
# - Null values in RENEWAL_PREMIUM are not considered in the save rate calculation because they do not represent valid transactions with renewal data. Similarly, for the volume of transactions, only rows with valid transaction details and month information are included.

# ## Task 1

# ### What were the save rates and discount rates for June and July

# In[8]:


data.columns


# In[9]:


save_rate_full_data = data[data['RENEWAL_PREMIUM']>0]['Transaction Month'].count() / len(data)
save_rate_full_data * 100 


# - The goal of Task 1 was to calculate the save rate, which measures the percentage of transactions where customers renewed their services. Specifically, I calculated the save rate for:
# 
# - The entire dataset.
# - The months of June and July, separately.
# 
# - The save rate is calculated as: (Number of Transactions Where (RENEWAL_PREMIUM > 0) / Total Volume of Transactions) * 100
# 
# - Here:
# 
# 1. RENEWAL_PREMIUM > 0 indicates a successful renewal.
# 2. The volume of transactions is the total number of rows for the dataset or a specific month, excluding null values in RENEWAL_PREMIUM.
# 
# - The overall save rate of 74.30%.

# In[10]:


temp_data = data

temp_data['Transaction Month'] = temp_data['TRANSACTION_DATE'].dt.month_name()

june_data = temp_data[temp_data['Transaction Month'] == 'June']
july_data = temp_data[temp_data['Transaction Month'] == 'July']

june_save_rate = june_data[june_data['RENEWAL_PREMIUM'] > 0].shape[0] / june_data.shape[0]
july_save_rate = july_data[july_data['RENEWAL_PREMIUM'] > 0].shape[0] / july_data.shape[0]


print(f"Save Rate for June: {june_save_rate:.2%}")
print(f"Save Rate for July: {july_save_rate:.2%}")


# - The save rates were 74.11% for June and 74.48% for July.
# - About three-quarters of all transactions resulted in renewals across the dataset.
# - The save rate was slightly higher in July compared to June, which might indicate improved renewal performance during that month.

# In[11]:


# Visualization of Save Rates
save_rates = pd.DataFrame({
    'Month': ['June', 'July'],
    'Save Rate (%)': [june_save_rate * 100, july_save_rate * 100]
})

plt.figure(figsize=(10, 6))
sns.barplot(x='Month', y='Save Rate (%)', data=save_rates, palette='coolwarm')
plt.title('Save Rates for June and July', fontsize=16)
plt.ylabel('Save Rate (%)', fontsize=12)
plt.xlabel('Month', fontsize=12)
plt.ylim(0, 100)
for index, value in enumerate(save_rates['Save Rate (%)']):
    plt.text(index, value + 2, f'{value:.2f}%', ha='center', fontsize=10)
plt.show()


# In[12]:


# june_discount_rate
june_total_discount = june_data['TOTAL_DISCOUNT'].sum()
june_invited_premium = june_data['INVITED_PREMIUM'].sum()
june_discount_rate = (june_total_discount / june_invited_premium ) 

# Calculate Discount Rate for July
july_total_discount = july_data['TOTAL_DISCOUNT'].sum()
july_invited_premium = july_data['INVITED_PREMIUM'].sum()
july_discount_rate = (july_total_discount / july_invited_premium)  

# Print results
print(f"Discount Rate for June: {june_discount_rate:.2%}")
print(f"Discount Rate for July: {july_discount_rate:.2%}")


# - I calculated the discount rate for June and July by dividing the total discounts (TOTAL_DISCOUNT) by the total invited premium (INVITED_PREMIUM). 
# 
# 
# - The discount rate tells us what percentage of the premium value was offered as discounts to customers.
# 
# 
# - The results showed that:
# 
#     - In June, the discount rate was 19.47%.
#     - In July, the discount rate increased slightly to 20.19%.
#     - This increase in discounts aligns with the slightly higher save rate in July (74.48% compared to 74.11% in June),   suggesting that offering higher discounts may have positively influenced customer renewals."

# In[13]:


# Visualization of Discount Rates
discount_rates = pd.DataFrame({
    'Month': ['June', 'July'],
    'Discount Rate (%)': [june_discount_rate * 100, july_discount_rate * 100]
})

plt.figure(figsize=(10, 6))
sns.barplot(x='Month', y='Discount Rate (%)', data=discount_rates, palette='viridis')
plt.title('Discount Rates for June and July', fontsize=16)
plt.ylabel('Discount Rate (%)', fontsize=12)
plt.xlabel('Month', fontsize=12)
plt.ylim(0, 25)
for index, value in enumerate(discount_rates['Discount Rate (%)']):
    plt.text(index, value + 0.5, f'{value:.2f}%', ha='center', fontsize=10)
plt.show()


# **Actionable Insights:**
# 
# - July showed slightly higher save rates and discount rates, suggesting that offering more discounts might have encouraged renewals.
# 
# 
# - The save rate for the full dataset is an average that accounts for months with both higher and lower performance, while the save rate for July reflects only one specific, better-performing period. July's performance likely benefited from factors like higher discounts, a favorable customer mix, or effective retention strategies.

# ## Task 2 

# ### Identify the highest and lowest performing team and agent (on save rate) for June and July

# In[14]:


save_rate_team_june = june_data.groupby('TEAM_NAME').apply(lambda x: x[x['RENEWAL_PREMIUM']>0].shape[0] /x.shape[0])

highest_team_june = save_rate_team_june.idxmax(), save_rate_team_june.max()
lowest_team_june = save_rate_team_june.idxmin(), save_rate_team_june.min()

print(f"Highest Performing Team in June: {highest_team_june[0]} with Save Rate: {highest_team_june[1]:.2%}")
print(f"Lowest Performing Team in June: {lowest_team_june[0]} with Save Rate: {lowest_team_june[1]:.2%}")


# - The highest-performing team (Team24) achieved a save rate of 76.73%, meaning that 76.73% of their transactions in June led to successful renewals.
# 
# 
# - The lowest-performing team (Team22) had a save rate of 0.00%, indicating that none of their transactions in June resulted in renewals.

# In[15]:


save_rate_team_july = july_data.groupby('TEAM_NAME').apply(lambda x: x[x['RENEWAL_PREMIUM']>0].shape[0] /x.shape[0])

highest_team_july = save_rate_team_july.idxmax(), save_rate_team_july.max()
lowest_team_july = save_rate_team_july.idxmin(), save_rate_team_july.min()

print(f"Highest Performing Team in June: {highest_team_june[0]} with Save Rate: {highest_team_june[1]:.2%}")
print(f"Lowest Performing Team in June: {lowest_team_june[0]} with Save Rate: {lowest_team_june[1]:.2%}")


# - The team with the highest Save Rate is Team24, with a Save Rate of 76.73%. This means that 76.73% of the cases handled by Team24 resulted in successful renewals.
# 
# - The team with the lowest Save Rate is Team22, with a Save Rate of 0.00%. This means that none of the cases handled by Team22 resulted in successful renewals, which is a significant concern for performance.

# In[16]:


# Save Rates for Teams in June and July
team_save_rates = pd.DataFrame({
    'Team': save_rate_team_june.index.union(save_rate_team_july.index),
    'June Save Rate (%)': save_rate_team_june.reindex(save_rate_team_june.index.union(save_rate_team_july.index), fill_value=0).values * 100,
    'July Save Rate (%)': save_rate_team_july.reindex(save_rate_team_june.index.union(save_rate_team_july.index), fill_value=0).values * 100
}).set_index('Team')

team_save_rates.plot(kind='bar', figsize=(14, 8), colormap='Set2')
plt.title('Team Save Rates for June and July', fontsize=16)
plt.ylabel('Save Rate (%)', fontsize=12)
plt.xlabel('Team', fontsize=12)
plt.legend(title='Month')
plt.ylim(0, 100)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[17]:


save_rate_agent_june = june_data.groupby('OPERATOR_ID').apply(lambda x: x[x['RENEWAL_PREMIUM']>0].shape[0] /x.shape[0])

highest_agent_june = save_rate_agent_june.idxmax(), save_rate_agent_june.max()
lowest_agent_june = save_rate_agent_june.idxmin(), save_rate_agent_june.min()

print(f"Highest Performing Agent in June: {highest_agent_june[0]} with Save Rate: {highest_agent_june[1]:.2%}")
print(f"Lowest Performing Agent in June: {lowest_agent_june[0]} with Save Rate: {lowest_agent_june[1]:.2%}")


# 1. Agent47 is performing exceptionally well, securing renewals in the vast majority of their cases. This could indicate they have a solid strategy or approach for handling cases, which other agents could potentially learn from.
# 
# 
# 2. On the other hand, **Agent100's Save Rate of 0% is concerning**, suggesting that none of their cases resulted in renewals. It may indicate issues such as:
# 
# - **A lack of effective strategies to retain customers.**
# - **Possible challenges in communication or follow-up with clients.**
# - **Training or resource needs.**
# 

# In[18]:


save_rate_agent_july = july_data.groupby('OPERATOR_ID').apply(lambda x: x[x['RENEWAL_PREMIUM']>0].shape[0] /x.shape[0])

highest_agent_july = save_rate_agent_july.idxmax(), save_rate_agent_july.max()
lowest_agent_july = save_rate_agent_july.idxmin(), save_rate_agent_july.min()

print(f"Highest Performing Agent in July: {highest_agent_july[0]} with Save Rate: {highest_agent_july[1]:.2%}")
print(f"Lowest Performing Agent in July: {lowest_agent_july[0]} with Save Rate: {lowest_agent_july[1]:.2%}")


# - Agent244 is excelling with a perfect Save Rate, while Agent100 is facing challenges. 
# 
# 
# - We have to identify the factors that contribute to these outcomes can help improve team performance overall.
# 
# - Factors may be:
#     - Lack of effective renewal strategies.
#     - Insufficient customer follow-up or engagement.
#     - Potential training gaps or other obstacles that hinder their ability to close renewals.

# #### Actionable Findings:
# 
# 
# 1. High performers can share strategies.
# 2. Low performers may need training or other support.

# #### Recommondations:
# 
# 
# - Teams like Team24 and agents like Agent47 / Agent244 can share their techniques and strategies through workshops or mentoring sessions.
#     
# - Focus on upskilling low-performing teams like Team22 and agents like Agent100 by providing specific training on customer engagement, objection handling, and renewal follow-ups.

# ## TASK 3

# ### What was the impact in a change in mix of tenure of callers in July compared to June ?

# In[19]:


june_data.columns


# In[20]:


june_tenure_mix = june_data['TENURE'].value_counts(normalize=True) * 100
july_tenure_mix = july_data['TENURE'].value_counts(normalize=True) * 100

tenure_comparison = pd.DataFrame({
    'June Mix (%)': june_tenure_mix,
    'July Mix (%)': july_tenure_mix
})

tenure_comparison['Change in Mix (%)'] = tenure_comparison['July Mix (%)'] - tenure_comparison['June Mix (%)']

print("Tenure Mix Comparison (June vs July):")
print(tenure_comparison)


# In[21]:


# Tenure Mix Comparison
tenure_comparison.plot(kind='bar', figsize=(14, 8), color=['skyblue', 'orange', 'green'], width=0.8)
plt.title('Tenure Mix Comparison: June vs July', fontsize=16)
plt.ylabel('Percentage (%)', fontsize=12)
plt.xlabel('Tenure', fontsize=12)
plt.legend(['June Mix (%)', 'July Mix (%)', 'Change in Mix (%)'], title='Legend', loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# #### Impact:
# 
# 
# - The Tenure Mix Comparison between June and July reveals notable shifts in the distribution of customer tenure.
# 
# 
# - Customers with a tenure of 20 months represent the largest segment, increasing from 24.40% in June to 26.54% in July, marking a 2.14% growth, which indicates that long-tenured customers may be renewing at a higher rate or new renewals are concentrated among this group. 
# 
# 
# - Conversely, customers with a tenure of 1 month and 2 months experienced declines of 1.13% and 0.81%, respectively, suggesting potential challenges in retaining newer customers. 
# 
# 
# - The slight drop for the 5-month group (-0.64%) and the relatively stable proportions for other tenures indicate a more consistent behavior across mid-tenure customers. 
# 
# 
# - Overall, these changes highlight a potential need for tailored strategies to engage newer customers and maintain loyalty, while leveraging the positive momentum among longer-tenured customers to drive higher renewals.

# #### Recommendations:
# 
# - Develop targeted onboarding and engagement strategies for customers with 1–2 months tenure to improve retention rates.
# 
# 
# - Retain newer customers with better onboarding and follow-ups.
# 
# 
# - Reward long-tenured customers to sustain their loyalty.
#     
#     
# - Investigate slight declines in the 5-month tenure group to identify any specific issues (e.g., product dissatisfaction or lack of communication).
#     
#     
# - Regularly analyze tenure-based trends to ensure strategies remain adaptive to shifts in customer behavior.
# 

# ## Task 4:

#  ### What kind of things would impact the save rates month to month ?

# - Customer Behavior: New customers are more price-sensitive, while long-term ones are more loyal.
# 
# 
# - Discounts: Higher discounts can encourage renewals, but over-dependence may reduce profitability.
# 
# 
# - Agent Performance: Skilled agents and efficient teams drive higher save rates.
# 
# 
# - External Factors: Economic conditions, competitor actions, and even natural events can affect customer decisions.
# 
# 
# - Payment Type: Automatic payments lead to higher renewal rates.

# # 

# ### **General Understanding from this Task as per My Knowledge:**
# 
# - Trends: Save rates improve with higher discounts and better service.
# 
# 
# - Performance Insights: Exceptional agents and teams stand out due to their effective strategies, while poor performers need support.
# 
# 
# - Customer Behavior: Long-tenured customers are loyal, but short-tenured ones need attention.
# 
# 
# - Monthly Changes: External factors, pricing strategies, and customer service all play a role in month-to-month save rate fluctuations.
# 
