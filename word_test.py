import pandas as pd

data = pd.read_csv('cleaned_file.csv')
sample_row = data.sample(1)

def calculate_word_count(text):
    # counting the number of words by splitting them up
    return len(text.split())

# assessing the text from the random row and applying the word count function
sample_text = sample_row['full_text'].values[0]
word_count = calculate_word_count(sample_text)

print(sample_text)
print(word_count)
