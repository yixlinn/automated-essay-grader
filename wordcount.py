import pandas as pd

# loading the cleaned file into a DataFrame object
data = pd.read_csv('cleaned_file.csv')

# function to calculate the word count
def calculate_word_count(text):
    # counting the number of words by splitting them up
    return len(text.split())

data['word_count'] = data['full_text'].apply(calculate_word_count)
data.to_csv('word_count.csv', index=False)