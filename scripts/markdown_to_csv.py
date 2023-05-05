import pandas as pd
import re
import os
from io import StringIO


# Read the Markdown file and extract the table as a string
# path = os.path.dirname(os.path.abspath('sources_table'))
with open('../sources_table/sources.md', 'r') as f:
    markdown_text = f.read()

table_match = re.search(r'\|(.+)\|[\n|\r\n]\|(.+)\|[\n|\r\n](\|[-:| ]+\|[\n|\r\n])*((\|.+[\n|\r\n])+)', markdown_text)
table_text = table_match.group()

# Convert the table string to a pandas DataFrame and then to CSV
df = pd.read_csv(StringIO(table_text), sep='|', header=0, engine='python')

# We need to drop the first and fifth column, which is empty and then remove the first row, which is the header
df_clean = df.drop(df.columns[[0, 4]], axis=1)
df_clean = df_clean.drop(df_clean.index[0])

# almost there XD now we need to format the url column by removing everything inside the brackets
df_clean[' Url '] = df_clean[' Url '].str.replace(r'\[.*\]', '', regex=True).str.replace(r'\(|\)', '', regex=True)


csv_text = df_clean.to_csv(index=False)

# Write the CSV to a file
with open('../sources_table/sources.csv', 'w') as f:
    f.write(csv_text)
