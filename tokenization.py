# importing the pandas library for data manipulation
import pandas as pd

# loading the file into the DataFrame object
data = pd.read_csv('train.csv')

# filling the missing values with empty strings
data['full_text'] = data['full_text'].fillna('')

# tokenizing the text in the 'full_text' column
data['full_text'] = data['full_text'].apply(lambda text: text.split())

# saving the updated file
data.to_csv('tokenized.csv', index=False)

