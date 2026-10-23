import pandas as pd

data = pd.read_csv('train.csv')
# checking for missing values
missing_values = data['full_text'].isna().sum()
print(f"Number of missing values in 'full_text': {missing_values}")

