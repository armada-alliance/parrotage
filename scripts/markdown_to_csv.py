import pandas as pd
import re
import os
from io import StringIO


# Read the Markdown file and extract the table as a string
with open('../sources_table/sources.md', 'r') as f:
    markdown_text = f.read()

table_match = re.search(r'\|(.+)\|[\n|\r\n]\|(.+)\|[\n|\r\n](\|[-:| ]+\|[\n|\r\n])*((\|.+[\n|\r\n])+)', markdown_text)
table_text = table_match.group()

# Convert the table string to a pandas DataFrame and then to CSV
df = pd.read_csv(StringIO(table_text), sep='|', header=0, engine='python')

new_df = df.loc[df[' Added to Index '] == ' ']
new_df = pd.concat([new_df, df.loc[df[' Added to Index '] == '  ']])

# We need to drop the first and fifth column, which is empty and then remove the first row, which is the header
df_clean = new_df.drop(new_df.columns[[0, 5]], axis=1)


# remove the beginning and ending spaces from the column names
df_clean.columns = df_clean.columns.str.strip()

# almost there XD now we need to format the url column by removing everything inside the brackets, remove the beginning and ending parentheses,
# and remove the beginning and ending spaces
df_clean['Url'] = df_clean['Url'].str.replace(r'\[.*\]', '', regex=True).str.replace(r'\(|\)', '', regex=True).str.strip()
df_clean['Type'] = df_clean['Type'].str.strip()
df_clean['Description (optional)'] = df_clean['Description (optional)'].str.strip()


# Urls that are not in the index into a list
url_list = df_clean.loc[df_clean['Type'] == 'Website']['Url'].tolist()


# The save string to a file called url_sources.txt
with open('../sources_table/new_url_sources.txt', 'w') as f:
    f.write(', '.join(url_list))