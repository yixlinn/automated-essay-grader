import pandas as pd

data = pd.read_csv('cleaned_file.csv')

# selecting a row to test the funciton
sample_row = data.iloc[1]  


print("Text in Selected Row:", sample_row['full_text'])

# function to count the number of sentences
def calculate_sentence_count(text):
    # counting the number of full stops in the text
    return text.count('.')

sentence_count = calculate_sentence_count(sample_row['full_text'])

print("Sentence Count:", sentence_count)
