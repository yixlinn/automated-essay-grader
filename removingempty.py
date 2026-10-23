import pandas as pd

# now loading the tokenized file into the DataFrame
data = pd.read_csv('tokenized.csv')

# removing rows where the 'full_text' column contains an empty string
data = data[data['full_text'] != '[]']
data.to_csv('cleaned_file.csv', index=False)

